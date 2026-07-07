# Contributing to GAIO

GAIO is an open standard for AI output integrity. Contributions are welcome — and because this is an *integrity* framework, contributions are held to the framework's own rules. The fastest way to a merged PR is to read this page first.

## What we accept

| Contribution | Where it goes | Template |
|---|---|---|
| **New edge cases** | Section 7 (Edge Case Handling) | Section 7's submission template — includes the observed failure, the rule gap it exposes, and a proposed handling pattern |
| **Domain / sub-domain profiles** | Section 8 (Domain Configuration Profiles) | Section 8's contribution template — parent defaults, sources, triggers, scope hints |
| **Verified source lists** | Section 2 / Section 8 source tiers | Sources must be official/primary and resolvable by a reader |
| **Rule amendments and fixes** | The relevant section file | See "The propagation chain" below — a rule change is never a one-file change |
| **Widget fixes** (code) | `widget/` | Apache 2.0; match existing conventions; include test evidence |
| **Validation tests** | The owning section's Validation Criteria | Registered by reference in Section 12; the test total is recounted deterministically (see below) |
| **Corrections to counts, citations, or claims** | Anywhere | The best kind of PR. Show the primary source |

## The non-negotiables (the framework's rules apply to contributions)

1. **No fabricated authorities, statistics, or citations.** Every specific claim in a contribution must trace to a verifiable source, or be labeled as illustrative. A citation must point to the source that actually contains the claim.
2. **No estimated counts presented as fact.** Framework statistics live in `framework/manifest.json` and are counted deterministically. If your change adds or removes validation tests, say so — the census is re-run at integration.
3. **US English.** And never "audit-ready" — the framework uses "audit-aligned."
4. **No encoding artifacts.** UTF-8, LF line endings (enforced by `.gitattributes`). No mojibake, no smart-quote corruption.
5. **Honest limitations over confident claims.** If your contribution has a known weakness, state it in the text. This framework documents its own limits (Section 15); contributions follow suit.

## The propagation chain (why a rule change is never one file)

Content flows in one direction: **sections → canonical → templates (including the Distilled Rendition) → widget strings.** The standalone section files under `framework/sections/` are the single source of truth; the canonical document is assembled from them, the templates are derived from their model-consumed output blocks, and the widget mirrors the templates.

If you change a rule in a section, your PR should either carry the downstream updates or explicitly note which downstream artifacts now need regeneration. A rule that exists only in one layer is a fork, and forks are how integrity frameworks rot.

Also update per change:
- The section's **Version/Change-from header** (sections carry draft numbers).
- The section's **Validation Criteria** if the rule is testable (append new test IDs; never renumber existing ones).
- `framework/manifest.json` if a counted statistic changed (re-run the deterministic census rather than editing the number by hand).
- `CHANGELOG.md` for anything behavior-changing (SemVer policy: breaking = changes what the framework blocks or permits for an unchanged configuration).

## Process

1. Fork, branch, make the change per the rules above.
2. PR description states: what changed, why, the primary sources for any factual claims, and which downstream artifacts were updated or need regeneration.
3. Expect an adversarial review — reviewers will try to refute the change before accepting it. That is the house style, not hostility.

## Licensing of contributions

Framework, guides, and documentation contributions are accepted under **CC-BY-SA 4.0**; widget code contributions under **Apache 2.0** (see `LICENSE`). By submitting a PR you agree your contribution is licensed accordingly.

## Questions

Open an issue, or contact opensource@techjacksolutions.com.
