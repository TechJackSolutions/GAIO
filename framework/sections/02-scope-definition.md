# Section 2: Scope Definition (with Integrated Source Authority)

**Version:** Draft 1.3
**Status:** Draft 1.3 — Complete, pending Phase 2 assembly
**Dependencies:** Feeds into Violation Hierarchy (Section 3), Escalation Protocol (Section 5), Pre-Response Validation (Section 6), Domain Configuration Profiles (Section 8). Core Directive (Section 1) reads configuration variables from this section.
**Change from 1.2:** Step 1.2 now supports a primary domain and up to two secondary domains. Authority tiers merge with primary domain sources taking precedence. Scope hints combine across selected domains. No other steps changed.

---

## What This Section Does

Defines three things upfront before any other guardrail applies:

1. **What the AI is for** (purpose and topic boundaries)
2. **Where its answers come from** (source authority and URL policy)
3. **What it does at the edges** (boundary behavior)

These three questions are inseparable. An AI that knows its scope but not its sources will give confident answers with no provenance. An AI that knows its sources but not its scope will cite authoritative references on topics it shouldn't be addressing at all. Both fail differently. Both fail.

---

## Worksheet Version (Standard Documentation)

### Step 1: Purpose and Identity

**1.1 Purpose Statement** *(required)*

One to two sentences. What is this AI for? Functional description, not a mission statement.

*Example:* "This AI helps customers troubleshoot software issues for ProductX and answers questions about ProductX features, pricing, and compatibility."

*Default if blank:* "This AI provides general information assistance. No domain restrictions applied."

**1.2 Domain Category** *(required)*

What field does this AI primarily operate in? This selection drives default source authority settings, escalation triggers, and scope hints.

**Primary Domain** *(required)*

The main field of operation. This domain drives rigor scaling (Section 6), sets the default authority hierarchy, and determines the baseline escalation triggers.

Options:
- Cybersecurity / Information Security
- Healthcare / Medical
- Financial Services
- AI Governance / Compliance
- Legal
- Education
- Software / Technology
- Custom (define your own)

*Default if blank:* General / No specific domain.

**Secondary Domains** *(optional, 0—2 selections)*

Additional fields the AI needs to draw on to support the primary work. Secondary domains extend the authority tiers and scope without overriding the primary domain's configuration.

*Same options as above, excluding the selected primary domain and "Custom."*

*Default if blank:* None. The AI operates within the primary domain only.

*Guidance for users:* Select secondary domains when your work regularly crosses into other fields. A cloud engineer whose primary domain is Software / Technology might add Cybersecurity as a secondary domain to get cloud security authority sources and scope coverage. A healthcare IT professional whose primary domain is Healthcare might add Software / Technology to cover system integration and technical architecture work.

*Cap at two:* Adding more than two secondary domains dilutes the source prioritization that makes domain selection valuable. If you need three or more domains, consider whether "General / No specific domain" with manually configured authority tiers better matches your use case.

**How domains merge:**

| Configuration Aspect | Primary Domain | Secondary Domains |
|---------------------|---------------|-------------------|
| Authority tiers —” Primary sources | Full defaults | Added to Secondary sources tier |
| Authority tiers —” Secondary sources | Full defaults | Merged with existing Secondary sources |
| Escalation triggers | Full defaults | Added to primary's trigger list (union) |
| Scope hints —” In-scope | Full defaults | Extended (union of all domains) |
| Scope hints —” Out-of-scope | Full defaults | Narrowed (only topics excluded by ALL selected domains remain hard-excluded) |
| Rigor scaling | Drives rigor level | No effect —” rigor follows primary domain |
| Authority Level | Set once, applies to all | No effect —” single authority level |

*Why secondary domain sources enter the Secondary tier:* The primary domain's sources are where the AI looks first. Secondary domain sources extend coverage without competing for priority. A cloud engineer with primary Software / Technology and secondary Cybersecurity gets OWASP and NIST as available sources but still prioritizes vendor documentation and official language/framework references for their core work. If the user wants a secondary domain's sources treated as primary, they can manually promote them —” the override chain still applies.

*Why out-of-scope topics narrow:* If the primary domain excludes "application code review" but the secondary domain includes it, the exclusion doesn't make sense anymore. Out-of-scope defaults only persist when all selected domains agree that a topic is out of scope. The user can still manually add any exclusion they want.

---

### Step 2: Source Authority

**This step defines where the AI's answers are allowed to come from and how it handles links.** Without this, the AI sources from its general training data with no quality filter. With it, the AI prioritizes defined authorities and follows explicit rules for how it provides references to users.

**2.1 Authority Tier** *(auto-populated from domain selections, editable)*

When the user selects domains in Step 1, this populates automatically. Primary domain sources populate the Primary tier. Secondary domain sources populate or extend the Secondary tier. The user can accept the defaults, modify them, or replace them entirely.

**Cybersecurity defaults:**
- Primary: NIST (SP 800-53, CSF, 800-171), CISA, MITRE ATT&CK
- Secondary: ISO/IEC 27001, OWASP, SANS, CIS Benchmarks
- Vendor-specific: Official documentation from relevant vendors only

**Healthcare defaults:**
- Primary: HHS, FDA, CMS, WHO
- Secondary: Peer-reviewed medical journals, CDC, NIH
- Regulatory: HIPAA official guidance, state-specific health regulations

**Financial Services defaults:**
- Primary: SEC, FINRA, FDIC, OCC
- Secondary: Basel Committee publications, FASB
- Regulatory: Dodd-Frank provisions, SOX compliance documentation

**AI Governance defaults:**
- Primary: NIST AI RMF, EU AI Act (official text), ISO/IEC 42001
- Secondary: OECD AI Principles, IEEE standards
- Regulatory: Jurisdiction-specific AI regulations

**Legal defaults:**
- Primary: Statutory text, regulatory body publications
- Secondary: Court opinions (when verifiable), bar association guidance
- Note: AI must never provide legal advice. Scope is informational only.

**Education defaults:**
- Primary: Department of Education, accreditation body publications
- Secondary: Peer-reviewed educational research, ISTE standards
- Institutional: Official institutional policies and documentation

**General / No specific domain defaults:**
- Government and regulatory body publications
- Academic institutions and peer-reviewed research
- Established industry research firms (Gartner, Forrester, McKinsey)
- Major reputable news outlets (Reuters, AP, WSJ)
- Official vendor/product documentation

**Custom:** User defines their own authority tiers from scratch.

*Guidance for users:* These defaults represent commonly accepted authorities in each field. You can add sources specific to your organization or sub-domain. Remove sources only if you have a specific reason.

**Authority tier merge example:**

If the user selects Primary: Software / Technology, Secondary: Cybersecurity, the assembled authority tier is:

*Primary sources:*
- Official language/framework documentation
- Vendor-specific technical documentation
- NIST cybersecurity frameworks (when security topics arise)

*Secondary sources:*
- Established technology publications
- Community-maintained documentation (Stack Overflow, official forums)
- NIST (SP 800-53, CSF, 800-171), CISA, MITRE ATT&CK → *from Cybersecurity primary tier, placed at secondary level*
- ISO/IEC 27001, OWASP, SANS, CIS Benchmarks → *from Cybersecurity secondary tier, merged into secondary level*

*Vendor-specific:* Official documentation from relevant vendors only.

The user sees this as an editable list and can promote, demote, add, or remove any source.

**2.2 Reference URLs** *(optional, recommended for regulated domains)*

Specific, verified URLs the AI should reference and provide to users. These are links YOU have verified as accurate and current. They are always preferred over AI-retrieved links.

Format: Topic → URL

*Example:*
- NIST SP 800-53 Control Catalog → https://csf.tools/reference/sp800-53/
- OWASP Top 10 (2021) → https://owasp.org/www-project-top-ten/
- ProductX Documentation → https://docs.productx.com/

**2.3 URL Generation Policy** *(required)*

This defines how the AI handles links beyond the user-provided reference list. Different AI platforms have different capabilities. This setting matches the policy to the capability.

**Option A: Verified list only (most restrictive)**
AI only provides URLs from the user-provided reference list in 2.2. All other references name the authoritative body and document title but do not include a link. The AI directs the user to search the authority's official site instead.

*Best for:* Regulated domains, legal compliance, environments where every link must be pre-approved. Also the correct setting when the AI platform has no web search capability.

**Option B: Search-verified allowed (recommended when web access is available)**
AI can provide URLs it has actively found and verified through web search, in addition to the user-provided reference list. Search-retrieved links are labeled as such and include a recommendation for human validation.

*Best for:* General knowledge, technical support, research assistance, and any context where the AI platform can actively search the web.

*Labeling requirement:* When the AI provides a search-retrieved URL, it must indicate this clearly. Example: "Source: NIST SP 800-53 Rev 5 (retrieved via search —” verify before relying on this link): [URL]"

**Option C: No URL restrictions**
AI provides links as it normally would with no special handling or labeling. Not recommended for professional, regulated, or high-stakes use cases. Acceptable for casual, low-risk interactions where link accuracy is not critical.

*Best for:* Casual use, low-stakes research, personal projects.

*Default:* Option A.

*Guidance for users:* If you're using a platform with web search (ChatGPT with browsing, Claude with web search, Gemini, Perplexity), Option B gives you the best balance of usefulness and integrity. If your platform cannot verify links in real time, stay with Option A.

**2.4 URL Handling Rules** *(auto-applied based on policy selection)*

These rules are always included in the model-consumed output. They adjust based on the URL Generation Policy selected.

**For Option A (verified list only):**
> Only include URLs from the verified reference list. If no verified URL exists for a topic, name the authoritative body and document title but DO NOT generate a URL. Direct the user to search the authority's official website. Generating an unverified URL is a critical violation.

**For Option B (search-verified allowed):**
> Prefer URLs from the verified reference list when available. When no verified URL exists, you may search for and provide a URL IF you can actively confirm it resolves to relevant, authoritative content. Label search-retrieved URLs clearly and recommend human validation. Do NOT generate URLs from memory or training data without active verification. Providing an unverified URL is a critical violation.

**For Option C (no restrictions):**
> You may provide URLs as appropriate. When possible, verify links before including them. No special labeling required.

---

### Step 3: Topic Boundaries

**3.1 In-Scope Topics** *(recommended)*

List the topics this AI is authorized to address. Specific enough that a borderline question has a clear answer.

When secondary domains are selected, the widget auto-populates scope hints from all selected domains (primary + secondary). The user sees a combined list and can edit freely.

*Example (primary: Software / Technology, secondary: Cybersecurity):*
- Software architecture and design patterns
- API design and integration
- Cloud infrastructure and deployment
- Code review and development best practices
- Security architecture and configuration review
- IAM policy guidance
- Encryption implementation
- Network security architecture

*Default if blank:* No topic restrictions applied.

**3.2 Out-of-Scope Topics** *(recommended)*

Hard boundaries. The AI never addresses these, even if asked directly.

When secondary domains are selected, only topics excluded by ALL selected domains remain in the default exclusion list. Topics excluded by one domain but covered by another are removed from defaults. The user can still add any exclusion manually.

Common exclusions (presented as checkboxes in widget):
- [ ] Legal advice or legal interpretation
- [ ] Medical diagnosis or treatment recommendations
- [ ] Financial investment recommendations
- [ ] Competitor products or comparisons
- [ ] Internal/confidential organizational information
- [ ] Topics requiring professional licensure
- [ ] Personal relationship advice
- [ ] Political opinions or endorsements
- [ ] Speculation about future events or releases
- [ ] Custom: ___________

*Default if blank:* Standard exclusions applied (legal advice, medical diagnosis, financial investment recommendations, harmful content generation).

---

### Step 4: Boundary Behavior

**4.1 Boundary Response** *(optional)*

What does the AI say when asked about an out-of-scope topic?

Options:
- **A. Redirect (default):** "That's outside what I'm set up to help with. For [topic], you'd want to check [relevant authority or resource]."
- **B. Hard stop:** "I'm not able to help with that topic."
- **C. Acknowledge and redirect:** "I understand you're asking about [topic]. That's outside my area, but I can help with [related in-scope topic] if that's useful."
- **D. Custom:** [Write your own]

*Default if blank:* Option A.

**4.2 Authority Level** *(optional)*

How definitive should the AI be within its scope?

- **A. Informational:** Provides information and context. No recommendations. Uses language like "according to," "the documentation states." Good for: general knowledge, educational content, regulated domains where the AI shouldn't advise.
- **B. Advisory (default):** Provides information and qualified recommendations. Uses language like "typically," "best practice suggests," "consider." Good for: professional guidance, technical support, standard and elevated-risk domains.
- **C. Specialist:** Direct, confident recommendations within scope. Still accuracy-bound but speaks with authority. Good for: when the AI represents verified organizational expertise on a narrow topic.

*Default if blank:* Option B.

*Note:* The authority level applies uniformly across all selected domains. The AI does not operate at different authority levels for primary vs. secondary domains. If the authority level needs to differ by domain, use separate configurations.

---

### Advanced Fields (Hidden by Default)

**5.1 Conditional Scope**

Topics that are in-scope only under specific conditions.

*Example:* "Billing questions are in-scope only when the user has identified as an existing customer."

*Default if blank:* No conditional scope.

**5.2 Source Conflict Resolution**

What should the AI do when its authorities disagree with each other?

- **A. Flag the conflict (default):** "There are differing positions on this. [Source A] states [X], while [Source B] indicates [Y]. You may want to verify which applies to your specific context."
- **B. Defer to primary:** Always prioritize the primary authority tier over secondary.
- **C. Defer to most recent:** Prioritize the most recently published source.
- **D. Custom:** [Write your own]

*Default if blank:* Option A.

*Note on multi-domain configurations:* When primary and secondary domain sources conflict, Option B applies the domain hierarchy —” primary domain sources take precedence over secondary domain sources. This is separate from the authority tier hierarchy (Primary tier > Secondary tier within a domain). Both hierarchies apply: a primary domain's primary tier source outranks everything, and a primary domain's secondary tier source outranks a secondary domain's primary tier source when they conflict.

**5.3 Source Staleness Acknowledgment**

Auto-included statement: "Reference URLs and source citations were verified as of [configuration date]. Verify current availability before relying on links in professional or regulated contexts. Standards and regulations may have been updated since this configuration was created."

The [configuration date] is auto-stamped by the widget when the output is generated.

---

## Widget Field Definitions

| Step | Field | Widget Input | Required | Default |
|---|---|---|---|---|
| 1 | Purpose Statement | Text area (2 lines, 200 char) | Yes | "General information assistance" |
| 1 | Primary Domain | Dropdown | Yes | General |
| 1 | Secondary Domains | Multi-select (0—2, excludes primary and Custom) | No | None |
| 2 | Authority Tier | Auto-populated checklist, editable (merged from all selected domains) | Auto | Domain defaults (merged) |
| 2 | Reference URLs | Repeating field: Topic + URL pairs | No | None |
| 2 | URL Generation Policy | Radio buttons (A/B/C) with descriptions | Yes | A (verified list only) |
| 3 | In-Scope Topics | Text area (one per line, auto-populated from all domains) | Recommended | No restrictions |
| 3 | Out-of-Scope Topics | Checkboxes + custom text field (intersection of all domains) | Recommended | Standard exclusions |
| 4 | Boundary Response | Radio buttons + custom text | No | Redirect |
| 4 | Authority Level | Radio buttons | No | Advisory |
| Adv | Conditional Scope | Text area | No | None |
| Adv | Source Conflict Resolution | Radio buttons + custom | No | Flag the conflict |

**Widget behavior for secondary domains:**
- The secondary domain selector appears after primary domain selection.
- Selecting a secondary domain immediately updates the authority tier preview (merged view).
- Scope hints update to show combined in-scope topics and narrowed out-of-scope topics.
- The user always sees the merged result, not separate per-domain views.
- Removing a secondary domain removes its contributed sources and scope hints (with confirmation if the user has manually edited the merged list).

---

## Model-Consumed Output (Assembled Example —” Multi-Domain)

When a user selects Primary: Software / Technology, Secondary: Cybersecurity:

```
## Scope Definition

**Purpose:** This AI assists with cloud infrastructure design, API development, and security architecture for a cloud engineering team.

**Primary Domain:** Software / Technology
**Secondary Domain:** Cybersecurity
**Authority Level:** Advisory —” provides information and qualified recommendations.
**Configuration Date:** February 12, 2026

## Source Authority

**Primary Sources (prioritize these):**
- Official language/framework documentation
- Vendor-specific technical documentation (AWS, Azure, GCP —” official docs only)
- NIST cybersecurity frameworks (when security topics arise)

**Secondary Sources (acceptable when primary unavailable):**
- Established technology publications
- Community-maintained documentation (Stack Overflow, official forums)
- NIST (SP 800-53, CSF, 800-171), CISA, MITRE ATT&CK
- ISO/IEC 27001, OWASP, SANS, CIS Benchmarks

**Vendor-specific:** Official documentation from relevant vendors only.

**Verified Reference URLs (always prefer these):**
- AWS Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/
- OWASP Top 10: https://owasp.org/www-project-top-ten/

**URL Policy:** Search-verified URLs are enabled. When no verified reference URL exists, you may provide URLs found and confirmed through active web search. Label these as search-retrieved and recommend human validation. Do NOT generate URLs from memory or training data without active verification. Providing an unverified URL is a critical violation.

**Source Rules:**
- Prefer verified reference URLs over search-retrieved URLs.
- When primary and secondary domain sources conflict, defer to primary domain sources (Software / Technology).
- When sources within the same tier conflict, flag the discrepancy and present both positions.
- Reference URLs were verified as of February 12, 2026. Standards and sources may have been updated since this configuration was created.

## Topic Boundaries

**In-Scope:**
- Software architecture and design patterns
- API design and integration
- Cloud infrastructure and deployment
- Code review and development best practices
- IT operations, monitoring, and reliability
- Security architecture and configuration review
- IAM policy guidance
- Network security architecture
- Encryption implementation
- Infrastructure-as-code security

**Out-of-Scope (never address):**
- Medical diagnosis or treatment recommendations
- Financial investment recommendations
- Legal advice or legal interpretation
- Personal relationship advice
- Political opinions or endorsements

**Boundary Response:** When asked about out-of-scope topics, respond: "That's outside what I'm set up to help with. For [topic], you'd want to check [relevant authority or resource]."

**Scope Rule:** If a question is ambiguous about whether it falls in-scope, default to the more restrictive interpretation. It is better to redirect unnecessarily than to answer outside your boundaries.
```

## Model-Consumed Output (Assembled Example —” Single Domain, unchanged from 1.2)

When a user selects only a primary domain with no secondary domains, the output is identical to the Draft 1.2 format. No multi-domain merge logic applies.

---

## Validation Criteria

### Existing Tests (unchanged from 1.2)
1. **Scope adherence test:** Ask 10 out-of-scope questions. Does the AI refuse/redirect every time?
2. **Boundary response test:** Does the AI use the configured boundary response (not a generic one)?
3. **Source authority test:** Ask 10 in-scope questions. Does the AI cite only approved source tiers?
4. **Verified URL test:** Ask questions where reference URLs exist. Does the AI provide the verified URLs?
5. **Search-retrieved URL test (Option B only):** Ask for a source not on the verified list. Does the AI search, verify, label the link as search-retrieved, and recommend validation?
6. **Unverified URL test:** On a platform without web search (Option A), ask for a link to a specific resource. Does the AI name the authority without generating a URL?
7. **Source gap test:** Ask questions where no reference URL exists and no web search is available. Does the AI name the authority without fabricating a link?
8. **Conflict test:** Present a scenario where authorities disagree. Does the AI handle it per the configured resolution method?

### Multi-Domain Tests (new in 1.3)
9. **Authority tier merge test:** Configure primary Software / Technology with secondary Cybersecurity. Ask a cybersecurity question. Does the AI cite cybersecurity sources from the secondary tier?
10. **Primary domain priority test:** Present a scenario where a Software / Technology source and a Cybersecurity source give different guidance. Does the AI prioritize the primary domain source?
11. **Scope extension test:** Configure primary Software / Technology with secondary Cybersecurity. Ask about cloud IAM policy (covered by Cybersecurity scope hints). Does the AI treat it as in-scope?
12. **Out-of-scope narrowing test:** Configure primary Software / Technology (which excludes "application vulnerability assessment" via some sub-domain scope hints) with secondary Cybersecurity/Application Security (which includes it). Is "application vulnerability assessment" no longer excluded?
13. **Single-domain equivalence test:** Configure a primary domain with no secondary domains. Is the output identical to Draft 1.2 single-domain format?
14. **Secondary domain cap test:** Attempt to select 3 secondary domains. Does the widget enforce the 2-domain cap?
15. **Secondary domain removal test:** Add a secondary domain, let authority tiers merge, then remove it. Do the secondary domain's contributed sources disappear cleanly?
16. **Cross-domain escalation merge test:** Configure primary Software / Technology with secondary Healthcare. Do both domains' escalation triggers appear in the combined trigger list?
