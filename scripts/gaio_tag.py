#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""GAIO Configuration Tag generator/verifier.

Deterministic Python port of the hash + tag logic in
/home/tjs/dev/projects/GAIO/widget/GAIO_Widget_v1_0.html (the reference
implementation) and framework/sections/13-configuration-tag.md
(Normalization Spec v1). Where prose and widget code disagree, the
widget code wins -- it is what produced any real-world hashes.

Ported behavior (widget file:line references):
- normalizeForHash()            widget 1496-1514  -> normalize()
- computeGaioHashes()           widget 1516-1524  -> hashes()
  * Canonical Hash  = SHA-256 over the raw config text as-is, UTF-8
    (TextEncoder), lowercase hex. No trailing-newline or whitespace
    manipulation of any kind.
  * Normalized Hash = SHA-256 over normalize(text), UTF-8, lowercase hex.
- getHashHeaderLines()          widget 1526-1529  -> tag block template
- copyOutput()/downloadOutput() widget 2131-2145  -> the tag block is
  inserted AFTER hashing, after the first '# Weight: ...' line
  (regex /^(# Weight: [^\\n]*\\n)/m, first match only). Therefore the
  tag block is OUTSIDE the hashed region: verification strips the
  block and recomputes over the remainder.

Tag ID (GAIO-TAG-YYYYMMDD-XXXXXXXX): the widget contains NO Tag ID
implementation -- Section 13 assigns Tag ID generation to tag-creation
time and allows it to be "derived deterministically from session
metadata" in code-execution environments (13-configuration-tag.md:93).
This tool derives the 8-hex suffix as
sha256(canonical_hash + "|" + normalized_hash + "|" + tag_date)[:8]
-- deterministic from the tagging event's own metadata, unique per
(config bytes, date). The '# Tag ID:' header line is a tool extension:
the widget emits only the 3 hash lines; verify accepts blocks with or
without the Tag ID line, so pure widget-tagged files verify too.

Stdlib only. Windows-safe (UTF-8 I/O, ASCII-only source and console
output; all non-ASCII code points appear as escape sequences).

CLI:
  python scripts/gaio_tag.py generate <config.txt> [--date YYYYMMDD] [--embed]
  python scripts/gaio_tag.py verify   <config.txt>
  python scripts/gaio_tag.py selftest

Exit codes: 0 = success/match, 1 = mismatch or error.
"""

import argparse
import datetime as _dt
import hashlib
import re
import shutil
import sys

NORMALIZATION_SPEC = "v1"

# JavaScript \s (WhiteSpace + LineTerminator productions) differs from
# Python's str \s: JS includes U+FEFF and excludes U+001C-001F / U+0085.
# Rules 14/15 in the widget use JS \s -- replicate its exact class.
_JS_WS_CLASS = (
    "\t\n\x0b\x0c\r "
    "   -     　﻿"
)


def normalize(text: str) -> str:
    """Normalization Spec v1 -- byte-faithful port of normalizeForHash()
    (GAIO_Widget_v1_0.html:1496-1514). Rule numbers match the widget
    comments and 13-configuration-tag.md:150-166."""
    s = text
    # 1. Strip BOM: single leading occurrence, FEFF then FFFE, exactly as
    #    the widget (replace(/^﻿/) has no /g flag).
    s = re.sub("\\A﻿", "", s)
    s = re.sub("\\A￾", "", s)
    s = s.replace("\r\n", "\n").replace("\r", "\n")   # 2. Line endings -> LF
    s = s.replace("—", "--")                     # 3. Em dash -> --
    s = s.replace("–", "-")                      # 4. En dash -> -
    s = re.sub("[“”]", '"', s)              # 5. Smart double quotes -> "
    s = re.sub("[‘’]", "'", s)              # 6. Smart single quotes -> '
    s = s.replace("→", "-->")                    # 7. Right arrow -> -->
    s = s.replace("←", "<--")                    # 8. Left arrow -> <--
    s = s.replace("↔", "<-->")                   # 9. Bidirectional arrow -> <-->
    s = re.sub("[✓✔]", "[x]", s)            # 10. Checkmark -> [x]
    s = s.replace("•", "-")                      # 11. Bullet -> -
    # 12. Trailing whitespace per line. JS /[ \t]+$/gm: multiline $ matches
    #     before \n,  ,   (no \r left after rule 2) and at end.
    s = re.sub("[ \t]+(?=[\n  ]|\\Z)", "", s)
    s = re.sub(r"\n{3,}", "\n\n", s)                  # 13. 3+ newlines -> 2
    s = re.sub("^[%s]+" % _JS_WS_CLASS, "", s)        # 14. Leading file ws (JS \s)
    s = re.sub("[%s]+$" % _JS_WS_CLASS, "", s, flags=0)  # 15. Trailing file ws (JS \s)
    return s


def hashes(text) -> dict:
    """Return {'canonical': hex, 'normalized': hex} exactly as
    computeGaioHashes() (widget 1516-1524): canonical = SHA-256 of the
    raw text UTF-8 bytes as-is; normalized = SHA-256 of normalize(text)
    UTF-8 bytes. Accepts str or bytes (bytes = exact file content, the
    canonical-preserving path)."""
    if isinstance(text, bytes):
        raw = text
        s = text.decode("utf-8")  # a BOM survives as U+FEFF; rule 1 strips it
    else:
        s = text
        raw = text.encode("utf-8")
    return {
        "canonical": hashlib.sha256(raw).hexdigest(),
        "normalized": hashlib.sha256(normalize(s).encode("utf-8")).hexdigest(),
    }


# Tag block as embedded in files. The 3 hash lines are byte-identical to
# getHashHeaderLines() (widget 1526-1529); the Tag ID line is this tool's
# additive extension (optional on verify, so widget-only blocks parse).
_TAG_BLOCK_RE = re.compile(
    rb"(?:# Tag ID: (?P<tag_id>GAIO-TAG-\d{8}-[0-9a-f]{8})\r?\n)?"
    rb"# Canonical Hash \(SHA-256\): (?P<canonical>[0-9a-f]{64})\r?\n"
    rb"# Normalized Hash \(SHA-256\): (?P<normalized>[0-9a-f]{64})\r?\n"
    rb"# Normalization Spec: (?P<spec>v[0-9][0-9.]*)\r?\n"
)

# Widget insertion anchor: /^(# Weight: [^\n]*\n)/m, first match only
# (copyOutput/downloadOutput, widget 2131-2145).
_WEIGHT_LINE_RE = re.compile(rb"(?m)^(# Weight: [^\n]*\n)")


def split_tag_block(data: bytes):
    """Return (match_or_None, remainder_bytes). remainder = file bytes with
    the embedded tag block removed = the exact region the widget hashed."""
    m = _TAG_BLOCK_RE.search(data)
    if not m:
        return None, data
    return m, data[: m.start()] + data[m.end():]


def make_tag_id(canonical_hex: str, normalized_hex: str, date_str: str) -> str:
    suffix = hashlib.sha256(
        ("%s|%s|%s" % (canonical_hex, normalized_hex, date_str)).encode("ascii")
    ).hexdigest()[:8]
    return "GAIO-TAG-%s-%s" % (date_str, suffix)


def tag_block(canonical_hex: str, normalized_hex: str, tag_id: str) -> str:
    """Tag ID line (tool extension) + the widget's exact 3-line template
    (getHashHeaderLines, widget 1526-1529), trailing newline included."""
    return (
        "# Tag ID: %s\n"
        "# Canonical Hash (SHA-256): %s\n"
        "# Normalized Hash (SHA-256): %s\n"
        "# Normalization Spec: %s\n"
        % (tag_id, canonical_hex, normalized_hex, NORMALIZATION_SPEC)
    )


def _read_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def cmd_generate(args) -> int:
    data = _read_bytes(args.config)
    existing, body = split_tag_block(data)
    if existing:
        print("[note] existing tag block found and excluded from the hashed region (re-tagging).")
    h = hashes(body)
    date_str = args.date or _dt.date.today().strftime("%Y%m%d")
    if not re.fullmatch(r"\d{8}", date_str):
        print("[error] --date must be YYYYMMDD", file=sys.stderr)
        return 1
    tag_id = make_tag_id(h["canonical"], h["normalized"], date_str)
    block = tag_block(h["canonical"], h["normalized"], tag_id)
    print(block, end="")
    if args.embed:
        block_b = block.encode("ascii")
        if _WEIGHT_LINE_RE.search(body):
            new = _WEIGHT_LINE_RE.sub(lambda m: m.group(1) + block_b, body, count=1)
            where = "after '# Weight:' line (widget insertion point)"
        else:
            new = block_b + body
            where = "at top of file (no '# Weight:' line found; widget would silently skip)"
        shutil.copyfile(args.config, args.config + ".bak")
        with open(args.config, "wb") as f:
            f.write(new)
        print("[embedded] %s -- backup at %s.bak" % (where, args.config))
    return 0


def cmd_verify(args) -> int:
    data = _read_bytes(args.config)
    m, body = split_tag_block(data)
    if m is None:
        print("[FAIL] no embedded GAIO tag block found in %s" % args.config)
        print("       expected '# Canonical Hash (SHA-256): ...' / '# Normalized Hash"
              " (SHA-256): ...' / '# Normalization Spec: vN' lines.")
        return 1
    expected = {
        "canonical": m.group("canonical").decode("ascii"),
        "normalized": m.group("normalized").decode("ascii"),
    }
    spec = m.group("spec").decode("ascii")
    tag_id = m.group("tag_id")
    if spec != NORMALIZATION_SPEC:
        print("[FAIL] file states Normalization Spec %s; this tool implements %s only."
              " Verify with the spec version stated in the file." % (spec, NORMALIZATION_SPEC))
        return 1
    actual = hashes(body)
    ok = True
    for kind in ("canonical", "normalized"):
        if actual[kind] == expected[kind]:
            print("[OK]       %-10s %s" % (kind, actual[kind]))
        else:
            ok = False
            print("[MISMATCH] %s" % kind)
            print("           expected: %s" % expected[kind])
            print("           actual:   %s" % actual[kind])
    if tag_id:
        print("Tag ID: %s" % tag_id.decode("ascii"))
    if ok:
        print("PASS: config text matches its embedded tag (spec %s)." % spec)
        return 0
    if actual["normalized"] == expected["normalized"]:
        print("FAIL: canonical mismatch with normalized match -- byte-level/encoding"
              " variance (CRLF, BOM, trailing newline), content intact.")
    else:
        print("FAIL: config text has been modified since tagging.")
    return 1


def cmd_selftest(args) -> int:
    """Hand-traced JS parity check: the input below was traced rule-by-rule
    through normalizeForHash() (widget 1496-1514); Python must match."""
    src = (
        "﻿# Title — GAIO\r\n"
        "A → B, “quote”, ‘s’, • item ✓\t \r\n"
        "\r\n\r\n\r\n"
        "End line\r\n\r\n"
    )
    expect = '# Title -- GAIO\nA --> B, "quote", \'s\', - item [x]\n\nEnd line'
    got = normalize(src)
    if got != expect:
        print("[FAIL] normalize() diverges from the hand-traced JS result")
        print("expected: %r" % expect)
        print("actual:   %r" % got)
        return 1
    h = hashes(src)
    assert h["canonical"] == hashlib.sha256(src.encode("utf-8")).hexdigest()
    assert h["normalized"] == hashlib.sha256(expect.encode("utf-8")).hexdigest()
    rt = hashes(src.encode("utf-8"))  # bytes path must agree with str path
    assert rt == h
    print("PASS: normalize() matches the hand-traced JS execution;"
          " canonical/normalized hash inputs confirmed (str and bytes paths agree).")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="gaio_tag.py",
        description="Deterministic GAIO Configuration Tag generator/verifier"
                    " (Python port of GAIO_Widget_v1_0.html hash logic).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate", help="compute hashes + Tag ID, print the tag block")
    g.add_argument("config", help="path to the GAIO config .txt")
    g.add_argument("--date", help="tag date YYYYMMDD (default: today)")
    g.add_argument("--embed", action="store_true",
                   help="also insert the block into the file (backup .bak first)")
    g.set_defaults(func=cmd_generate)
    v = sub.add_parser("verify", help="recompute hashes excluding the embedded tag block")
    v.add_argument("config", help="path to the tagged GAIO config .txt")
    v.set_defaults(func=cmd_verify)
    s = sub.add_parser("selftest", help="JS-parity hand-trace regression check")
    s.set_defaults(func=cmd_selftest)
    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
