# GAIO Platform Setup Guides — Quick Reference

**GAIO v1.0 — Guardrail Architecture for Informed Output**
**Created by Tech Jacks Solutions**

---

## Which Guide Do I Need?

| I use... | Guide | Setup Time | Config Weight Supported |
|----------|-------|------------|------------------------|
| **Claude** (claude.ai) | Claude Projects Guide | ~3 minutes | Full, Standard, Compact |
| **ChatGPT** (personal) | ChatGPT Guide — Option A | ~2 minutes | Compact only (~1,500 char limit) |
| **ChatGPT** (team) | ChatGPT Guide — Option B (Custom GPT) | ~5 minutes | Full, Standard, Compact |
| **Gemini** | Gemini Gems Guide | ~3 minutes | Full, Standard, Compact |
| **API** (any provider) | API & Open-Source Guide | ~10 minutes | Full, Standard, Compact |
| **Local models** (Ollama, LM Studio) | API & Open-Source Guide | ~10 minutes | Full, Standard, Compact |

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
| Gemini — Thinking Mode | Compliant | Verified |
| Gemini — Fast Mode | **Non-compliant** | Verified (bypasses rules) |
| Local models (Llama, Mixtral) | Variable | Untested |

**Key finding:** GAIO compliance is mode-dependent, not just model-dependent. Speed-optimized inference modes may bypass system prompt instructions. Always use the most capable reasoning mode available when guardrail compliance matters.

---

## Guides in This Set

1. `GAIO_Setup_Guide_Claude_Projects.md` — Claude Projects setup with tips for Project Knowledge integration
2. `GAIO_Setup_Guide_ChatGPT.md` — Custom Instructions (personal) and Custom GPTs (team), including multi-GPT team deployment
3. `GAIO_Setup_Guide_Gemini.md` — Gemini Gems setup with critical Thinking Mode vs. Fast Mode compatibility notes
4. `GAIO_Setup_Guide_API_OpenSource.md` — API integration (Anthropic, OpenAI, Google), local models (Ollama, LM Studio, vLLM), automation patterns, and gateway/proxy deployment

---

*GAIO v1.0 — Created and maintained by Tech Jacks Solutions*
*Standard licensed under CC-BY-SA 4.0 | Widget licensed under Apache 2.0*
