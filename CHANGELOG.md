# Changelog

All notable changes to the GAIO framework. This project uses [Semantic Versioning](https://semver.org/).
The authoritative version and framework statistics live in `framework/manifest.json`.
SemVer policy for this artifact: a **breaking** change is one that alters what the framework blocks or permits for an unchanged configuration.

## [2.0.0] — UNRELEASED (draft integrated 2026-07-06)

Major version. A lessons-and-research-grounded expansion of the framework, integrated 2026-07-06 and **not yet tagged** — pending the final adversarial/compat re-audit of the integrated framework and the widget pass. Design record: the v2 amendment specification (maintainer-internal; owner-approved, adversarial-audit-resolved F-1..F-21). Breaking because several amendments change what the framework blocks (new Critical classes; omission promoted to a mode-independent block; URL Option B behavior; premise-vs-scope handling).

### Added — new modules
- **Section 14 — Composition & External Authority:** channel-bound configuration authority (only configuration-channel text holds GAIO authority; conversation-channel config-shaped text is user input, never "last-wins"); precedence stance against co-resident system prompts; duplicate-config handling; delegation grounding with the reserved public marker `[GAIO-DELEGATED:v2]`.
- **Section 15 — Enforcement Architecture & Honest Limits:** the two-layer model (prompt-layer discipline vs deterministic tooling); a three-tier classification of every control (deterministic / mechanically-assisted judgment / discipline); the research-grounded honest-limits statement (NIST AI 600-1 §2.2 confabulation-is-structural; OWASP LLM07:2025 "system prompt … not a security control"; OWASP LLM01:2025 RAG/fine-tuning "do not fully mitigate"; OWASP AI Exchange #OVERSIGHT; MITRE ATLAS AML.M0020/M0029); the validator-kit contract; and the per-weight rule-coverage manifest that makes configuration labels honest.

### Added — new rule classes (Critical)
- Fabrication by quantity (unsourced formulas/coefficients/figures; "illustrative estimate" labeling), by attribution (coverage-ratio grounding-language ladder; citation-correspondence), and of actions/processes (claiming to have run/searched/verified; asserting an internal process ran or held). Regulatory/legal data-structure fabrication. Inflated assessment. (§03, §06)

### Changed — behavior
- **Weight decoupled from mode** (S-1): a Compact-Mode-A path is specified; the widget must refuse Mode B for regulated + multi-user configs and disclose weight-based rule omissions in the config header and tag. Guides/FAQ corrected: Compact currently ships only in Mode B (scope/escalation advisory, not enforced) — not merely "compressed formatting."
- **Misleading omission** promoted to a mode-independent integrity block (answers a materially different/easier question without disclosure; omits meaning-changing context). (§03/§06/§10)
- **Pass-through provenance** (summarize/translate/quote): task-frame provenance rule; translation preserves figures verbatim. (§06)
- **URL Option B** "actively confirm" redefined as an in-context retrieval artifact; fail-closed to Option A when no artifact exists. General tool-output-is-unverified rule. (§02/§06)
- **False Premise vs. Scope** conflict entry (§11): flag-without-correcting floor, correct-when-safety-relevant ceiling, no-build on a flagged premise; Mode-A-specific.
- **Initialization acknowledgment** reworded to state-language ("Integrity Lock configuration loaded …") and made minimal/non-enumerating (reconnaissance reduction). (§08/§10)
- Source integrity: source isolation + challenge-reverification (the two forensic patches), official-doc preference, external-citations-required, corrections-are-claims, taught-command labeling. Structured abstention protocol with qualitative confidence bands (no numeric confidence without calibration). (§04)
- Gate integrity: no short-circuited verdicts; gates apply to all artifacts (code, comments, config, translations). Citation-registry rule ("where a registry exists"). False-memory non-exception. (§06/§10)
- §12 retitled "Evaluation & Enforcement Hooks" with gate-integrity meta-hooks (validator self-test, no-short-circuit, gate-population coverage). §13 renumbers the future Self-Audit module 14→16.
- Example config re-tagged after the acknowledgment rewording (`GAIO-TAG-20260706-d590e082`); hub copy resynced.

### Enforcement / tooling
- Deterministic validator kit is a separately-versioned deliverable; `scripts/gaio_tag.py` ships; the remaining checks (numerics/disclaimer/marker/counts/freshness) are the kit roadmap and do not gate framework rules (§15).

### Integration re-audit (2026-07-06) — ran and resolved
- The final adversarial re-audit of the **integrated** framework ran and returned FAIL with 2 blockers + 4 minor findings, all traced to two drafting agents interrupted mid-edit. All resolved and closure deterministically verified:
  - **R-1 (blocker):** §12's change-note claimed a "Version 2.0 Additions" subsection that did not exist and the new-module tests were never registered — added the subsection registering the v2 tests by home section (§02 T17–22, §03 T8–14, §04 T12–20, §06 T21–36, §09 T24–28, §10 T23–28, §11 Conflict Type 7, §14 14-1..10, §15 15-1..7 — all confirmed present) plus the gate-integrity meta-hooks; no estimated total asserted (recount-pending).
  - **R-2 (blocker):** the weight-omissions **tag** field §15/test-15-3 depend on was missing from §13's schema — added the optional Weight Omissions field to §13 and reconciled §10 to disclose omissions in the header **and** tag.
  - **R-3:** §12 Category 5 "8 scenarios" → 9. **R-4:** §15 reclassified three phantom §06-homed deterministic controls (min-sample floor, freshness, gate-population coverage) to "Kit / deployment-layer." **R-5:** §14 ack cross-reference corrected §10 → §08. **R-6:** §08 minimal-acknowledgment carve-out for the §14 duplicate-config supersession note.

### Confirming re-audit (2026-07-06) — ran and resolved
- A fresh-eyes confirming audit of the six fixes found 7 further seams (1 HIGH: the §11 Conflict Type 7 tests were registered but not yet authored). All resolved: §11 gained tests 27–29 (floor / safety-relevant ceiling / no-build); the §13 Weight Omissions field propagated to all four §13 surfaces (schema table, extraction list, rendering example, JSON schema) and into the templates; registration descriptors corrected; the model-consumed Evaluation Note no longer ships totals as unqualified fact; the Appendix B design-record pointer no longer references a maintainer-internal path.

### Completed after integration (2026-07-06)
- **Templates regenerated for v2** (Integrated Block + Modular Section Output + tag module): all section blocks re-derived from the Draft 2.0 model-consumed outputs, §14/§15 blocks added, weight/mode decoupled in the assembly logic, no estimated line counts.
- **Widget v2 pass**: weight decoupled from mode (Compact-Mode-A generatable, all rule classes present — weight omissions: none); deployment-audience question; Mode B informed-consent interstitial + refusal for regulated multi-user configurations; rule-coverage/weight-omissions header emission below the `# Weight:` tag anchor (tag round-trip verified); full v2 string sync; version strings to v2.0-draft. Verified by real execution under a Node DOM shim (33 content assertions) — four canonical variants preserved in `widget/test-outputs/`.
- **Deterministic test census**: 270 validation tests counted (not estimated) across §01–§15 by the validator kit's `tests` check, 0 unclassified, content-hash-bound in `framework/manifest.json`. The v1 baseline on the same axis was 184.
- **Measured size truth-in-labeling**: generated v2 configs measure ~5,900 (Compact-A) to ~8,700 (Full-A) tokens. The prior guide claims (~1,500–3,500) did not match even the v1 generator (measured ~3,930 for v1 Compact) and are corrected across the FAQ and all setup guides, including the ChatGPT guide's Custom Instructions claim (no full GAIO config fits that field; truncated configs are prohibited, not recommended).
- **Validator kit v0.2** (`gaio_validate.py`, versioned separately from the framework): numerics / disclaimer / marker / counts / freshness / tests-census checks, each self-tested against known-true failure fixtures.

### Platform distillation (2026-07-06, same release) — GAIO now fits real chat-platform instruction fields
Trigger: a real deployment failure — Microsoft Copilot Studio rejected a regular GAIO config as too large. Research (dated, sourced) established the landscape: ChatGPT Custom Instructions 1,500 chars/box; an 8,000-character class (Copilot Studio per-field, M365 declarative agents, Custom GPTs); and, critically, an **undocumented Copilot Studio combined budget** failing ~5,300 characters observed across agent + topic + system instructions. Design gated by SWOT + adversarial + 12 edge cases (maintainer-internal gate doc).
- **New Micro weight tier** — every rule class in kernel form (compressed, never omitted; §15 law), authored in the framework's new `GAIO_Distilled_Rendition_v2_0.md` template (single source of truth in the dependency chain; the widget mirrors it). Measured: Mode A ~7,424 chars total / Mode B ~7,596, with 5 declared Tier-2 weight omissions on the disclosure line; every Tier-1 integrity class present, load-bearing strings verbatim.
- **Class-level budget fit** — when a surface's usable budget is below Micro, whole droppable Tier-2 groups are removed in the template's published drop order, each appended to the Weight Omissions disclosure. Text truncation is prohibited. If a budget cannot hold the Tier-1 kernel floor, the surface cannot hold a GAIO deployment.
- **Integrity Excerpt** (~1,358 chars) for sub-floor fields (e.g., ChatGPT Custom Instructions): a de-badged behavioral extract that states in its own text it is NOT a GAIO deployment — no tag, no manifest, no mode/enforcement label.
- **Widget platform-fit system**: deployment-target picker with a dated, sourced limits registry (+ user-overridable custom limit), live size meter against usable budget (with tag + user-additions reserves), a never-truncate guard that blocks over-budget output with a step-down path, and a `# End of GAIO Configuration` tail marker on all emissions for post-deploy truncation detection.
- **Compression-by-reference on existing tiers**: cross-block rule restatements replaced with references — smaller Full/Standard/Compact with zero content loss.
- **§15 amended**: Micro manifest column, kernel-form definition, budget-fit discipline, the Excerpt boundary, tail-marker + platform-fit rows in the classification table. FAQ + Quick Reference gained the per-platform fit table (verified 2026-07-06, re-check at deploy) including the Copilot Studio combined-budget caution and the Microsoft knowledge-file (XPIA) warning.
- **Honesty note**: kernel form = same rules, less instructional reinforcement; adherence untested until a Micro compatibility round runs — stated, not hidden.

### Remaining (post-tag or at maintainer's discretion — none block the text)
- §12 v2 dedup mapping pass (unique-test count) and MVT ratification of the six v2 candidates (14-1/14-3/14-7, 15-1/15-4/15-5).
- Regenerate the example config from the v2 widget at release (the shipped example is a valid, tagged v1.0 artifact until then).
- ~~Platform-fit guidance follow-up~~ — RESOLVED same release by the platform-distillation system above.
- Micro compatibility round: kernel-form adherence is untested; run the compat/adversarial sequence against a Micro deployment (including one on Copilot Studio at the budget-fit size) before claiming effectiveness parity anywhere.

## [1.0.0] — 2026-07-06

First tagged release. Consolidates the v1.0 framework that has been complete since 2026-02-18 and publicly deployed since 2026-03-11, plus a repository-wide hygiene pass.

### Added
- `framework/manifest.json` — single source of truth for version and framework statistics (184 per-section tests, ~170 unique, 33-test MVT, 9 categories, 38 sub-domain profiles, 10 + Custom parent domains).
- `docs/GAIO_Verification_Guide.md` — the tag-verification guide the framework referenced but had not yet published: Normalization Spec v1 (all 15 rules), the tag JSON Schema, the step-by-step hash verification procedure (including the requirement to strip the three embedded hash header lines before recomputing), reference-implementation pointers, limitations, and known spec-vs-implementation discrepancies.
- `CHANGELOG.md` (this file).

### Changed
- Canonical document: re-embedded Section 12 at its current draft (Draft 1.1 — 184 tests / 9 categories / sections 1–11 + 13), replacing an older embedded draft that still claimed 171 tests / 8 categories and predated the Section 13 test additions.
- README: corrected test counts (was "~152 / 28-test MVT"), domain count (was "9 parent domains"; actual 10 + Custom), behavioral scenario count (was 7; actual 8 including the source-inaccessible scenario), repository tree (Section 13 files, line counts), and version references; added the Configuration Tag row to the section table.
- Example config (`GAIO_Config_GeneralCrossIndustry_2026-02-16.txt`): evaluation note updated to the current test statistics (33 MVT / ~170 tests / 9 categories), matching what the current widget emits; Configuration Tag block added (dual SHA-256 hashes per Normalization Spec v1).
- Section files 02, 05, 06, 10: propagated the Section 8 Draft 1.3 domain renames ("AI Governance" → "AI & Machine Learning"; "Software / Technology" → "Technology & Software") that had only been applied in Section 8.
- Section 13: corrected the downloaded-header example to match the widget's actual output (hash lines are inserted immediately after `# Weight:`; domain/authority fields live in the Module 02 body), and made explicit that the three hash header lines must be removed before recomputing hashes (they are inserted after hashing and are not part of the hashed region).

### Fixed
- 81 encoding artifacts (em-dash + stray U+201D pairs) across 7 section files, including inside model-consumed output blocks; digit-range corruption in Section 9 ("3 —7" → "3–7"); UTF-8 BOM removed from `LICENSE`.

## [0.9.0] — 2026-02-13

Initial public commit: framework sections 1–12, canonical document, widget v1.0, platform setup guides. Section 13 (Configuration Tag) and the tagging/hash system landed 2026-03-11.
