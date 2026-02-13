# GAIO — Guardrail Architecture for Informed Output

An open, modular standard for making AI outputs more accurate, consistent, and trustworthy.

GAIO gives AI systems a structured set of rules about what they can say, where their information comes from, how they handle uncertainty, and when they should stop and tell the user to consult a human. It works with any platform that accepts text instructions — ChatGPT, Claude, Gemini, open-source models, or API deployments.

**Created and maintained by [Tech Jacks Solutions](https://techjacksolutions.com)**

---

## The Problem

AI models fabricate. They invent statistics, generate fake URLs, cite nonexistent studies, and present speculation as fact. They do this confidently and consistently.

Existing solutions are either too technical for most users (prompt engineering documentation), too vague to be actionable ("be careful with AI"), or locked inside specific platforms. There is no open standard that a non-technical user can pick up, configure in five minutes, and paste into their AI platform to meaningfully reduce these problems.

That's what GAIO creates.

---

## Who It's For

**Non-technical users** (primary audience): People who use AI tools at work but don't write prompts professionally. Configure through the [HTML widget](widget/GAIO_Widget_v1_0.html) — answer a few questions, copy the output, paste it into your AI platform.

**Technical users and prompt engineers**: Customize the framework directly from the [markdown documentation](framework/). Fork, modify, and integrate into your own workflows.

**Developers**: Integrate guardrails into applications and pipelines. (YAML/JSON configuration format planned for a future release.)

---

## Quick Start

### Option 1: Use the Widget (Recommended)

1. Open the [GAIO Widget on techjacksolutions.com](https://techjacksolutions.com/prompt-engineering-library/) (or use the [local copy](widget/GAIO_Widget_v1_0.html) in this repo)
2. Answer 6-7 questions about your use case (domain, sources, scope, enforcement mode)
3. Click Generate
4. Copy the output and paste it into your AI platform's system prompt, custom instructions, or project settings

Setup guides for specific platforms:
- [Claude Projects](guides/GAIO_Setup_Guide_Claude_Projects.md)
- [ChatGPT](guides/GAIO_Setup_Guide_ChatGPT.md)
- [Gemini](guides/GAIO_Setup_Guide_Gemini.md)
- [API / Open-Source Models](guides/GAIO_Setup_Guide_API_OpenSource.md)
- [Quick Reference (all platforms)](guides/GAIO_Platform_Setup_Quick_Reference.md)

### Option 2: Use the Markdown Directly

Browse the [framework sections](framework/sections/) and the [canonical document](framework/canonical/GAIO_Canonical_v1_0.md). Customize for your needs.

---

## How It Works

GAIO uses a two-layer architecture:

**Layer 1 (What you see):** Plain language questions with sensible defaults. The basic setup is 6-7 questions. Advanced options are hidden until you need them.

**Layer 2 (What the AI sees):** Structured, hierarchical rules optimized for LLM parsing. Generated automatically from your answers. You never have to read or understand this layer unless you choose to.

The widget bridges the two layers. You answer questions → the widget generates a configuration → you paste it into your AI platform. Done.

### What the Configuration Controls

| Section | What It Does |
|---------|-------------|
| Core Directive | Sets the AI's mission, decision hierarchy, and persistence rules |
| Scope Definition | Defines the domain, approved sources, topic boundaries, and URL policy |
| Violation Hierarchy | Classifies violations into Critical (zero tolerance), Major (avoid always), and Minor (minimize) |
| Required Behaviors | Templates for 7 scenarios: when the AI knows, partially knows, doesn't know, is asked to fabricate, needs to flag a hypothetical, encounters a wrong premise, or should defer to a human |
| Escalation Protocol | Triggers and routing for "this needs human review" situations |
| Pre-Response Validation | Three-gate check the AI runs before every response, aligned to violation severity |
| Edge Case Handling | Cross-cutting edge cases + an extensibility framework for community contributions |
| Domain Configuration | 38 sub-domain profiles across 9 domains that auto-populate sources, triggers, and scope |
| Drift Prevention | Detects and corrects validation degradation over long conversations |
| Session Persistence | Separates integrity rules (always enforced) from operational rules (configurable by use case) |
| Implementation Priority | Resolves conflicts when framework rules contradict each other |
| Evaluation Hooks | ~152 validation tests with a 28-test minimum viable set |

### Enforcement Modes

**Full Enforcement (Mode A):** All rules enforced. Designed for organizational deployments, regulated industries, and professional use cases where scope should never relax.

**Integrity Lock (Mode B):** Anti-fabrication protections fully enforced. Scope and escalation rules shift from mandatory to advisory. Designed for individual users and creative professionals who need accuracy without rigidity.

### Configuration Scale

The widget supports 9 parent domains, 38 sub-domain profiles (multi-select, up to 3 per domain), primary + secondary domain combinations, 3 authority levels, 2 enforcement modes, 3 URL policies, and configurable scope, sources, and escalation routing. This produces an estimated 707,000+ unique configurations before manual edits.

---

## Design Principles

1. **Non-technical users come first.** Every feature must pass: "Would a marketing manager understand this without help?" If not, it needs simplification or progressive disclosure.

2. **One action, multiple outputs.** Selecting a domain auto-populates sources, escalation triggers, and scope. Selecting a sub-domain refines all three. The user makes choices; the system does the cascading work.

3. **Integrity over helpfulness.** The standard's own core directive applies to the standard itself. We don't fabricate capabilities or promise more than the framework can deliver.

4. **Model-agnostic always.** No feature assumes a specific AI platform. The output is text. It works anywhere that accepts text instructions.

5. **Testable.** Every section includes validation criteria. If you can't test whether a guardrail works, the guardrail doesn't work.

6. **Open and forkable.** The standard is meant to be adopted, modified, and extended — with mandatory credit to Tech Jacks Solutions.

---

## Platform Compatibility

GAIO compliance is mode-dependent, not just model-dependent.

| Platform | Compliance | Notes |
|----------|------------|-------|
| Claude 4.5 Sonnet | ✔ Strongest | Zero drift, caught all social engineering attempts |
| ChatGPT 5.2 | ✔ Strong | Zero drift, strong scope enforcement |
| Gemini (Thinking Mode) | ✔ Compliant | Aligned correctly |
| Gemini (Fast Thinking) | ✘ Failed | Bypassed requirements under pressure |

Speed-optimized inference modes may deprioritize system prompt instruction following even on capable models. See the full [Platform Compatibility Report](docs/platform-compatibility-report.md) for details.

---

## Repository Structure

```
GAIO/
├── README.md
├── LICENSE-CODE                        # Apache 2.0 (widget)
├── LICENSE-CONTENT                     # CC-BY-SA 4.0 (framework, guides)
│
├── framework/
│   ├── canonical/
│   │   └── GAIO_Canonical_v1_0.md      # Complete standard (~3,750 lines)
│   ├── sections/
│   │   ├── 01-core-directive.md        # Individual section files
│   │   ├── 02-scope-definition.md
│   │   └── ...through 12
│   └── templates/
│       ├── GAIO_Integrated_Block_Template_v1_0.md
│       └── GAIO_Modular_Section_Output_v1_0.md
│
├── guides/
│   ├── GAIO_Setup_Guide_Claude_Projects.md
│   ├── GAIO_Setup_Guide_ChatGPT.md
│   ├── GAIO_Setup_Guide_Gemini.md
│   ├── GAIO_Setup_Guide_API_OpenSource.md
│   ├── GAIO_Platform_Setup_Quick_Reference.md
│   └── GAIO_FAQ_Context_Window.md
│
├── widget/
│   └── GAIO_Widget_v1_0.html           # Single-file widget (~1,890 lines)
│
└── docs/
    └── platform-compatibility-report.md
```

---

## Versioning

Repository releases (e.g., v0.9.0) represent the overall framework version. Individual sections carry their own draft numbers (e.g., Draft 1.3) reflecting internal revision history. The repository release version is the authoritative reference for compatibility and citation.

This project uses [Semantic Versioning](https://semver.org/). GAIO is currently in pre-release (v0.x.x), meaning the framework is functional and tested but still undergoing validation and refinement. Expect the interface and structure to stabilize at v1.0.0.

---

## Licensing

This project uses a dual-license structure:

| Content | License | Covers |
|---------|---------|--------|
| Framework, guides, documentation | [CC-BY-SA 4.0](LICENSE-CONTENT) | Everything in `framework/`, `guides/`, and `docs/` |
| Widget (code) | [Apache 2.0](LICENSE-CODE) | Everything in `widget/` |

**In plain terms:**

- **Framework and guides:** Use, modify, and share freely. You must credit Tech Jacks Solutions. Derivatives must use the same license (cannot go proprietary).
- **Widget:** Use for any purpose, including commercial. Includes a patent grant for enterprise adoption. Attribution required in the license file.

---

## Contributing

GAIO is designed for community extension. Section 7 (Edge Case Handling) includes a submission template and intake process for new edge cases. Section 8 (Domain Configuration Profiles) includes a contribution template for new sub-domain profiles.

**How to contribute:**

1. Fork the repository
2. Create a branch for your contribution
3. Follow the relevant submission template (Section 7 for edge cases, Section 8 for domain profiles)
4. Submit a pull request with a clear description of what you're adding and why

All contributions must use verifiable sources only. No fabricated authorities, statistics, or references.

**Report bugs or request features:** [Open an issue](../../issues)

---

## Roadmap

- YAML/JSON machine-readable configuration format
- Community-maintained domain reference sheets (verified source libraries per domain)
- Community-contributed sub-domain profiles and edge cases
- Automated evaluation tooling
- Additional platform integration examples

---

## Contact

**Tech Jacks Solutions**

- Website: [techjacksolutions.com](https://techjacksolutions.com)
- Open-source inquiries: [opensource@techjacksolutions.com](mailto:opensource@techjacksolutions.com)
- LinkedIn: [Tech Jacks Solutions](https://www.linkedin.com/company/tech-jacks-solutions/)
- Bug reports and feature requests: [GitHub Issues](../../issues)

---

*GAIO v0.9.0 — Created and maintained by Tech Jacks Solutions. Framework licensed under CC-BY-SA 4.0. Widget licensed under Apache 2.0.*
