#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""GAIO deterministic validator kit v0.2 (kit versioned separately from the
framework -- see framework/sections/15-enforcement-architecture.md, "The
Validator Kit Contract").

Implements the DETERMINISTIC tier of GAIO v2's three-tier enforcement ledger
(amendment spec section 8, F-8): string / format / presence / count / date
checks only. Where a control borders judgment, each check is narrowed to its
mechanical part and the narrowing is stated in --help:

  numerics    numeric-label PRESENCE lint (A-1). Presence-only: whether a
              quantity-bearing line carries a citation marker or an
              illustrative/assumed label. Whether the cited source actually
              CONTAINS the number (citation correspondence) is
              mechanically-assisted-judgment tier and is NOT checked here.
  disclaimer  disclaimer-presence + prohibited-phrase check (A-4/F-20).
              String presence only; whether the disclaimer is legally
              adequate is judgment.
  marker      delegation-marker presence + integrity-core-block heuristic
              (A-9/F-21, section 14). Detects the marker string and keyword
              presence; whether the preamble is faithful GAIO text is
              judgment (see test 14-9: a marker can outlive its preamble).
  counts      count-claims vs framework/manifest.json (CR-23). Pattern-table
              match + integer comparison. Claims mapped to manifest values
              that are themselves strings ("recount pending") are reported
              as unverifiable-yet, never as verified.
  freshness   timestamp presence + parse + age vs SLA (CR-18). A null,
              missing, or unparseable timestamp is STALE -- never fresh.
  tests       deterministic test census over the framework sections/ dir:
              counts validation tests per section file in the two real
              formats (numbered '**Title:**' items; '| Ref |' table rows
              with S13.T1 / 14-1 style refs) inside each file's
              '## Validation Criteria' block. Ambiguous lines are listed as
              unclassified, not guessed. Replaces the estimated totals in
              framework/manifest.json with a counted one.
  all         run applicable checks by extension over a file or directory.
  selftest    each check must FAIL its known-true violation fixture and
              PASS its fixed fixture before being trusted (CR-17).

Scope statement (section 15, kit contract): a pass from this kit means the
deterministic checks passed. It does NOT mean the configuration is compliant,
the deployment is safe, or the judgment-tier / discipline-tier controls held.

Conventions inherited from scripts/gaio_tag.py: stdlib only; byte-level file
reads (utf-8 decode); argparse subcommands; ASCII-only source and console
output (non-console-safe characters are backslash-escaped on emit);
Windows-safe.

Exit codes: 0 = pass (no findings), 1 = findings, 2 = usage error.
Every finding prints file:line, the offending text, and the rule name.
"""

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import sys

KIT_VERSION = "0.2"
DELEGATION_MARKER = "[GAIO-DELEGATED:v2]"


def emit(s=""):
    """ASCII-safe console output (Windows cp1252 consoles must never crash)."""
    sys.stdout.write(s.encode("ascii", "backslashreplace").decode("ascii") + "\n")


def _read_text(path):
    with open(path, "rb") as f:
        return f.read().decode("utf-8", errors="replace")


def _finding(fname, line_no, rule, text, msg=""):
    return {"file": fname, "line": line_no, "rule": rule,
            "text": text.strip()[:160], "msg": msg}


def _print_findings(findings, notes=None):
    for n in (notes or []):
        emit("[note] %s:%s %s" % (n["file"], n["line"], n["msg"]))
    for f in findings:
        emit("[FIND] %s:%d  rule=%s" % (f["file"], f["line"], f["rule"]))
        emit("       | %s" % f["text"])
        if f["msg"]:
            emit("       > %s" % f["msg"])


# ---------------------------------------------------------------------------
# numerics -- numeric-label presence lint (deterministic tier of A-1)
# ---------------------------------------------------------------------------

_PCT = re.compile(r"\b\d[\d,]*(?:\.\d+)?\s?%")
_CUR = re.compile(
    r"[$€£]\s?\d[\d,]*(?:\.\d+)?\s?(?:million|billion|bn|[MBKk])?\b"
    r"|\b\d[\d,]*(?:\.\d+)?\s?(?:USD|EUR|GBP)\b")
_MULT = re.compile(r"\b\d+(?:\.\d+)?x\b")
_COEF = re.compile(r"\b\d+(?:\.\d+)?\s?\*\s?[A-Za-z(]")
_QUANT_RES = ((_PCT, "percentage"), (_CUR, "currency"),
              (_MULT, "multiplier"), (_COEF, "coefficient"))

# Spans excluded from quantity matching: versions, semver, ISO dates,
# test/line IDs. (Dates like 2026-07-06 and refs like 14-1 / S13.T4.)
_EXCL_RES = (
    re.compile(r"\bv\d+(?:\.\d+)*\b"),
    re.compile(r"\b\d+\.\d+\.\d+\b"),
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    re.compile(r"\b[Ss]?\d+-\d+\b"),
    re.compile(r"\bS\d+\.T\d+\b"),
    re.compile(r"\b\d+:\d+\b"),
)
# A line that is entirely a key:value / key=value config pair is skipped.
_KEYVAL_LINE = re.compile(r"^\s*[\w.$-]+\s*[:=]\s*\S+\s*$")
# Quantities inside a double-quoted span are quotations/examples, not the
# author's asserted claims (e.g. GAIO's own gate examples: 'catches lines
# like "reduces risk by 40%"'). Straight and curly double quotes.
_QUOTED_SPAN = re.compile("\"[^\"]{0,300}?\"|“[^“”]{0,300}?”")

# Citation markers: bracketed ref (incl. markdown links), "per <Source>",
# "according to", URL, Art./section/Clause patterns.
_CITE_CI = re.compile(
    r"\[[^\]]+\]|according to|https?://|\b(?:art|article|cl|clause|sec)\.?\s*\d",
    re.I)
_CITE_CS = re.compile(r"\bper\s+[A-Z0-9]|§")
_LABEL = re.compile(
    r"illustrativ|assum|estimat|hypothetical|example|for instance|sample"
    r"|placeholder|not actuarially", re.I)
_TABLE_SKIP = re.compile(r"example|illustrat|assum|hypothetical|sample", re.I)


def _table_skip_lines(lines):
    """Indices of lines inside tables whose header row or nearest preceding
    heading contains example/illustrative/assume-class words."""
    skip = set()
    i, last_heading = 0, ""
    while i < len(lines):
        if lines[i].lstrip().startswith("#"):
            last_heading = lines[i]
        if lines[i].lstrip().startswith("|"):
            start = i
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                i += 1
            header = lines[start]
            if _TABLE_SKIP.search(header) or _TABLE_SKIP.search(last_heading):
                skip.update(range(start, i))
        else:
            i += 1
    return skip


def check_numerics(lines, fname):
    findings = []
    tbl_skip = _table_skip_lines(lines)
    in_code = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or i in tbl_skip:
            continue
        if _KEYVAL_LINE.match(line) and not line.lstrip().startswith("|"):
            continue
        excl = []
        for rx in _EXCL_RES:
            excl.extend(m.span() for m in rx.finditer(line))
        excl.extend(m.span() for m in _QUOTED_SPAN.finditer(line))
        quants = []
        for rx, kind in _QUANT_RES:
            for m in rx.finditer(line):
                if any(m.start() < e and m.end() > s for s, e in excl):
                    continue
                quants.append((m.group(0), kind))
        if not quants:
            continue
        window = "\n".join(lines[max(0, i - 1):i + 2])
        if _CITE_CI.search(window) or _CITE_CS.search(window) or _LABEL.search(window):
            continue
        for qtext, kind in quants:
            findings.append(_finding(
                fname, i + 1, "numeric-label-presence", line,
                "unlabeled %s '%s' -- no citation marker and no "
                "illustrative/assumed/estimate label on or near the line "
                "(GAIO A-1; presence-only: correspondence is judgment-tier)"
                % (kind, qtext)))
    return findings


# ---------------------------------------------------------------------------
# disclaimer -- presence check + prohibited phrases (A-4 / F-20)
# ---------------------------------------------------------------------------

_ASSESS_HEADING = re.compile(
    r"^#{1,6}\s.*(score|assessment|compliance|readiness|maturity)", re.I)
_DISCLAIMER = re.compile(
    r"not\s+(?:legal|professional|financial)\s+advice"
    r"|does\s+not\s+constitute\s+(?:legal|professional|financial)?\s*advice"
    r"|informational\s+purposes\s+only"
    r"|not\s+a\s+substitute\s+for\s+(?:legal|professional)", re.I)
# Ordered longest-first so overlapping matches deduplicate to one finding.
_HARD_PHRASES = (
    ("this certifies that", "prohibited certification language -- use "
     "'Self-Assessment Summary' framing (GAIO A-4)"),
    ("certification statement", "prohibited certification language -- use "
     "'Self-Assessment Summary' (GAIO A-4)"),
    ("certifies that", "prohibited certification language (GAIO A-4)"),
    ("audit-ready", "prohibited term -- the fix is 'audit-aligned'"),
)


def check_disclaimer(lines, fname):
    findings, notes = [], []
    text = "\n".join(lines)
    # Hard flags apply anywhere, assessment-like or not.
    for i, line in enumerate(lines):
        low, consumed = line.lower(), []
        for phrase, msg in _HARD_PHRASES:
            start = 0
            while True:
                p = low.find(phrase, start)
                if p < 0:
                    break
                span = (p, p + len(phrase))
                start = p + 1
                if any(p < e and span[1] > s for s, e in consumed):
                    continue
                consumed.append(span)
                findings.append(_finding(fname, i + 1, "prohibited-phrase",
                                         line, msg))
    assessment_like = any(_ASSESS_HEADING.match(l) for l in lines)
    if assessment_like:
        if not _DISCLAIMER.search(text):
            findings.append(_finding(
                fname, 1, "disclaimer-presence",
                "(document-level)", "assessment-like document (heading "
                "heuristic: score/assessment/compliance/readiness/maturity) "
                "has no not-legal-advice disclaimer pattern (GAIO A-4)"))
    else:
        notes.append({"file": fname, "line": 0, "msg":
                      "not assessment-like by heading heuristic; disclaimer "
                      "presence not required (prohibited phrases still checked)"})
    return findings, notes


# ---------------------------------------------------------------------------
# marker -- delegation marker + integrity-core block (A-9 / F-21 / 14-9)
# ---------------------------------------------------------------------------

_CORE_KEYWORDS = ("fabricat", "verifiable", "scope", "escalat")


def check_marker(text, fname):
    findings = []
    idx = text.find(DELEGATION_MARKER)
    if idx < 0:
        findings.append(_finding(
            fname, 1, "delegation-marker-missing", "(document-level)",
            "delegation marker %s not found -- an ungrounded delegation is "
            "machine-detectable only through this marker (GAIO section 14)"
            % DELEGATION_MARKER))
        return findings
    line_no = text[:idx].count("\n") + 1
    low = text.lower()
    have_hierarchy = "decision hierarchy" in low
    kw_hits = [k for k in _CORE_KEYWORDS if k in low]
    if not (have_hierarchy and len(kw_hits) >= 2):
        findings.append(_finding(
            fname, line_no, "marker-without-preamble", DELEGATION_MARKER,
            "marker present but no integrity-core block found (need "
            "'decision hierarchy' + >=2 of %s; found hierarchy=%s, %s) -- "
            "a marker can outlive its preamble: marker presence alone is "
            "not grounding and carries no GAIO assurance (test 14-9)"
            % (list(_CORE_KEYWORDS), have_hierarchy, kw_hits or "none")))
    return findings


# ---------------------------------------------------------------------------
# counts -- count claims vs framework/manifest.json (CR-23)
# ---------------------------------------------------------------------------

_WORD_NUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
             "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15}

# Ordered pattern table: earlier keys consume their spans first so the
# generic "N tests" pattern cannot re-claim an MVT/dedup-specific claim.
_COUNT_PATTERNS = (
    ("minimum_viable_test_set", (r"\b(\d+)[- ]test\s+MVT",
                                 r"MVT[^\n]{0,80}?\b(\d+)\s+tests\b",
                                 r"\b(\d+)\s+tests\s+that\s+cover",
                                 r"[Mm]inimum\s+[Vv]iable\s+[Tt]est[^\n]{0,40}?\b(\d+)\b")),
    ("tests_unique_after_dedup", (r"~?(\d+)\s+unique\s+(?:tests|after)",
                                  r"unique\s+after\s+dedup\D{0,20}(\d+)")),
    ("tests_per_section_total", (r"\b(\d+)\s+validation\s+tests\b",
                                 r"total\s+of\s+(\d+)\s+tests\b",
                                 r"\b(\d+)\s+tests\b")),
    ("sections", (r"\b(\d+)\s+sections\b", r"\b(\d+)-section\b")),
    ("design_decisions", (r"\b(\d+)\s+design\s+decisions\b",)),
    ("evaluation_categories", (r"\b(\d+)\s+(?:evaluation|test)\s+categor(?:ies|y)\b",)),
    ("subdomain_profiles", (r"\b(\d+)\s+sub-?domain\s+profiles\b",)),
    ("behavioral_scenarios", (r"\b(\d+)\s+behavioral\s+scenarios\b",)),
    ("conflict_types_mapped", (r"\b(\d+)\s+conflict\s+types\b",)),
    ("enforcement_tiers", (r"\b(\d+|one|two|three|four|five)\s+enforcement\s+tiers\b",)),
    ("parent_domains", (r"\b(\d+)\s+parent\s+domains\b",)),
    ("edge_cases_launch", (r"\b(\d+)\s+edge\s+cases\b",)),
)


def check_counts(text, fname, manifest):
    findings, notes = [], []
    stats = manifest.get("statistics", {})
    consumed = []

    def taken(span):
        return any(span[0] < e and span[1] > s for s, e in consumed)

    for key, patterns in _COUNT_PATTERNS:
        for pat in patterns:
            for m in re.finditer(pat, text):
                if taken(m.span()):
                    continue
                consumed.append(m.span())
                raw = m.group(1).lower()
                claim = _WORD_NUM.get(raw) if not raw.isdigit() else int(raw)
                if claim is None:
                    continue
                line_no = text[:m.start()].count("\n") + 1
                line_text = text.splitlines()[line_no - 1] if text else ""
                if key not in stats:
                    notes.append({"file": fname, "line": line_no, "msg":
                                  "claim '%s' maps to manifest key '%s' which is "
                                  "absent -- unverifiable" % (m.group(0), key)})
                    continue
                mval = stats[key]
                if isinstance(mval, str):
                    try:
                        mval = int(mval)
                    except ValueError:
                        notes.append({"file": fname, "line": line_no, "msg":
                                      "claim '%s' (=%d) vs manifest '%s' = %r -- "
                                      "unverifiable-yet (recount pending; skipped "
                                      "numeric comparison)" % (m.group(0), claim,
                                                               key, mval)})
                        continue
                if isinstance(mval, (int, float)) and claim != mval:
                    findings.append(_finding(
                        fname, line_no, "count-vs-manifest", line_text,
                        "claim '%s' (=%d) contradicts manifest '%s' = %s "
                        "(CR-23: enumerable claims counted against the "
                        "primary source)" % (m.group(0), claim, key, mval)))
                else:
                    notes.append({"file": fname, "line": line_no, "msg":
                                  "[ok] claim '%s' matches manifest '%s' = %s"
                                  % (m.group(0), key, mval)})
    return findings, notes


# ---------------------------------------------------------------------------
# freshness -- timestamp presence + parse + SLA age (CR-18)
# ---------------------------------------------------------------------------

_DEFAULT_TS_FIELDS = ("generated_at", "generated", "as_of", "date",
                      "timestamp", "last_updated")


def _parse_ts(value):
    """Return a UTC datetime or None. Accepts ISO 8601 (Z ok), YYYY-MM-DD,
    YYYYMMDD, YYYY/MM/DD, and unix epoch seconds/milliseconds."""
    if isinstance(value, (int, float)):
        v = float(value)
        if v > 1e12:
            v /= 1000.0
        if v > 1e8:
            try:
                return _dt.datetime.fromtimestamp(v, _dt.timezone.utc)
            except (OverflowError, OSError, ValueError):
                return None
        return None
    if not isinstance(value, str) or not value.strip():
        return None
    s = value.strip()
    try:
        d = _dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=_dt.timezone.utc)
        return d
    except ValueError:
        pass
    for fmt in ("%Y%m%d", "%Y/%m/%d"):
        try:
            return _dt.datetime.strptime(s, fmt).replace(tzinfo=_dt.timezone.utc)
        except ValueError:
            continue
    return None


def check_freshness(obj, fname, fields=None, sla_days=None, now=None):
    findings, notes = [], []
    fields = tuple(fields) if fields else _DEFAULT_TS_FIELDS
    now = now or _dt.datetime.now(_dt.timezone.utc)
    if not isinstance(obj, dict):
        findings.append(_finding(fname, 1, "freshness-stale", "(document-level)",
                                 "top-level JSON is not an object; no timestamp "
                                 "field -- STALE (a missing timestamp is never fresh)"))
        return findings, notes
    lower_map = {k.lower(): k for k in obj}
    key = next((lower_map[f.lower()] for f in fields if f.lower() in lower_map), None)
    if key is None:
        findings.append(_finding(
            fname, 1, "freshness-stale", "(document-level)",
            "no timestamp field among %s -- STALE (CR-18: null/missing "
            "timestamp is stale, never fresh)" % (list(fields),)))
        return findings, notes
    ts = _parse_ts(obj[key])
    if ts is None:
        findings.append(_finding(
            fname, 1, "freshness-stale", "%s: %r" % (key, obj[key]),
            "timestamp field '%s' is null/unparseable -- STALE, never fresh "
            "(CR-18)" % key))
        return findings, notes
    age_days = (now - ts).total_seconds() / 86400.0
    if sla_days is not None and age_days > sla_days:
        findings.append(_finding(
            fname, 1, "freshness-sla", "%s: %r" % (key, obj[key]),
            "age %.1f days exceeds SLA of %d days" % (age_days, sla_days)))
    else:
        notes.append({"file": fname, "line": 0, "msg":
                      "timestamp '%s' parsed OK; age %.1f days%s"
                      % (key, age_days,
                         (" (within %d-day SLA)" % sla_days) if sla_days is not None else "")})
    return findings, notes


# ---------------------------------------------------------------------------
# tests -- deterministic test census over framework section files
# ---------------------------------------------------------------------------

_VC_HEADING = re.compile(r"^## Validation Criteria\s*$")
_H2 = re.compile(r"^## ")
_NUMBERED_TEST = re.compile(r"^(\d+)\.\s+\*\*([^*]+?)\*\*")
_NUMBERED_ANY = re.compile(r"^(\d+)\.\s+\S")
_TABLE_REF = re.compile(r"^(?:S\d+\.T\d+|\d+-\d+)$")
_SEP_CELL = re.compile(r"^:?-{2,}:?$")


def _census_one(name, text, secnum):
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if _VC_HEADING.match(l)), None)
    entry = {"file": name, "tests": 0, "ids": [], "unclassified": [],
             "warnings": [], "note": ""}
    if start is None:
        entry["note"] = ("no '## Validation Criteria' heading found -- 0 tests "
                         "defined in this file (section 12 is the registry: "
                         "tests are authored in home sections and referenced "
                         "there, per its own text)")
        return entry
    end = next((i for i in range(start + 1, len(lines)) if _H2.match(lines[i])),
               len(lines))
    seen = set()
    in_ref_table = False
    for i in range(start + 1, end):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            first = cells[0] if cells else ""
            if first.lower() == "ref":
                in_ref_table = True
                continue
            if _SEP_CELL.match(first.replace(" ", "")):
                continue
            if _TABLE_REF.match(first):
                tid = first
                if tid in seen:
                    entry["warnings"].append("duplicate test ref %s at line %d"
                                             % (tid, i + 1))
                seen.add(tid)
                title = cells[1].strip("* ") if len(cells) > 1 else ""
                entry["ids"].append("%s (%s)" % (tid, title[:60]) if title else tid)
                entry["tests"] += 1
            elif in_ref_table and first:
                entry["unclassified"].append(
                    {"line": i + 1, "text": stripped[:120],
                     "why": "row in a '| Ref |' table whose first cell does not "
                            "match a test-ref pattern"})
            continue
        in_ref_table = False
        m = _NUMBERED_TEST.match(stripped)
        if m:
            num, title = int(m.group(1)), m.group(2).rstrip(": ")
            tid = "S%d.T%d" % (secnum, num)
            if tid in seen:
                entry["warnings"].append("duplicate numbered test %s at line %d"
                                         % (tid, i + 1))
            seen.add(tid)
            entry["ids"].append("%s (%s)" % (tid, title[:60]))
            entry["tests"] += 1
        elif _NUMBERED_ANY.match(stripped):
            entry["unclassified"].append(
                {"line": i + 1, "text": stripped[:120],
                 "why": "numbered item without the bold '**Title:**' test format"})
    return entry


def run_census(sections_dir):
    files = sorted(
        f for f in os.listdir(sections_dir)
        if re.match(r"^\d{2}-.*\.md$", f) and ".bak" not in f)
    census = {
        "kit_version": KIT_VERSION,
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "definition": ("Deterministic count of validation tests DEFINED in each "
                       "section file's '## Validation Criteria' block. Formats "
                       "counted: numbered '**Title:**' items and '| Ref |' table "
                       "rows with S<sec>.T<n> or <sec>-<n> refs. Ambiguous lines "
                       "are listed as unclassified, not counted. Section 12 "
                       "registers tests by reference and defines none. Each "
                       "count is content-hash-bound: it holds for the sha256 "
                       "recorded per file and must be re-run after any edit "
                       "(a verdict must not outlive an edit)."),
        "sections_dir": sections_dir,
        "files": [],
        "grand_total": 0,
        "unclassified_total": 0,
    }
    combined = hashlib.sha256()
    for f in files:
        secnum = int(f[:2])
        with open(os.path.join(sections_dir, f), "rb") as fh:
            data = fh.read()
        combined.update(hashlib.sha256(data).digest())
        entry = _census_one(f, data.decode("utf-8", errors="replace"), secnum)
        entry["sha256"] = hashlib.sha256(data).hexdigest()
        census["files"].append(entry)
        census["grand_total"] += entry["tests"]
        census["unclassified_total"] += len(entry["unclassified"])
    census["combined_sha256"] = combined.hexdigest()
    return census


# ---------------------------------------------------------------------------
# subcommand handlers
# ---------------------------------------------------------------------------

def _exit_for(findings):
    return 1 if findings else 0


def cmd_numerics(args):
    findings = check_numerics(_read_text(args.file).splitlines(), args.file)
    _print_findings(findings)
    emit("numerics: %d finding(s) in %s" % (len(findings), args.file))
    return _exit_for(findings)


def cmd_disclaimer(args):
    findings, notes = check_disclaimer(_read_text(args.file).splitlines(), args.file)
    _print_findings(findings, notes)
    emit("disclaimer: %d finding(s) in %s" % (len(findings), args.file))
    return _exit_for(findings)


def cmd_marker(args):
    findings = check_marker(_read_text(args.file), args.file)
    _print_findings(findings)
    emit("marker: %d finding(s) in %s" % (len(findings), args.file))
    return _exit_for(findings)


def _load_manifest(path):
    with open(path, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


def cmd_counts(args):
    manifest = _load_manifest(args.manifest)
    findings, notes = check_counts(_read_text(args.file), args.file, manifest)
    _print_findings(findings, notes)
    emit("counts: %d finding(s), %d note(s) in %s"
         % (len(findings), len(notes), args.file))
    return _exit_for(findings)


def cmd_freshness(args):
    try:
        with open(args.file, "rb") as f:
            obj = json.loads(f.read().decode("utf-8"))
    except (ValueError, OSError) as e:
        emit("[FIND] %s:1  rule=freshness-stale" % args.file)
        emit("       > file unreadable or not valid JSON (%s) -- STALE" % e)
        return 1
    fields = args.field if args.field else None
    findings, notes = check_freshness(obj, args.file, fields=fields,
                                      sla_days=args.sla_days)
    _print_findings(findings, notes)
    emit("freshness: %d finding(s) in %s" % (len(findings), args.file))
    return _exit_for(findings)


def cmd_tests(args):
    census = run_census(args.sections_dir)
    out_json = json.dumps(census, indent=2)  # ensure_ascii default -> ASCII
    emit(out_json)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(out_json + "\n")
        emit("[written] %s" % args.out)
    emit("")
    emit("%-42s %6s %12s" % ("file", "tests", "unclassified"))
    for e in census["files"]:
        emit("%-42s %6d %12d" % (e["file"], e["tests"], len(e["unclassified"])))
    emit("%-42s %6d %12d" % ("TOTAL", census["grand_total"],
                             census["unclassified_total"]))
    return 0


def cmd_all(args):
    targets = []
    if os.path.isdir(args.path):
        for root, dirs, files in os.walk(args.path):
            dirs[:] = [d for d in dirs if not d.startswith(".")
                       and d != "node_modules"]
            for f in files:
                if ".bak" in f:
                    continue
                if f.lower().endswith((".md", ".txt", ".json")):
                    targets.append(os.path.join(root, f))
    else:
        targets.append(args.path)
    manifest = _load_manifest(args.manifest) if args.manifest else None
    total, rows = 0, []
    for path in sorted(targets):
        per = {}
        if path.lower().endswith(".json"):
            try:
                with open(path, "rb") as f:
                    obj = json.loads(f.read().decode("utf-8"))
                fnd, _ = check_freshness(obj, path, sla_days=args.sla_days)
            except (ValueError, OSError):
                fnd = [_finding(path, 1, "freshness-stale", "(unreadable)",
                                "not valid JSON -- STALE")]
            per["freshness"] = fnd
        else:
            text = _read_text(path)
            lines = text.splitlines()
            per["numerics"] = check_numerics(lines, path)
            per["disclaimer"] = check_disclaimer(lines, path)[0]
            if DELEGATION_MARKER[:15] in text:  # "[GAIO-DELEGATED"
                per["marker"] = check_marker(text, path)
            if manifest:
                per["counts"] = check_counts(text, path, manifest)[0]
        for rule, fnd in per.items():
            _print_findings(fnd)
            total += len(fnd)
        rows.append((path, {k: len(v) for k, v in per.items()}))
    emit("")
    emit("=== all: summary ===")
    for path, counts in rows:
        emit("%s  %s" % (path, " ".join("%s=%d" % kv for kv in sorted(counts.items()))
                         or "(no applicable checks)"))
    emit("TOTAL findings: %d" % total)
    return 1 if total else 0


# ---------------------------------------------------------------------------
# selftest -- known-true fixtures (CR-17: a detector is trusted only after
# failing its violation fixture and passing its fixed fixture)
# ---------------------------------------------------------------------------

def cmd_selftest(args):
    results = []

    def case(name, expect, got_findings):
        n = len(got_findings)
        ok = (n > 0) if expect == "FAIL" else (n == 0)
        results.append(ok)
        emit("[%s] %-38s expected=%s findings=%d"
             % ("ok" if ok else "SELFTEST-FAIL", name, expect, n))
        if not ok:
            for f in got_findings:
                emit("        stray: %s -- %s" % (f["rule"], f["msg"][:100]))

    emit("gaio_validate.py v%s selftest" % KIT_VERSION)
    emit("")

    # numerics
    viol = ["The program delivers 3x ROI and cuts incident cost by 43%, "
            "saving $1.2M annually."]
    f = check_numerics(viol, "<numerics-viol>")
    case("numerics violation (3 quantities)", "FAIL", f)
    results.append(len(f) == 3)
    emit("[%s] %-38s expected exactly 3, got %d"
         % ("ok" if len(f) == 3 else "SELFTEST-FAIL", "numerics count", len(f)))
    fixed = ["The program delivers 3x ROI (illustrative estimate -- not "
             "actuarially derived).",
             "Breaches cost $4.45M on average per IBM Cost of a Data Breach.",
             "Latency improved 43% according to the benchmark report [1]."]
    case("numerics fixed (label/cite suppress)", "PASS",
         check_numerics(fixed, "<numerics-fixed>"))
    skips = ["```", "roi = 3x", "```", "Released v2.0.0 on 2026-07-06.",
             "See test 14-1 and S13.T4.", "threshold: 95%",
             "| Illustrative example | 40% |", "| more | 60% |"]
    case("numerics skip rules (code/ver/ids/kv/table)", "PASS",
         check_numerics(skips, "<numerics-skip>"))
    quoted = ['Gate 1 catches lines like "this reduces risk by 40%."']
    case("numerics quoted-span exclusion", "PASS",
         check_numerics(quoted, "<numerics-quoted>"))

    # disclaimer
    dviol = ["# Compliance Readiness Assessment", "",
             "Certification Statement: this certifies that Acme Corp is "
             "audit-ready."]
    f, _ = check_disclaimer(dviol, "<disclaimer-viol>")
    case("disclaimer violation (missing + phrases)", "FAIL", f)
    rules = sorted({x["rule"] for x in f})
    ok = rules == ["disclaimer-presence", "prohibited-phrase"]
    results.append(ok)
    emit("[%s] %-38s rules=%s" % ("ok" if ok else "SELFTEST-FAIL",
                                  "disclaimer rule coverage", rules))
    dfixed = ["# Compliance Readiness Assessment", "",
              "Self-Assessment Summary. This output is informational and is "
              "not legal advice. The artifact is audit-aligned."]
    case("disclaimer fixed", "PASS", check_disclaimer(dfixed, "<disclaimer-fixed>")[0])

    # marker
    case("marker missing", "FAIL",
         check_marker("Do the research task. Decision hierarchy applies; "
                      "never fabricate; stay in scope.", "<marker-viol1>"))
    case("marker without preamble", "FAIL",
         check_marker("Task:\n%s\nGo do it." % DELEGATION_MARKER, "<marker-viol2>"))
    case("marker fixed (marker + core block)", "PASS",
         check_marker("%s\nDecision hierarchy: integrity over helpfulness. "
                      "Never fabricate; every claim must be verifiable; stay "
                      "within scope; escalate to a human when uncertain."
                      % DELEGATION_MARKER, "<marker-fixed>"))

    # counts
    man = {"statistics": {"sections": 15, "behavioral_scenarios": 9,
                          "tests_per_section_total": "184 baseline -- RECOUNT PENDING"}}
    f, _ = check_counts("The framework has 14 sections and 9 behavioral "
                        "scenarios.", "<counts-viol>", man)
    case("counts violation (14 != 15 sections)", "FAIL", f)
    results.append(len(f) == 1)
    emit("[%s] %-38s expected exactly 1, got %d"
         % ("ok" if len(f) == 1 else "SELFTEST-FAIL", "counts precision", len(f)))
    f, notes = check_counts("The framework has 15 sections and 9 behavioral "
                            "scenarios across 184 validation tests.",
                            "<counts-fixed>", man)
    case("counts fixed (+ recount-pending note)", "PASS", f)
    ok = any("unverifiable-yet" in n["msg"] for n in notes)
    results.append(ok)
    emit("[%s] %-38s unverifiable-yet note present=%s"
         % ("ok" if ok else "SELFTEST-FAIL", "counts recount-pending handling", ok))

    # freshness
    case("freshness missing timestamp", "FAIL",
         check_freshness({"name": "x"}, "<fresh-viol1>")[0])
    case("freshness null timestamp", "FAIL",
         check_freshness({"generated_at": None}, "<fresh-viol2>")[0])
    case("freshness unparseable timestamp", "FAIL",
         check_freshness({"generated_at": "not-a-date"}, "<fresh-viol3>")[0])
    case("freshness SLA breach", "FAIL",
         check_freshness({"generated_at": "2020-01-01"}, "<fresh-viol4>",
                         sla_days=2)[0])
    now_iso = _dt.datetime.now(_dt.timezone.utc).isoformat()
    case("freshness fixed (fresh within SLA)", "PASS",
         check_freshness({"generated_at": now_iso}, "<fresh-fixed>",
                         sla_days=30)[0])

    # tests census
    a = ("## Validation Criteria\n\n1. **Alpha test:** Does it work?\n"
         "2. **Beta test:** Does it hold?\n3. Gamma check without bold title\n")
    ea = _census_one("<census-a>", a, 4)
    ok = ea["tests"] == 2 and len(ea["unclassified"]) == 1
    results.append(ok)
    emit("[%s] %-38s tests=%d unclassified=%d (expected 2/1)"
         % ("ok" if ok else "SELFTEST-FAIL", "census numbered + unclassified",
            ea["tests"], len(ea["unclassified"])))
    b = ("## Validation Criteria\n\n| Ref | Test | Pass | Fail |\n"
         "|-----|------|------|------|\n| 14-1 | **X** | p | f |\n"
         "| 14-2 | **Y** | p | f |\n")
    eb = _census_one("<census-b>", b, 14)
    ok = eb["tests"] == 2 and not eb["unclassified"]
    results.append(ok)
    emit("[%s] %-38s tests=%d (expected 2, table refs %s)"
         % ("ok" if ok else "SELFTEST-FAIL", "census ref-table", eb["tests"],
            eb["ids"]))
    c = "## Other Heading\n\n1. **Not a criteria block:** ignored.\n"
    ec = _census_one("<census-c>", c, 12)
    ok = ec["tests"] == 0 and "no '## Validation Criteria'" in ec["note"]
    results.append(ok)
    emit("[%s] %-38s tests=%d note-present=%s"
         % ("ok" if ok else "SELFTEST-FAIL", "census no-block (registry case)",
            ec["tests"], ok))

    emit("")
    if all(results):
        emit("SELFTEST PASS: %d/%d assertions -- every check failed its "
             "known-true violation fixture and passed its fixed fixture."
             % (len(results), len(results)))
        return 0
    emit("SELFTEST FAIL: %d/%d assertions passed. Do NOT trust the failing "
         "detector (CR-17)." % (sum(results), len(results)))
    return 1


# ---------------------------------------------------------------------------

def main(argv=None):
    p = argparse.ArgumentParser(
        prog="gaio_validate.py",
        description="GAIO deterministic validator kit v%s -- string/format/"
                    "presence/count/date checks only (the deterministic tier "
                    "of GAIO v2 section 15). A pass here does NOT mean the "
                    "judgment-tier or discipline-tier controls held."
                    % KIT_VERSION)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("numerics", help="numeric-label PRESENCE lint: flag "
                       "authoritative-looking quantities (%%, currency, Nx, "
                       "coefficients) with neither a citation marker nor an "
                       "illustrative/assumed label nearby. Presence-only: "
                       "whether the cited source CONTAINS the number is "
                       "judgment-tier and not checked. Skips: code fences, "
                       "tables with example/illustrative/assume headers, "
                       "versions/dates/test-IDs, whole-line key:value pairs, "
                       "and quantities inside double-quoted spans "
                       "(quotations/examples, not asserted claims).")
    s.add_argument("file")
    s.set_defaults(func=cmd_numerics)

    s = sub.add_parser("disclaimer", help="assessment-like docs (heading "
                       "heuristic: score/assessment/compliance/readiness/"
                       "maturity) must contain a not-legal-advice disclaimer; "
                       "'Certification Statement'/'certifies that'/"
                       "'audit-ready' are hard-flagged anywhere (fix: "
                       "'audit-aligned'). Legal adequacy is judgment-tier.")
    s.add_argument("file")
    s.set_defaults(func=cmd_disclaimer)

    s = sub.add_parser("marker", help="delegation-marker check: %s present "
                       "AND an integrity-core block in the document "
                       "('decision hierarchy' + >=2 of fabricat/verifiable/"
                       "scope/escalat). Keyword presence only: preamble "
                       "faithfulness is judgment-tier." % DELEGATION_MARKER)
    s.add_argument("file")
    s.set_defaults(func=cmd_marker)

    s = sub.add_parser("counts", help="find count claims matching manifest "
                       "statistics keys via a fixed pattern table; flag "
                       "integer contradictions. 'recount pending' string "
                       "values are reported unverifiable-yet, never verified.")
    s.add_argument("file")
    s.add_argument("--manifest", required=True,
                   help="path to framework/manifest.json")
    s.set_defaults(func=cmd_counts)

    s = sub.add_parser("freshness", help="JSON timestamp must exist and "
                       "parse; null/missing/unparseable = STALE, never "
                       "fresh; with --sla-days, age > SLA is a finding.")
    s.add_argument("file")
    s.add_argument("--sla-days", type=int, default=None)
    s.add_argument("--field", action="append", default=None,
                   help="timestamp field name(s); default: %s"
                        % (", ".join(_DEFAULT_TS_FIELDS)))
    s.set_defaults(func=cmd_freshness)

    s = sub.add_parser("tests", help="deterministic test census: count "
                       "validation tests per section file (numbered "
                       "'**Title:**' items + '| Ref |' table rows) inside "
                       "'## Validation Criteria' blocks; ambiguous lines go "
                       "to 'unclassified' rather than being guessed. JSON to "
                       "stdout and --out.")
    s.add_argument("sections_dir")
    s.add_argument("--out", default=None)
    s.set_defaults(func=cmd_tests)

    s = sub.add_parser("all", help="run applicable checks by extension over "
                       "a file/dir: .md/.txt -> numerics + disclaimer (+ "
                       "marker if the file contains the marker prefix; + "
                       "counts if --manifest); .json -> freshness.")
    s.add_argument("path")
    s.add_argument("--manifest", default=None)
    s.add_argument("--sla-days", type=int, default=None)
    s.set_defaults(func=cmd_all)

    s = sub.add_parser("selftest", help="run every check against embedded "
                       "known-true violation and fixed fixtures (CR-17).")
    s.set_defaults(func=cmd_selftest)

    try:
        args = p.parse_args(argv)
    except SystemExit as e:
        # argparse exits 2 on usage error already; preserve it.
        raise e
    try:
        return args.func(args)
    except OSError as e:
        emit("[usage-error] %s" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
