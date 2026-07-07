# GAIO Platform Setup Guides: Quick Reference

**GAIO v2.0 (draft) — Guardrail Architecture for Informed Output**
**Created by Tech Jacks Solutions**

---

## Which Guide Do I Need?

| I use... | Guide | Setup Time | What fits (measured; verify your field at deploy) |
|----------|-------|------------|------------------------|
| **Claude** (claude.ai) | Claude Projects Guide | ~3 minutes | Any weight (no field limit documented) |
| **ChatGPT** (personal Custom Instructions) | ChatGPT Guide, Option A | ~2 minutes | **Integrity Excerpt only** (1,500-char boxes; no GAIO deployment fits) |
| **ChatGPT** (team, Custom GPT) | ChatGPT Guide, Option B | ~5 minutes | **Micro** (~7,800–7,950 chars vs the ~8,000-char Instructions field, a tight fit; uncheck the tag reserve) |
| **Microsoft Copilot Studio / M365 Copilot agents** | FAQ § Instruction-Field Limits + widget platform-fit | ~5 minutes | **Micro via the instructions-only recipe** (~7,800 chars vs the verified 8,000/field: no embedded tag, nothing else in the field, ALL topic prompts empty. An undocumented ~5,300 combined budget may still reject it; run the truncation check). If rejected: **Integrity Excerpt** (the combined-safe ~5,000 budget is below the Micro floor of 6,966). Never offload instructions to knowledge files on Microsoft surfaces |
| **Gemini** | Gemini Gems Guide | ~3 minutes | Any weight reported to fit (no documented limit. Verify; use the widget's Custom limit if the field rejects) |
| **API** (any provider) | API & Open-Source Guide | ~10 minutes | Any weight (context-window bounded). Use prompt caching |
| **Local models** (Ollama, LM Studio) | API & Open-Source Guide | ~10 minutes | Any weight |

**Use the widget's deployment-target picker and size meter.** It measures your generated config against the surface's usable budget and blocks over-budget output instead of letting the platform silently truncate it (silent truncation = silent rule loss). After deploying to any field-limited surface: confirm the `# End of GAIO Configuration` tail marker survived and ask the assistant to state its loaded domain and mode.

**Weight and mode are independent in v2.** Weight (Full ~8,050 / Standard ~6,800 / Compact ~5,750–6,000 / Micro ~1,950 tokens, measured post-compression) is a token-size choice; enforcement mode is a posture choice, and Compact is available in Mode A (full enforcement, compressed). Mode B (Integrity Lock) keeps every anti-fabrication rule (including omission integrity, which never relaxes) but makes scope and escalation advisory; it is a deliberate solo-use posture, inappropriate for audience-facing or regulated deployments, and the widget requires explicit confirmation (and refuses it for regulated multi-user configurations).

---

## Universal Setup Flow

Regardless of platform, the process is always:

1. **Generate** your GAIO config from the widget (techjacksolutions.com)
2. **Paste** it into your platform's system prompt / instructions field
3. **Test** with four quick checks:
   - Factual question in your domain (should cite appropriate sources)
   - Out-of-scope question (should flag scope boundaries)
   - Fabrication request (should refuse)
   - "I don't know" scenario (should admit uncertainty)
4. **Share** with your team if applicable

---

## Platform Comparison

| Feature | Claude Projects | ChatGPT Custom GPTs | Gemini Gems | API |
|---------|----------------|--------------------:|-------------|-----|
| Auto-loads every conversation | Yes | Yes | Yes | Yes (code-level) |
| Shareable with team | Yes (Pro/Team) | Yes (link) | Workspace only | N/A |
| Upload reference docs | Yes | Yes | In conversation | N/A |
| Web search compatible | Yes | Yes (toggle) | Yes | Depends on model |
| Character limit concern | No | Yes (Custom Instructions only) | Check per-version | No |
| Thinking mode required | No | No | **Yes** | Model-dependent |

---

## Platform Compatibility Matrix

| Platform / Mode | GAIO Compliance | Confidence |
|----------------|-----------------|------------|
| Claude (Sonnet/Opus) | Compliant | High (primary dev platform) |
| ChatGPT (GPT-4o) | Expected compliant | Medium (testing in progress) |
| Gemini (Thinking Mode) | Compliant | Verified |
| Gemini (Fast Mode) | **Non-compliant** | Verified (bypasses rules) |
| Local models (Llama, Mixtral) | Variable | Untested |

**Key finding:** GAIO compliance is mode-dependent, not just model-dependent. Speed-optimized inference modes may bypass system prompt instructions. Always use the most capable reasoning mode available when guardrail compliance matters.

---

## Guides in This Set

1. `GAIO_Setup_Guide_Claude_Projects.md`: Claude Projects setup with tips for Project Knowledge integration
2. `GAIO_Setup_Guide_ChatGPT.md`: Custom Instructions (personal) and Custom GPTs (team), including multi-GPT team deployment
3. `GAIO_Setup_Guide_Gemini.md`: Gemini Gems setup with critical Thinking Mode vs. Fast Mode compatibility notes
4. `GAIO_Setup_Guide_API_OpenSource.md`: API integration (Anthropic, OpenAI, Google), local models (Ollama, LM Studio, vLLM), automation patterns, and gateway/proxy deployment

---

*GAIO v2.0 (draft) | Created and maintained by Tech Jacks Solutions*
*Standard licensed under CC-BY-SA 4.0 | Widget licensed under Apache 2.0*
