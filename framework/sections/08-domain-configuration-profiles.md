# Section 8: Domain Configuration Profiles

**Version:** Draft 1.2
**Status:** Draft 1.2 — Complete, pending Phase 2 assembly
**Dependencies:** Reads from Scope Definition (domain selections —” primary and secondary, authority tiers). Feeds refined defaults into Scope Definition (authority tiers), Escalation Protocol (domain-specific triggers), and Pre-Response Validation (rigor scaling).
**Change from 1.1:** Sub-domain picker now shows options for all selected domains (primary and secondary). Override chain updated to include domain-level hierarchy. Widget field definitions and model-consumed output updated. Sub-domain profile content unchanged.

---

## What This Section Does

Section 2 asks the user to pick a primary domain and optionally up to two secondary domains. Those selections auto-populate broad defaults for source authority, escalation triggers, and scope hints. Those defaults are intentionally general. "Cybersecurity" covers SOC analysts, GRC teams, penetration testers, cloud architects, and application security engineers. The authority tiers that work for all of them are too loose to be optimal for any of them.

This section adds a second-level selection: the sub-domain specialization. It narrows the defaults without adding complexity. The user picks from a short list —” for each selected domain. Everything downstream gets tighter. If they skip the pick, the parent domain defaults apply unchanged.

---

## How It Works

The sub-domain picker is optional. It appears after the domain selection in Section 2 and before source authority configuration. When secondary domains are selected, the picker shows sub-domain options for each selected domain.

**Flow:**

1. User selects primary domain (Section 2, Step 1.2) → primary domain defaults populate
2. User optionally selects secondary domains (Section 2, Step 1.2) → secondary domain defaults merge per Section 2 rules
3. Widget presents sub-domain options for the primary domain
4. If secondary domains are selected, widget presents sub-domain options for each secondary domain (in separate, labeled groups)
5. User picks sub-domains (any, all, or none) → refined defaults replace parent defaults for each domain where a sub-domain was selected
6. User skips the pick or selects "General / No specialization" for any domain → that domain's parent defaults remain
7. User can still manually edit any auto-populated field regardless of selections

**The override chain:** Most specific wins, with domain hierarchy preserved.

1. **Manual user edits** override everything.
2. **Primary domain sub-domain defaults** override primary domain parent defaults.
3. **Secondary domain sub-domain defaults** override secondary domain parent defaults.
4. **Primary domain sources** take precedence over secondary domain sources when they conflict (regardless of sub-domain selection).
5. **Parent domain defaults** apply for any domain where no sub-domain is selected.

*The key rule:* Sub-domain selection refines within a domain. Domain hierarchy (primary > secondary) governs across domains. A secondary domain's sub-domain can add and specialize sources, but those sources still enter the configuration at the secondary domain's priority level as defined in Section 2.

**Example:** A user selects Primary: Software / Technology → IT Operations/Infrastructure, Secondary: Cybersecurity → Cloud Security/Architecture.

- IT Ops/Infrastructure authority adjustments apply to the primary domain's authority tier (primary sources level).
- Cloud Security/Architecture authority adjustments apply to the secondary domain's contributed sources (secondary sources level, per Section 2 merge rules).
- If both sub-domains promote NIST SP 800-53, it appears in the primary tier (because IT Ops promoted it within the primary domain).
- CIS Benchmarks (promoted by Cloud Security sub-domain) appear in the secondary tier (because they're promoted within a secondary domain).
- The user can manually promote CIS Benchmarks to the primary tier if their work warrants it.

---

## Sub-Domain Profiles

Each profile defines three things that refine the parent domain:

- **Authority tier adjustments:** Sources that get promoted, added, or deprioritized for this specialization
- **Escalation trigger refinements:** Triggers that get added or elevated for this specialization
- **Scope hints:** Suggested in-scope and out-of-scope topics specific to this specialization

All three are presented as editable defaults. The user accepts, modifies, or replaces.

---

### Cybersecurity

**Parent defaults:** NIST (SP 800-53, CSF, 800-171), CISA, MITRE ATT&CK, ISO/IEC 27001, OWASP, SANS, CIS Benchmarks

**Sub-domains:**

**Security Operations / Incident Response**
- Authority adjustments:
  - Promote: MITRE ATT&CK, CISA alerts and advisories, NIST SP 800-61r3 (Incident Response Recommendations, aligned to CSF 2.0, published April 2025)
  - Add: Vendor-specific SIEM and EDR documentation, FIRST (Forum of Incident Response and Security Teams)
  - Deprioritize: ISO/IEC 27001 (relevant but not primary for operational work)
- Escalation refinements:
  - Add: Active threat indicators requiring immediate containment decisions
  - Elevate: Urgency override triggers are on by default (Section 5, Edge Case 5)
- Scope hints:
  - In-scope: Alert triage, detection rule tuning, incident classification, log analysis, playbook development, threat intelligence interpretation
  - Out-of-scope: Compliance certification decisions, penetration testing methodology, application code review

**Governance, Risk & Compliance (GRC)**
- Authority adjustments:
  - Promote: NIST SP 800-53, NIST CSF, ISO/IEC 27001, ISO/IEC 27701
  - Add: SOC 2 Trust Service Criteria (AICPA), FedRAMP documentation, CMMC requirements
  - Deprioritize: MITRE ATT&CK (relevant for threat context but not primary for compliance mapping)
- Escalation refinements:
  - Add: Audit readiness determinations, control adequacy assessments for specific environments
  - Elevate: Compliance certification pass/fail interpretations (already in parent, elevated to always-trigger)
- Scope hints:
  - In-scope: Framework mapping, control implementation guidance, policy template development, risk assessment methodology, audit preparation
  - Out-of-scope: Active incident response, vulnerability exploitation techniques, specific tool configuration

**Cloud Security / Architecture**
- Authority adjustments:
  - Promote: CIS Benchmarks, CSA Cloud Controls Matrix (CCM v4/v4.1, 207 controls across 17 domains), CSA STAR program documentation
  - Add: AWS Well-Architected Framework (Security Pillar), Azure Security Benchmark, GCP Security Best Practices (vendor-specific, official documentation only), NIST SP 1800-35 (Zero Trust Architecture practice guide, draft)
  - Deprioritize: SANS (still valid but less central for cloud-native work)
- Escalation refinements:
  - Add: Production infrastructure change decisions, cross-account trust policy modifications
  - Elevate: Specific vulnerability assessment for production systems (already in parent, applies more frequently here)
- Scope hints:
  - In-scope: Cloud configuration review, IAM policy guidance, network architecture, encryption implementation, logging and monitoring architecture, infrastructure-as-code security
  - Out-of-scope: Physical security controls, non-cloud compliance frameworks, application-layer vulnerability assessment

**Application Security**
- Authority adjustments:
  - Promote: OWASP (all projects, not just Top 10), NIST SSDF (SP 800-218 v1.1, with v1.2 in draft as of December 2025)
  - Add: CWE (Common Weakness Enumeration), CERT Secure Coding Standards, language-specific security guides (official sources only), NIST SP 800-218A (SSDF Community Profile for Generative AI and Dual-Use Foundation Models), OWASP Top 10 for LLM Applications (2025 edition)
  - Deprioritize: CIS Benchmarks (infrastructure-focused)
- Escalation refinements:
  - Add: Vulnerability severity classification for specific production applications, remediation prioritization for actively exploited vulnerabilities
  - Elevate: Code review decisions with legal or regulatory implications
- Scope hints:
  - In-scope: Secure coding patterns, vulnerability classification, threat modeling for applications, SAST/DAST interpretation, dependency analysis, API security
  - Out-of-scope: Infrastructure hardening, compliance certification, incident response procedures

**Identity & Access Management (IAM)**
- Authority adjustments:
  - Promote: NIST SP 800-63 (Digital Identity Guidelines), NIST SP 800-207 (Zero Trust Architecture)
  - Add: FIDO Alliance specifications, OAuth/OIDC official documentation, vendor-specific IAM documentation (Okta, Azure AD/Entra, AWS IAM)
  - Deprioritize: OWASP (relevant for AuthN/AuthZ flaws but not primary for IAM architecture)
- Escalation refinements:
  - Add: Privileged access decisions for production systems, federation trust establishment
  - Elevate: Any question involving break-glass or emergency access procedures
- Scope hints:
  - In-scope: Authentication architecture, authorization models, directory services, federation, MFA implementation, privileged access management, identity lifecycle
  - Out-of-scope: Application vulnerability testing, network security architecture, physical access controls

---

### Healthcare

**Parent defaults:** HHS, FDA, CMS, WHO, peer-reviewed medical journals, CDC, NIH, HIPAA official guidance

**Sub-domains:**

**Clinical Operations**
- Authority adjustments:
  - Promote: CMS Conditions of Participation, Joint Commission standards, state health department regulations
  - Add: Agency for Healthcare Research and Quality (AHRQ), professional society clinical guidelines (AMA, ANA, specialty-specific)
  - Deprioritize: FDA (relevant for device/drug context but not primary for operations)
- Escalation refinements:
  - Add: Staffing adequacy determinations, clinical workflow changes affecting patient care
  - Elevate: Any question about specific patient care decisions (already in parent, now always-trigger)
- Scope hints:
  - In-scope: Operational workflows, scheduling optimization, quality metrics, accreditation preparation, department management, resource allocation frameworks
  - Out-of-scope: Specific patient diagnosis or treatment, pharmaceutical recommendations, medical device technical specifications

**Health IT / Informatics**
- Authority adjustments:
  - Promote: ONC (Office of the National Coordinator for Health IT), HL7 FHIR standards
  - Add: HITRUST CSF, CHIME/AEHIS resources, vendor-specific EHR documentation (Epic, Cerner/Oracle Health —” official documentation only), FDA guidance on AI/ML-based Software as Medical Device (SaMD) including Predetermined Change Control Plan (PCCP, finalized December 2024) and AI/ML Lifecycle Management (January 2025)
  - Deprioritize: WHO (global policy, less relevant for IT implementation)
- Escalation refinements:
  - Add: System configuration changes affecting clinical decision support, data migration decisions involving patient records
  - Elevate: Any question about clinical data interpretation or use in AI model training
- Scope hints:
  - In-scope: EHR configuration, interoperability standards, health data exchange, clinical informatics workflows, health IT security, AI/ML in clinical decision support
  - Out-of-scope: Direct patient care decisions, medical billing code selection, pharmaceutical formulary decisions

**Healthcare Compliance / Privacy**
- Authority adjustments:
  - Promote: HIPAA (Privacy Rule, Security Rule, Breach Notification Rule), HHS Office for Civil Rights guidance
  - Add: State-specific health privacy laws, 42 CFR Part 2 (substance use disorder records), HITECH Act provisions, FTC Health Breach Notification Rule
  - Deprioritize: WHO, CMS (relevant background but not primary for compliance)
- Escalation refinements:
  - Add: Breach determination decisions, Business Associate Agreement scope questions
  - Elevate: Any question about specific incident reporting obligations or timelines
- Scope hints:
  - In-scope: HIPAA compliance interpretation, privacy impact assessment, security risk assessment methodology, breach response procedures, training content development, policy template development
  - Out-of-scope: Legal defense strategy, specific litigation guidance, insurance coverage determinations

---

### Financial Services

**Parent defaults:** SEC, FINRA, FDIC, OCC, Basel Committee publications, FASB, Dodd-Frank, SOX

**Sub-domains:**

**Banking / Lending**
- Authority adjustments:
  - Promote: OCC Comptroller's Handbook, FDIC guidance
  - Add: CFPB guidance and enforcement actions, Fair Lending regulations (ECOA, HMDA), BSA/AML guidance (FinCEN), FFIEC IT Examination Handbooks
  - Deprioritize: Basel Committee (relevant for capital adequacy but not primary for operational lending)
- Escalation refinements:
  - Add: Fair lending analysis for specific loan decisions, BSA/AML suspicious activity determinations
  - Elevate: Any question about specific customer account decisions
- Scope hints:
  - In-scope: Regulatory compliance frameworks, risk assessment methodology, lending policy development, BSA/AML program design, examination preparation, deposit operations
  - Out-of-scope: Specific customer loan approvals or denials, investment advisory, insurance underwriting

**Investment / Wealth Management**
- Authority adjustments:
  - Promote: SEC regulations (Advisers Act, Investment Company Act), FINRA rules
  - Add: CFA Institute Standards of Practice, CFP Board Standards, Morningstar research methodology (as reference for analytical frameworks, not as investment recommendation source)
  - Deprioritize: FDIC, OCC (banking-focused)
- Escalation refinements:
  - Add: Suitability or best-interest determinations for specific clients, fee structure modifications
  - Elevate: Any question about specific portfolio allocation recommendations (already in universal triggers, now always-trigger)
- Scope hints:
  - In-scope: Investment frameworks and theory, regulatory compliance, fiduciary standards, portfolio construction methodology, risk assessment frameworks, client communication templates
  - Out-of-scope: Specific buy/sell recommendations, individual client portfolio analysis, market predictions, tax return preparation

**Insurance**
- Authority adjustments:
  - Promote: NAIC model laws and regulations, state insurance department publications
  - Add: AM Best rating methodology, ISO (Insurance Services Office) forms and rules, actuarial standards (Actuarial Standards Board)
  - Deprioritize: SEC, FINRA (relevant for variable products but not primary for general insurance)
- Escalation refinements:
  - Add: Claims coverage determinations, underwriting decisions for specific risks, rate adequacy assessments
  - Elevate: Any question about specific policy coverage interpretation
- Scope hints:
  - In-scope: Regulatory compliance frameworks, product development guidelines, underwriting methodology, claims process design, actuarial concepts, market conduct standards
  - Out-of-scope: Specific claims adjudication, individual policy pricing, legal interpretation of policy language

---

### AI Governance

**Parent defaults:** NIST AI RMF, EU AI Act, ISO/IEC 42001, OECD AI Principles, IEEE standards

**Sub-domains:**

**AI Risk Management**
- Authority adjustments:
  - Promote: NIST AI RMF (AI 100-1), ISO/IEC 42001 (AI Management System)
  - Add: ISO/IEC 23894 (AI Risk Management), OWASP AI Exchange (Flagship project covering AI security, privacy, and safety), OWASP Top 10 for LLM Applications (2025 edition), OWASP Agentic AI Top 10 (December 2025), NIST Cyber AI Profile (in development, companion to NIST CSF 2.0 for AI-specific risks), MITRE ATLAS (Adversarial Threat Landscape for AI Systems)
  - Deprioritize: Jurisdiction-specific regulations (handled by AI Regulatory Compliance sub-domain)
- Escalation refinements:
  - Add: Risk classification decisions for specific AI systems, impact assessment determinations
  - Elevate: Any question about high-risk system classification
- Scope hints:
  - In-scope: Risk identification frameworks, impact assessment methodology, testing and evaluation approaches, monitoring and reporting design, organizational governance structure, vendor AI risk assessment
  - Out-of-scope: Specific regulatory compliance determinations, legal interpretation of AI regulations, model development or training

**AI Regulatory Compliance**
- Authority adjustments:
  - Promote: EU AI Act (full text), EU General-Purpose AI (GPAI) Guidelines (published July 2025), GPAI Code of Practice
  - Add: Jurisdiction-specific AI regulations, sector-specific AI guidance (healthcare AI, financial AI), regulatory sandbox documentation, EC Guidelines for General-Purpose AI compliance
  - Deprioritize: OECD AI Principles (high-level, less operational for compliance)
- Escalation refinements:
  - Add: Compliance determination for specific AI systems, cross-jurisdictional regulatory conflict resolution
  - Elevate: Any question about specific penalties, enforcement actions, or compliance deadlines
- Scope hints:
  - In-scope: Regulatory requirement mapping, compliance gap analysis, documentation requirements, conformity assessment preparation, regulatory reporting, cross-border compliance
  - Out-of-scope: Technical AI model development, risk management methodology (covered by AI Risk Management sub-domain), general ethics without regulatory basis

---

### Legal

**Parent defaults:** Statutory text, regulatory body publications, court opinions (when verifiable), bar association guidance

**Sub-domains:**

**Corporate / Commercial**
- Authority adjustments:
  - Promote: UCC provisions, SEC filings and guidance, state business entity statutes
  - Add: ABA Business Law Section resources, Delaware Court of Chancery opinions (for corporate governance), Restatements (relevant sections)
  - Deprioritize: Non-commercial regulatory guidance
- Escalation refinements:
  - Add: Contract interpretation for specific agreements, entity structure decisions, M&A considerations
  - Elevate: Any question requiring application of law to specific facts (always in legal domain, reinforced here)
- Scope hints:
  - In-scope: Corporate governance frameworks, contract drafting patterns, regulatory compliance overview, entity formation considerations, commercial transaction structures
  - Out-of-scope: Specific legal advice, litigation strategy, individual case analysis, tax law application

**Employment / Labor**
- Authority adjustments:
  - Promote: Department of Labor guidance, EEOC publications, NLRB decisions
  - Add: State-specific employment law resources, ABA Labor and Employment Section resources, SHRM (as industry practice reference, not legal authority)
  - Deprioritize: SEC, commercial law sources
- Escalation refinements:
  - Add: Termination decisions, discrimination or harassment complaint handling, wage and hour determinations
  - Elevate: Any question about specific employee situations or disciplinary actions
- Scope hints:
  - In-scope: Employment law overview, policy development, compliance frameworks, workplace safety standards, benefits administration regulations, hiring process guidelines
  - Out-of-scope: Specific employee case analysis, litigation strategy, union negotiation tactics, individual termination decisions

**Privacy / Data Protection**
- Authority adjustments:
  - Promote: GDPR (full text and Article 29 Working Party / EDPB guidance), CCPA/CPRA
  - Add: State-specific privacy laws, IAPP resources, NIST Privacy Framework, FTC enforcement guidance, sector-specific privacy regulations (HIPAA, GLBA, FERPA, COPPA)
  - Deprioritize: General commercial law sources
- Escalation refinements:
  - Add: Data breach notification determinations, Data Protection Impact Assessment conclusions, cross-border transfer decisions
  - Elevate: Any question about specific incident response or regulatory notification obligations
- Scope hints:
  - In-scope: Privacy program design, compliance gap analysis, DPIA methodology, data mapping, consent framework design, vendor privacy assessment, privacy-by-design implementation
  - Out-of-scope: Specific legal opinions on enforcement actions, DPA interaction strategy, individual rights request adjudication

---

### Education

**Parent defaults:** Department of Education, accreditation body publications, peer-reviewed educational research, ISTE standards

**Sub-domains:**

**K-12 Education**
- Authority adjustments:
  - Promote: State Department of Education standards and regulations, ISTE Standards for Students/Educators
  - Add: Common Core State Standards (where applicable), FERPA guidance (for student privacy), IDEA (Individuals with Disabilities Education Act), Title I guidance
  - Deprioritize: Higher education accreditation body publications
- Escalation refinements:
  - Add: Individual student accommodation decisions, mandatory reporting obligations, IEP/504 plan modifications
  - Elevate: Any question about specific student situations involving privacy or safety
- Scope hints:
  - In-scope: Curriculum alignment, instructional strategy, classroom technology integration, assessment design, differentiated instruction, parent communication frameworks
  - Out-of-scope: Individual student diagnosis, specific IEP recommendations, disciplinary hearing decisions, medical or therapeutic recommendations

**Higher Education**
- Authority adjustments:
  - Promote: Regional accreditation body standards, Department of Education regulations (Title IV, Clery Act)
  - Add: SACSCOC/HLC/MSCHE standards (as applicable), AAUP guidelines, NCAA regulations (if athletics are in scope)
  - Deprioritize: K-12-specific standards
- Escalation refinements:
  - Add: Accreditation compliance determinations, Title IX response decisions, FERPA edge cases
  - Elevate: Any question about specific student disciplinary or academic integrity proceedings
- Scope hints:
  - In-scope: Program development, accreditation preparation, institutional effectiveness, assessment methodology, faculty governance, enrollment management strategy
  - Out-of-scope: Individual student academic decisions, specific tenure cases, legal interpretation of institutional policies, financial aid determination

**EdTech / Instructional Design**
- Authority adjustments:
  - Add: Quality Matters standards, ADDIE/SAM methodology references, W3C accessibility guidelines (WCAG), Section 508 compliance
  - Promote: ISTE standards, peer-reviewed educational technology research
  - Deprioritize: Regulatory and accreditation sources (relevant context but not primary for design work)
- Escalation refinements:
  - Add: Accessibility compliance determinations for specific platforms, student data privacy decisions for specific tools
  - Elevate: Any question about COPPA compliance for tools used with minors
- Scope hints:
  - In-scope: Course design methodology, learning management system configuration, assessment design, multimedia content development, accessibility compliance, learning analytics interpretation
  - Out-of-scope: Institutional policy decisions, accreditation reporting, individual student assessment, IT infrastructure management

---

### Software / Technology

**Parent defaults:** Official language/framework documentation, vendor-specific technical documentation, established technology publications, community documentation (Stack Overflow, official forums)

**Sub-domains:**

**Software Development**
- Authority adjustments:
  - Promote: Official language and framework documentation
  - Add: Language-specific style guides (official), design pattern references (Gang of Four, Martin Fowler), testing framework documentation, NIST SSDF (SP 800-218) for secure development practices
  - Deprioritize: Infrastructure and operations-focused documentation
- Escalation refinements:
  - Add: Architecture decisions with significant technical debt implications, technology stack decisions binding the organization long-term
  - Elevate: Security vulnerability decisions in production code
- Scope hints:
  - In-scope: Code architecture, design patterns, API design, testing strategy, code review, debugging methodology, version control workflows, CI/CD pipeline design, dependency management
  - Out-of-scope: Infrastructure provisioning, network architecture, database administration, security compliance certification

**IT Operations / Infrastructure**
- Authority adjustments:
  - Promote: Vendor-specific infrastructure documentation (AWS, Azure, GCP, VMware —” official docs only)
  - Add: ITIL framework references, SRE methodology (Google SRE book as reference), monitoring platform documentation, NIST SP 800-53 (for infrastructure security controls)
  - Deprioritize: Application-level development documentation
- Escalation refinements:
  - Add: Production outage triage decisions, capacity planning decisions with significant cost implications, disaster recovery plan modifications
  - Elevate: Any change to production infrastructure during an active incident
- Scope hints:
  - In-scope: Infrastructure architecture, networking, server administration, containerization, orchestration, monitoring and alerting, backup and disaster recovery, cloud resource management, automation and IaC
  - Out-of-scope: Application code review, business logic development, UI/UX design, project management methodology

**Data / Analytics**
- Authority adjustments:
  - Add: Official database/platform documentation, DAMA-DMBOK (Data Management Body of Knowledge)
  - Promote: Vendor-specific data platform documentation
- Scope hints:
  - In-scope: Data modeling, query optimization, ETL/ELT patterns, visualization best practices, data quality methodology, pipeline architecture
  - Out-of-scope: Business strategy decisions based on data, regulatory compliance for data handling (escalate to domain-specific expertise)

---

### Custom Domain

When the user selects "Custom" in Section 2, the sub-domain picker is replaced with a guided configuration flow. No pre-built profiles are applied.

**Guided Custom Flow (Option A):**

Instead of a sub-domain dropdown, the widget presents a short series of questions to build a starter authority tier:

**Question 1: "What types of authoritative sources does your field rely on?"** (checkboxes, select all that apply)
- Government or regulatory body publications
- Academic institutions and peer-reviewed research
- Industry standards bodies (ISO, IEEE, OWASP, etc.)
- Professional associations and licensing boards
- Official vendor or product documentation
- Legal or statutory text
- Other (text field)

**Question 2: "Does your field have specific regulations or compliance requirements?"** (yes/no)
- If yes: Text field to name the regulation(s). These are added to the Primary authority tier.

**Question 3: "Are there specific organizations or publications considered authoritative in your field?"** (optional, repeating text field)
- Named organizations are added to the Primary or Secondary authority tier based on user placement.

The widget assembles a starter authority tier from these inputs. The user reviews and edits before finalizing.

**Closest-Match Fallback (Option B):**

If the user prefers not to answer the guided questions, the widget offers a fallback:

"Would you prefer to start from an existing domain's defaults and customize from there?"

If yes, a dropdown of existing domains is presented. The selected domain's parent defaults populate, and the user edits freely. This is functionally identical to selecting a domain in Section 2 and then overriding fields, but it makes the path explicit for Custom users who know their field is adjacent to an existing domain.

**If neither path is used:** The authority tier fields are left blank with a guidance note: "No authority sources configured. The AI will source from its general training data with no quality filter. Adding at least a Primary authority tier is recommended."

---

## Fallback Behavior

**If no sub-domain is selected (for any domain):** The parent domain defaults from Section 2 apply unchanged for that domain. No sub-domain-specific refinements are added.

**If "General / No specialization" is selected:** Identical to no selection. This option exists so the user can make a deliberate choice rather than leaving a field blank by oversight.

**If the user edits a sub-domain default:** The edit takes priority. Sub-domain profiles are starting points. User modifications are always preserved, even if the user later changes their sub-domain selection. (The widget should confirm before overwriting user edits with new sub-domain defaults.)

**Multi-domain fallback behavior:** Each domain's sub-domain selection is independent. The user can select a sub-domain for their primary domain but skip it for a secondary domain (or vice versa). There is no requirement for consistency —” each domain's refinement level is the user's choice.

---

## Profile Structure (For Community Contributions)

New sub-domain profiles or entirely new domain profiles can be contributed using this template:

```
### [Domain Name] (if new domain)

**Parent defaults:** [List primary, secondary, and any special-category authority sources]

**Sub-domain: [Sub-Domain Name]**

**Authority adjustments:**
- Promote: [Sources from the parent tier that become more important for this specialization]
- Add: [New sources not in the parent tier. Must be verifiable, authoritative sources. Official publications, standards bodies, or recognized professional organizations only.]
- Deprioritize: [Sources from the parent tier that are less central for this specialization. Not removed, just lower priority.]

**Escalation refinements:**
- Add: [New triggers specific to this sub-domain]
- Elevate: [Existing triggers from the parent that should always-trigger in this sub-domain]

**Scope hints:**
- In-scope: [Topics this sub-domain addresses]
- Out-of-scope: [Topics outside this sub-domain's focus. These are suggestions, not hard blocks. The user's configured out-of-scope list in Section 2 takes precedence.]

**Validation notes:** [Any specific test scenarios that should be added to the Evaluation Hooks for this profile]
```

**Contribution requirements:**
- All authority sources must be verifiable organizations, standards bodies, or official publications
- No fabricated source names, invented standards, or assumed publications
- Escalation trigger additions must explain why the trigger is necessary for this sub-domain
- Scope hints are suggestions, not mandates. Users always have final edit authority.
- New domains must include at least two sub-domain profiles to justify domain-level status. A single-specialization domain should be submitted as a sub-domain under the closest existing parent.

---

## Widget Field Definitions

| Field | Widget Input | Required | Default | Trigger |
|---|---|---|---|---|
| Primary Sub-Domain | Dropdown (populated from primary domain) | No | "General / No specialization" | Appears after domain selection in Section 2 (hidden for Custom and General) |
| Secondary Sub-Domain 1 | Dropdown (populated from first secondary domain) | No | "General / No specialization" | Appears only when a secondary domain is selected (hidden for Custom and General) |
| Secondary Sub-Domain 2 | Dropdown (populated from second secondary domain) | No | "General / No specialization" | Appears only when a second secondary domain is selected (hidden for Custom and General) |
| Custom: Source Types | Checkboxes (7 options + Other text field) | No | None | Appears only when domain is "Custom" |
| Custom: Regulatory Requirements | Yes/No toggle + text field | No | No | Appears only when domain is "Custom" |
| Custom: Named Authorities | Repeating text field | No | None | Appears only when domain is "Custom" |
| Custom: Closest-Match Fallback | Dropdown of existing domains | No | None | Appears only when domain is "Custom" and user skips guided questions |

**Dropdown contents by domain:**

| Domain | Sub-Domain Options |
|---|---|
| Cybersecurity | General / No specialization, Security Operations / Incident Response, Governance Risk & Compliance (GRC), Cloud Security / Architecture, Application Security, Identity & Access Management (IAM) |
| Healthcare | General / No specialization, Clinical Operations, Health IT / Informatics, Healthcare Compliance / Privacy |
| Financial Services | General / No specialization, Banking / Lending, Investment / Wealth Management, Insurance |
| AI Governance | General / No specialization, AI Risk Management, AI Regulatory Compliance |
| Legal | General / No specialization, Corporate / Commercial, Employment / Labor, Privacy / Data Protection |
| Education | General / No specialization, K-12 Education, Higher Education, EdTech / Instructional Design |
| Software / Technology | General / No specialization, Software Development, IT Operations / Infrastructure, Data / Analytics |
| Custom | No sub-domain picker shown |
| General | No sub-domain picker shown |

**Widget presentation for multi-domain sub-domain selection:**

The sub-domain pickers are presented in labeled groups:

```
Your primary domain: Software / Technology
  Specialization: [dropdown: General / No specialization ▾]

Your secondary domain: Cybersecurity
  Specialization: [dropdown: General / No specialization ▾]
```

Each dropdown operates independently. Selections update the merged authority tier preview in real time.

---

## Model-Consumed Output (Assembled Example —” Multi-Domain with Sub-Domains)

When a user selects Primary: Software / Technology → IT Operations/Infrastructure, Secondary: Cybersecurity → Cloud Security/Architecture:

```
## Domain Configuration

**Primary Domain:** Software / Technology
**Primary Specialization:** IT Operations / Infrastructure
**Secondary Domain:** Cybersecurity
**Secondary Specialization:** Cloud Security / Architecture

## Source Authority (refined by specializations)

**Primary Sources (prioritize these):**
- Vendor-specific infrastructure documentation (AWS, Azure, GCP, VMware —” official docs only)
- ITIL framework references
- SRE methodology references
- Monitoring platform documentation
- NIST SP 800-53 (for infrastructure security controls)

**Secondary Sources (acceptable when primary unavailable):**
- Established technology publications
- Community-maintained documentation (Stack Overflow, official forums)
- NIST (SP 800-53, CSF, 800-171), CISA, MITRE ATT&CK (cloud matrix)
- CIS Benchmarks (cloud-specific)
- CSA Cloud Controls Matrix (CCM)
- ISO/IEC 27001, OWASP (cloud-relevant projects)
- AWS Well-Architected Framework (Security Pillar)
- Azure Security Benchmark
- GCP Security Best Practices

**Vendor-specific:** Official documentation from relevant cloud providers and infrastructure vendors only. Community blogs, unofficial guides, and third-party interpretations are not authoritative sources.

**Source priority when domains conflict:** Primary domain (Software / Technology) sources take precedence over secondary domain (Cybersecurity) sources.

## Escalation Triggers (combined from all domains and specializations)

In addition to universal triggers:
- Production outage triage decisions
- Capacity planning decisions with significant cost implications
- Disaster recovery plan modifications
- Any change to production infrastructure during an active incident
- Active incident response (ongoing breach or attack)
- Specific vulnerability assessment for a production system
- Compliance certification decisions (pass/fail interpretations)
- Forensic analysis or evidence handling
- Production infrastructure change decisions
- Cross-account trust policy modifications

## Scope Hints (combined, editable)

**Suggested in-scope topics:**
- Infrastructure architecture, networking, containerization, orchestration
- Server administration, monitoring and alerting, backup and disaster recovery
- Cloud resource management, automation and infrastructure-as-code
- Cloud configuration review, IAM policy guidance
- Network security architecture, encryption implementation
- Logging and monitoring architecture, infrastructure-as-code security

**Suggested out-of-scope topics:**
- Application code review and business logic development
- UI/UX design, project management methodology
- Medical diagnosis or treatment recommendations
- Financial investment recommendations
- Legal advice or legal interpretation
```

## Model-Consumed Output (Assembled Example —” Single Domain, unchanged from 1.1)

When a user selects only a primary domain with no secondary domains, the output is identical to the Draft 1.1 format. No multi-domain merge logic applies.

---

## Validation Criteria

### Existing Tests (unchanged from 1.1)
1. **Fallback test:** Select a domain but skip the sub-domain picker. Do the parent domain defaults apply unchanged?
2. **"General / No specialization" equivalence test:** Select "General / No specialization" explicitly. Is the output identical to skipping the picker?
3. **Sub-domain refinement test:** Select a sub-domain. Do the authority tiers, escalation triggers, and scope hints reflect the sub-domain profile (not just the parent)?
4. **Override preservation test:** Select a sub-domain, manually edit an authority source, then change to a different sub-domain. Does the widget warn before overwriting edits?
5. **Custom domain guided flow test:** Select "Custom." Does the widget present the guided source type questions (Option A) instead of the sub-domain picker?
6. **Custom closest-match fallback test:** Select "Custom," skip the guided questions. Does the widget offer the closest-match domain fallback (Option B)? Does selecting a domain populate editable defaults?
7. **Custom blank state test:** Select "Custom," skip both guided flow and closest-match. Are authority tier fields blank with the guidance note about no quality filter?
8. **Cross-section propagation test:** Select a sub-domain with escalation refinements. Do those refinements appear in the assembled escalation protocol output (Section 5)?
9. **Source authority accuracy test:** For each sub-domain profile, verify that all listed authority sources are real organizations, standards, or publications. No fabricated sources.
10. **Scope hint clarity test:** For each sub-domain, are the in-scope and out-of-scope hints specific enough that a borderline question has a clear classification?
11. **Community template test:** Use the profile structure template to create a new sub-domain. Does it integrate cleanly with the widget and model-consumed output format?

### Multi-Domain Sub-Domain Tests (new in 1.2)
12. **Multi-domain sub-domain independence test:** Select a sub-domain for the primary domain but skip for the secondary domain. Does the primary domain get refined defaults while the secondary domain keeps parent defaults?
13. **Multi-domain authority merge with sub-domains test:** Select sub-domains for both primary and secondary domains. Do both sub-domains' authority adjustments apply at the correct tier level (primary sub-domain adjustments at primary tier, secondary sub-domain adjustments at secondary tier)?
14. **Cross-domain escalation merge test:** Select sub-domains with different escalation refinements across primary and secondary domains. Do all escalation triggers appear in the combined list?
15. **Multi-domain scope hint merge test:** Select sub-domains whose scope hints overlap. Do the in-scope hints combine (union) and out-of-scope hints narrow (intersection)?
16. **Override chain with multi-domain sub-domains test:** Manually edit an authority source contributed by a secondary domain sub-domain, then change the secondary sub-domain selection. Does the widget warn before overwriting the manual edit?
17. **Single-domain equivalence test:** Configure a primary domain with sub-domain and no secondary domains. Is the output identical to Draft 1.1 single-domain format?
