# How to Use GAIO with Google Gemini

**GAIO v1.0 — Platform Setup Guide**
**Created by Tech Jacks Solutions**

---

## What This Guide Covers

This guide shows you how to set up GAIO in Google Gemini using Gems (custom AI personas). It also covers an important compatibility finding about Gemini's inference modes.

---

## What You Need

- A Google One AI Premium or Gemini Advanced subscription (Gems require a paid tier)
- Your GAIO configuration (generated from the widget at techjacksolutions.com or copied from the GitHub repository)

---

## Critical Compatibility Note

**Not all Gemini modes comply with GAIO equally.**

During testing, we found:

| Gemini Mode | GAIO Compliance |
|-------------|-----------------|
| **Thinking Mode (Deep Think)** | Compliant — follows GAIO framework rules |
| **Fast / Speed Mode** | Non-compliant — bypasses GAIO requirements entirely |

Speed-optimized inference modes deprioritize system prompt instruction following. If you're using GAIO with Gemini, **always use Thinking Mode** for sessions where guardrail compliance matters. This isn't a Gemini-specific flaw — it's a pattern we expect to see across platforms that offer speed/quality tradeoffs.

---

## Setup Steps

### Step 1: Generate Your GAIO Configuration

Complete the widget's 6-step setup, click Generate, and copy the full output.

### Step 2: Create a Gem

1. Open Gemini at gemini.google.com
2. In the left sidebar, click **Gem Manager** (or navigate to Settings → Gems)
3. Click **Create Gem** (or **New Gem**)
4. You'll see a configuration screen with fields for the Gem's behavior

### Step 3: Configure the Gem

**Name:** Choose a name that reflects the domain:
- "SecOps Advisor — Guardrailed"
- "Healthcare Research (GAIO)"
- "Legal Assistant — GAIO v1.0"

**Instructions:** Paste your **entire GAIO configuration** into the instructions field. This is where the behavioral rules live.

At the top of your pasted config, consider adding this line to address the mode compatibility issue:

```
IMPORTANT: This configuration requires Thinking Mode (Deep Think) for reliable compliance. Speed/Fast mode may bypass these instructions.
```

### Step 4: Save and Select Thinking Mode

1. Save your Gem
2. Start a conversation with the Gem
3. Before sending your first message, **verify you are in Thinking Mode** (not Fast/Speed mode)
4. Look for the model selector — it may appear as a dropdown near the input field or in conversation settings

### Step 5: Test It

Run the standard verification checks:

- Ask a factual question in your domain — does the AI cite appropriate sources?
- Ask something outside your configured scope — does it flag scope boundaries?
- Ask it to fabricate — does it refuse?
- Ask something it cannot answer — does it admit uncertainty rather than guessing?

If using Fast/Speed mode, repeat the same tests and compare results. This will confirm whether the mode distinction matters for your specific configuration.

---

## Sharing Gems with a Team

Gem sharing depends on your Google Workspace configuration:

- **Google Workspace (Business/Enterprise):** Gems can be shared within your organization. Create domain-specific Gems and share them with relevant teams.
- **Personal Google accounts:** Gems are currently personal only. Each team member would need to create their own Gem with the same GAIO config. Share the config text (or the widget link with pre-selected settings) so everyone generates the same output.

For team deployment where individual Gem creation isn't practical, consider the API integration path instead (see the API Setup Guide).

---

## Tips for Gemini Gems + GAIO

**Context window advantage.** Gemini models offer very large context windows (1M+ tokens). GAIO configurations consume less than 0.4% of available context even at Full weight. Long research sessions with extensive back-and-forth will run well within limits.

**Gemini's grounding with Google Search.** Gemini can ground responses using Google Search. This pairs naturally with GAIO's URL Policy Option B (Search-verified allowed). When Gemini retrieves and cites web sources, GAIO's source authority rules still apply — the AI should prioritize sources that match your configured authority tiers.

**File uploads.** Gemini supports uploading documents, images, and other files within conversations. Upload reference materials alongside your GAIO-configured Gem to give the AI both behavioral rules and domain-specific source material.

**Re-anchoring in long sessions.** Gemini's large context window enables very long conversations, which is exactly where drift becomes a concern. GAIO's drift prevention (Section 9) is designed for this — the re-anchoring protocol triggers at configured intervals to prevent validation gate degradation. Monitor whether Gemini maintains compliance through extended sessions.

---

## Troubleshooting

**The Gem doesn't follow GAIO rules from the start.**
- Check that you're in Thinking Mode, not Fast/Speed mode
- Verify the full config was pasted (not truncated)
- Start a fresh conversation — Gems apply instructions at conversation start

**Behavior degrades after many messages.**
- This is drift. GAIO's re-anchoring should catch it, but if the model's compliance with re-anchoring instructions also degrades, start a new conversation
- Consider noting the approximate message count where drift began — this data is useful for refining drift check intervals

**The Gem works differently than the same config in Claude or ChatGPT.**
- Expected. Each model interprets system prompt instructions differently. The GAIO framework is model-agnostic in design, but compliance levels vary by platform. Document differences you observe — this contributes to the platform compatibility matrix.

**Instructions field has a character limit.**
- If Gemini's Gem instructions field truncates your Full weight config, use Standard or Compact weight. Compact configs are designed specifically for platforms with tighter limits.

---

*GAIO v1.0 — Created and maintained by Tech Jacks Solutions*
*Standard licensed under CC-BY-SA 4.0 | Widget licensed under Apache 2.0*
