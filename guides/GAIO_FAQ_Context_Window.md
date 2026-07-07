# FAQ: Does GAIO Use Up My Context Window?

**Short answer:** No. A full GAIO configuration uses well under 10% of any modern AI platform's context window. It typically *saves* more context than it costs by reducing wasted back-and-forth over the course of a session.

---

## The Numbers

A GAIO v2 configuration ranges from roughly 1,950 (Micro) to 8,050 (Full) tokens depending on your settings. These are **measured** figures (generated output from the v2 widget, sized with a characters/4 heuristic on 2026-07-06), replacing earlier estimates that did not match the shipped generator. Here's how they compare to current platform limits:

| Configuration Weight | Measured Tokens (approx.) | 200K window | 128K window | 1M+ window |
|---------------------|--------------------------|-------------|-------------|------------|
| **Full** (Mode A) | ~8,050 | 4.0% | 6.3% | < 0.9% |
| **Standard** (Mode A) | ~6,800 | 3.4% | 5.3% | < 0.7% |
| **Compact** (Mode A) | ~5,750 | 2.9% | 4.5% | < 0.6% |
| **Compact** (Mode B / Integrity Lock) | ~6,000 | 3.0% | 4.7% | < 0.6% |
| **Micro** (kernel form, either mode) | ~1,950–1,990 (≈7,800–7,950 characters) | ~1.0% | ~1.6% | < 0.2% |

In v2, **weight (token size) and enforcement mode (posture) are independent choices.** Compact and Micro are available in Mode A with the full integrity rule set. The widget recommends a weight for your domain; you can adjust it. Every weight tier carries every Tier 1 integrity rule class; anything omitted for size is disclosed on the configuration header's `# Weight Omissions:` line (Full/Standard/Compact: none; Micro: five declared Tier 2 detail groups, listed in the Distilled Rendition template, and further groups only via the published budget-fit drop order).

---

## Why GAIO Saves More Than It Costs

Without behavioral guardrails, AI sessions accumulate waste. Common patterns include:

- **Fabrication corrections:** "That URL doesn't exist." "Where did you get that statistic?" Each correction cycle costs 200–500 tokens of your prompt plus the wasted response, and produces nothing useful.
- **Scope drift re-anchoring:** "Let's get back to the actual topic." The model wanders, you pull it back, tokens spent on both sides.
- **Repeated instructions:** "Remember, I need sources for any claims." Said once, twice, three times in a session because the model doesn't retain behavioral expectations without explicit structure.
- **Verbose hedging:** Without clear rules about how to handle uncertainty, models pad responses with excessive qualifiers and disclaimers instead of being direct about what they know and don't know.

Each of these patterns burns tokens without advancing your work. Two or three fabrication correction loops in a single session can consume more tokens than the entire GAIO configuration.

**The math:** An ~8,050-token GAIO configuration that prevents a handful of correction cycles (roughly 1,000–2,000 wasted tokens each) pays for itself over a working session. On API deployments, prompt caching makes the recurring cost of the config prefix a small fraction of its first-call cost (see the API setup guide). The longer the conversation, the greater the savings, which is exactly where GAIO's drift prevention keeps working in the background.

---

## What About Shorter Context Windows?

If you're using a platform or model tier with a smaller context window (16K–32K tokens), GAIO's Compact weight tier fits at roughly 5,750–6,000 tokens (a meaningful but workable share of a 16K window at ~36%, and a comfortable one at 32K at ~18%), and Micro (~1,950 tokens) fits anywhere. For platform instruction *fields* with hard character limits, use the **Micro tier and the widget's platform-fit system** (below) rather than truncating a larger configuration. A truncated config silently drops rules, which is exactly the failure the Weight Omissions disclosure exists to prevent.

---

## Instruction-Field Limits by Platform (verified 2026-07-06, re-check at deploy; platform limits change without notice)

| Surface | Documented limit | What fits | Notes |
|---|---|---|---|
| API system prompts (Anthropic / OpenAI / Google) · Claude Projects | Context-window bounded (no field limit) | Any weight | Preferred surfaces; use prompt caching |
| Google Gemini Gems | No documented limit | Any weight (verify your field) | Google publishes no instruction limit. If the field rejects your config, use the widget's Custom limit option |
| ChatGPT Custom GPTs · Microsoft 365 Copilot agent builder | 8,000 characters | **Micro** (~7,800–7,950 chars) | Custom GPT limit is community-confirmed, not officially documented. On Microsoft surfaces, do NOT offload instructions into knowledge files. Injection classifiers may sanitize directive-like knowledge at runtime |
| Microsoft Copilot Studio (agent Instructions) | 8,000 characters per field, **but** an undocumented *combined* budget across agent + topic + system instructions fails around ~5,300 characters observed | **Two paths.** (1) *Instructions-only recipe:* Micro (~7,800 chars) fits the verified per-field 8,000 IF the tag is kept in your records rather than embedded, nothing else shares the field, and ALL topic-level prompts stay empty. The undocumented combined budget may still reject it at runtime, so run the truncation check after saving. (2) *Conservative:* the combined-safe budget (~5,000) is below the GAIO Micro floor (6,966), so Integrity Excerpt only | Same knowledge-file caution as above |
| ChatGPT Custom Instructions | 1,500 characters per box | **Integrity Excerpt only** (no GAIO deployment fits) | The Excerpt is a behavioral nudge, explicitly not a GAIO deployment (no tag, no mode, no enforcement label). Never split a config across the two boxes |

**How the fit system works:** the widget's deployment-target picker + live size meter measure your generated config against the surface's usable budget (with reserve for the tag block and your own additions) and **block over-budget output** instead of letting a platform field silently cut it. When Micro is still too large for a budget, whole optional rule groups are removed in the framework's published drop order (each removal disclosed on the `# Weight Omissions:` line), never by cutting text mid-rule. If a budget can't hold even the integrity core in kernel form, that surface can't hold GAIO; the widget offers only the Excerpt, honestly labeled.

**After deploying to any field-limited surface, run the truncation check:** confirm the final line `# End of GAIO Configuration` survived in the saved field, and ask the assistant to state its loaded domain and mode. A truncated config typically loses its tail.

**Micro honesty note:** Micro renders every rule in kernel form: same rules, less instructional reinforcement. Adherence on kernel form is untested until a Micro compatibility round runs; for high-stakes deployments prefer a fuller weight on a surface that fits it.

**Mode still matters at Compact size.** As of v2, Compact is available in both modes. Compact-Mode-A keeps scope and escalation enforced; Compact-Mode-B (Integrity Lock) keeps every anti-fabrication integrity rule (including omission integrity, which never relaxes) but makes scope boundaries and escalation triggers **advisory**. Mode B remains inappropriate for audience-facing or regulated deployments; the widget requires explicit confirmation before generating it, and refuses it outright for regulated multi-user configurations.

---

## Do I Need to Read or Understand the Configuration?

No. The GAIO widget generates your configuration behind a button click. You paste it into your AI platform's system prompt or custom instructions field. You don't need to read, edit, or understand the output unless you want to. The configuration is designed for the AI to parse, not for you to study.

---

*GAIO v2.0 (draft) | Created and maintained by Tech Jacks Solutions*
*Licensed under CC-BY-SA 4.0*
