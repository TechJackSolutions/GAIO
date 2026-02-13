# FAQ: Does GAIO Use Up My Context Window?

**Short answer:** No. A full GAIO configuration uses less than 3% of any modern AI platform's context window — and it typically *saves* more context than it costs by reducing wasted back-and-forth over the course of a session.

---

## The Numbers

A GAIO configuration ranges from roughly 1,500 to 4,000 tokens depending on your settings. Here's how that compares to current platform limits:

| Configuration Weight | Approximate Tokens | Claude (200K) | GPT-4o (128K) | Gemini (1M+) |
|---------------------|-------------------|---------------|---------------|--------------|
| **Full** (Mode A + regulated domain) | ~3,500 | 1.75% | 2.7% | < 0.4% |
| **Standard** (Mode A + standard domain) | ~2,500 | 1.25% | 2.0% | < 0.3% |
| **Compact** (Mode B / Integrity Lock) | ~1,500 | 0.75% | 1.2% | < 0.2% |

Your configuration weight is determined automatically based on your domain and enforcement mode. You don't choose it directly — the widget selects the appropriate level for your use case.

---

## Why GAIO Saves More Than It Costs

Without behavioral guardrails, AI sessions accumulate waste. Common patterns include:

- **Fabrication corrections** — "That URL doesn't exist." "Where did you get that statistic?" Each correction cycle costs 200–500 tokens of your prompt plus the wasted response, and produces nothing useful.
- **Scope drift re-anchoring** — "Let's get back to the actual topic." The model wanders, you pull it back, tokens spent on both sides.
- **Repeated instructions** — "Remember, I need sources for any claims." Said once, twice, three times in a session because the model doesn't retain behavioral expectations without explicit structure.
- **Verbose hedging** — Without clear rules about how to handle uncertainty, models pad responses with excessive qualifiers and disclaimers instead of being direct about what they know and don't know.

Each of these patterns burns tokens without advancing your work. Two or three fabrication correction loops in a single session can consume more tokens than the entire GAIO configuration.

**The math:** A 3,500-token GAIO configuration that prevents just two correction cycles (roughly 1,000–2,000 wasted tokens each) pays for itself before your session is halfway through. The longer the conversation, the greater the savings — which is exactly where GAIO's drift prevention keeps working in the background.

---

## What About Shorter Context Windows?

If you're using a platform or model tier with a smaller context window (16K–32K tokens), GAIO's Compact weight tier is designed for you. At roughly 1,500 tokens, it preserves all core anti-fabrication protections while minimizing configuration size. The Compact tier keeps every integrity rule (no fabrication, source verification, uncertainty disclosure) fully intact — it only compresses operational rules like detailed scope enforcement and escalation formatting.

---

## Do I Need to Read or Understand the Configuration?

No. The GAIO widget generates your configuration behind a button click. You paste it into your AI platform's system prompt or custom instructions field. You don't need to read, edit, or understand the output unless you want to. The configuration is optimized for the AI to parse, not for you to study.

---

*GAIO v1.0 — Created and maintained by Tech Jacks Solutions*
*Licensed under CC-BY-SA 4.0*
