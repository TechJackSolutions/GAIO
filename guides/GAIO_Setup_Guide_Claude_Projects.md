# How to Use GAIO with Claude Projects

**GAIO v1.0 — Platform Setup Guide**
**Created by Tech Jacks Solutions**

---

## What This Guide Covers

This guide walks you through setting up GAIO in a Claude Project so that every conversation in that project automatically inherits your guardrail configuration. No re-pasting. No per-session setup.

---

## What You Need

- A Claude Pro, Team, or Enterprise account (Projects are not available on the free tier)
- Your GAIO configuration (generated from the widget at techjacksolutions.com or copied from the GitHub repository)

---

## Setup Steps

### Step 1: Generate Your GAIO Configuration

Go to the GAIO widget and complete the 6-step setup:

1. Define your purpose and select your primary domain
2. Choose sub-domain specialization (optional)
3. Set authority level and enforcement mode
4. Configure source types and URL policy
5. Review auto-populated scope and escalation settings
6. Click Generate and copy the output

You now have a block of text — your GAIO configuration. Keep it in your clipboard or save the downloaded .txt file.

### Step 2: Create a New Claude Project

1. Open Claude at claude.ai
2. In the left sidebar, click **Projects**
3. Click **Create Project**
4. Give it a name that reflects the domain (e.g., "Cybersecurity Research — GAIO Protected" or "Marketing Content — Guardrailed")

### Step 3: Add GAIO as Project Instructions

1. Inside your new project, look for the **Project Instructions** field (also called "Custom Instructions" in some versions)
2. Paste your entire GAIO configuration into this field
3. Save

That's it. Every conversation you start inside this project will automatically load your GAIO configuration as the system prompt.

### Step 4: Add Supporting Documents (Optional)

If you have reference materials that the AI should draw from (company policies, style guides, product documentation), you can add them as Project Knowledge files:

1. Click **Add Content** or the upload area in the project
2. Upload your files (PDF, TXT, MD, DOCX supported)
3. These files become available to every conversation in the project

This pairs well with GAIO's source authority configuration — the AI now has both the behavioral rules (from GAIO) and the reference material (from your uploads) in the same workspace.

### Step 5: Test It

Start a new conversation in the project and try these checks:

- Ask a factual question in your domain — does the AI cite appropriate authority types?
- Ask something outside your configured scope — does the AI flag it as out-of-scope?
- Ask it to make something up — does it refuse and explain why?
- Ask a question it genuinely cannot answer — does it say "I don't know" rather than fabricating?

If the AI behaves according to your GAIO configuration, you're set.

---

## Tips for Claude Projects + GAIO

**One project per domain configuration.** If you work across multiple domains (e.g., cybersecurity during the day, content writing in the evening), create separate projects with different GAIO configs rather than trying to use one config for everything.

**Project Instructions have a character limit.** Claude Projects support substantial instruction fields, but if you're using a Full weight GAIO config (~3,500 tokens / ~15,000 characters) alongside other custom instructions, check that everything fits. Compact weight configs (~1,500 tokens) leave more room for additional instructions.

**GAIO + Claude's built-in tools.** Claude Projects support web search, file creation, and other tools. GAIO's URL policy (Option B: Search-verified allowed) pairs naturally with Claude's web search capability — the AI can find and verify URLs in real time, which is exactly what Option B is designed for.

**Updating your config.** When a new version of GAIO is released or you want to change your domain settings, just regenerate your config from the widget and replace the Project Instructions text. All future conversations in the project will use the new config. Existing conversations keep whatever config was active when they started.

---

## Troubleshooting

**The AI doesn't seem to follow the GAIO rules.**
- Verify the config was pasted into **Project Instructions**, not into a regular chat message
- Start a **new conversation** within the project (existing conversations may not pick up instruction changes)
- Check that you're inside the correct project (the project name appears at the top of the conversation)

**The config seems too long / gets cut off.**
- Use Compact weight (Mode B) if you need a shorter config
- Remove any trailing whitespace or formatting artifacts from the paste

**The AI references GAIO rules explicitly in its responses.**
- This is normal behavior in Full Enforcement mode — the AI may cite its own rules when declining requests or flagging scope boundaries
- If you prefer less visible rule-citing, Integrity Lock mode (Mode B) is less explicit about operational rules

---

*GAIO v1.0 — Created and maintained by Tech Jacks Solutions*
*Standard licensed under CC-BY-SA 4.0 | Widget licensed under Apache 2.0*
