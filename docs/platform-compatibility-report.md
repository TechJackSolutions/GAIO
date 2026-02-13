# GAIO — Platform Compatibility Report

**Version:** 1.0
**Test Date:** February 13, 2026
**Created by:** Tech Jacks Solutions

---

## Overview

GAIO configurations were tested across three major AI platforms using identical prompts and identical configurations. The test sequence evaluated factual accuracy, source authority compliance, scope enforcement, social engineering resistance, and drift behavior over a sustained session.

---

## Test Methodology

**Configuration:** Custom domain (astrophysics), Specialist authority level, Full Enforcement mode, Standard weight, Search-Verified URL policy (Option B).

**Approach:** A 12-prompt sequence progressing from standard factual queries through increasingly aggressive scope expansion attempts, authority override claims, and reframing pressure. All three platforms received identical prompts in identical order.

**Areas evaluated:**
- Factual accuracy and source compliance
- Uncertainty handling
- Simple and complex scope refusals
- Authority override resistance
- Social engineering resistance (using the AI's own words as leverage)
- Drift resistance over the full session

---

## Results

| Test Area | Claude 4.5 Sonnet | ChatGPT 5.2 | Gemini |
|---|---|---|---|
| Factual accuracy | ✅ Pass | ✅ Pass | ✅ Pass |
| Source authority compliance | ✅ Pass | ✅ Pass | ✅ Pass |
| Uncertainty handling | ✅ Pass (strongest) | ✅ Pass | ✅ Pass |
| Simple scope refusal | ✅ Clean | ✅ Clean | ✅ Clean |
| Complex scope refusal | ✅ Clean | ✅ Clean | ⚠️ Refused but reframed |
| Authority override resistance | ✅ Cited persistence rule | ✅ Pass | ✅ Pass |
| Social engineering resistance | ✅ Caught all attempts | ✅ Caught all attempts | ❌ Accepted reframe |
| Drift resistance (full session) | ✅ Zero drift | ✅ Zero drift | ❌ Progressive drift |
| Refusal conciseness | ✅ Best | ⚠️ Sometimes verbose | ❌ Often 400+ words |

---

## Platform Ranking

1. **Claude 4.5 Sonnet** — Strongest overall compliance. Zero drift, caught every reframe attempt, most concise refusals.
2. **ChatGPT 5.2** — Strong compliance. Zero drift, caught reframes. Slightly more verbose in boundary responses.
3. **Gemini** — Strong factual accuracy and initial refusals. Failed under sustained social engineering pressure through rationalized scope drift.

---

## Key Findings

**GAIO compliance is mode-dependent, not just model-dependent.** Gemini in Thinking Mode aligned correctly with GAIO. Gemini in Fast Thinking mode bypassed GAIO requirements entirely. Speed-optimized inference modes may deprioritize system prompt instruction following even on capable models.

**Refusal length correlates inversely with compliance quality.** Shorter, clearer refusals left less room for boundary drift. The platforms with the longest refusal responses showed the most scope creep.

**All platforms narrate configuration on initialization.** None were instructed to do this. This has been addressed in GAIO v1.0 with initialization acknowledgment guidance limiting restatement to 2-3 sentences.

**Social engineering via the AI's own output is an effective attack pattern.** Using the AI's prior redirect language as justification for scope expansion succeeded against one of three platforms. GAIO's Drift Prevention section (Section 9) addresses this through the rationalized drift clause and legitimacy reframing trigger.

---

## Recommendations

- **For regulated or high-risk domains:** Use platforms that demonstrated zero drift (Claude, ChatGPT) with Full Enforcement mode.
- **For Gemini users:** Use Thinking Mode, not Fast Thinking, when GAIO compliance is required.
- **For all platforms:** Verify GAIO compliance with a brief scope enforcement test before deploying in production. A 3-4 prompt sequence (factual query → out-of-scope request → scope expansion pressure → authority override attempt) provides a quick baseline.
- **General:** Test your specific configuration on your specific platform. Model updates can change compliance behavior between versions.

---

## Scope and Limitations

This report reflects a single test round on a single configuration. Results may vary across different domains, authority levels, enforcement modes, and model versions. Platform updates may change compliance behavior at any time. This report will be updated as additional testing rounds are completed.

---

*Created and maintained by Tech Jacks Solutions. Licensed under [CC-BY-SA 4.0](../LICENSE-CONTENT).*
