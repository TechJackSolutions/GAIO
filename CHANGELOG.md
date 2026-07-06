# Changelog

All notable changes to the GAIO framework. This project uses [Semantic Versioning](https://semver.org/).
The authoritative version and framework statistics live in `framework/manifest.json`.

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
