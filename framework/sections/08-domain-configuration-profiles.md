# Section 8: Domain Configuration Profiles

**Version:** Draft 1.3
**Status:** Draft 1.3 — Complete, pending Phase 2 assembly
**Dependencies:** Reads from Scope Definition (domain selections — primary and secondary, authority tiers). Feeds refined defaults into Scope Definition (authority tiers), Escalation Protocol (domain-specific triggers), and Pre-Response Validation (rigor scaling).
**Change from 1.2:** Sub-domain picker updated from single-select dropdown to multi-select checkboxes (up to 3 per domain). Three parent domains renamed: "AI Governance" → "AI & Machine Learning," "Software / Technology" → "Technology & Software," "General" → "General / Cross-Industry." New parent domain added: Government & Public Sector (regulated tier, 4 sub-domains). 16 new sub-domain profiles added across 7 parent domains. Multi-select merge rules documented. Initialization acknowledgment guidance added. Widget field definitions and model-consumed output updated.

---

## What This Section Does

Section 2 asks the user to pick a primary domain and optionally up to two secondary domains. Those selections auto-populate broad defaults for source authority, escalation triggers, and scope hints. Those defaults are intentionally general. "Cybersecurity" covers SOC analysts, GRC teams, penetration testers, cloud architects, and application security engineers. The authority tiers that work for all of them are too loose to be optimal for any of them.

This section adds a second-level selection: the sub-domain specialization. It narrows the defaults without adding complexity. The user picks from a short list — for each selected domain. Everything downstream gets tighter. If they skip the pick, the parent domain defaults apply unchanged.

---

## How It Works

The sub-domain picker is optional. It appears after the domain selection in Section 2 and before source authority configuration. When secondary domains are selected, the picker shows sub-domain options for each selected domain.

**Flow:**

1. User selects primary domain (Section 2, Step 1.2) → primary domain defaults populate
2. User optionally selects secondary domains (Section 2, Step 1.2) → secondary domain defaults merge per Section 2 rules
3. Widget presents sub-domain checkbox group for the primary domain (up to 3 selections)
4. If secondary domains are selected, widget presents sub-domain checkbox groups for each secondary domain (in separate, labeled groups, up to 3 each)
5. User picks sub-domains (any, all, or none) → refined defaults replace parent defaults for each domain where a sub-domain was selected
6. User skips the pick or selects "General / No specialization" for any domain → that domain's parent defaults remain
7. User can still manually edit any auto-populated field regardless of selections

**Multi-select merge rules (new in 1.3):**

When a user selects multiple sub-domains within a single domain:

- **Authority sources:** Union. All Promote, Add, and Deprioritize entries from each selected sub-domain apply. If one sub-domain promotes a source and another deprioritizes the same source, Promote wins (the user selected both specializations, so the source is relevant).
- **Escalation triggers:** Union. All Add and Elevate entries from each selected sub-domain apply.
- **Scope hints (in-scope):** Union. All in-scope topics from each selected sub-domain are combined.
- **Scope hints (out-of-scope):** Intersection. Only topics that appear in the out-of-scope list of ALL selected sub-domains remain out-of-scope. If any selected sub-domain considers a topic in-scope (or doesn't list it as out-of-scope), it is not out-of-scope in the merged result.

Selecting "General / No specialization" clears other selections for that domain (mutually exclusive with specific sub-domains).

**The override chain:** Most specific wins, with domain hierarchy preserved.

1. **Manual user edits** override everything.
2. **Primary domain sub-domain defaults** override primary domain parent defaults.
3. **Secondary domain sub-domain defaults** override secondary domain parent defaults.
4. **Primary domain sources** take precedence over secondary domain sources when they conflict (regardless of sub-domain selection).
5. **Parent domain defaults** apply for any domain where no sub-domain is selected.

*The key rule:* Sub-domain selection refines within a domain. Domain hierarchy (primary > secondary) governs across domains. A secondary domain's sub-domain can add and specialize sources, but those sources still enter the configuration at the secondary domain's priority level as defined in Section 2.

**Example:** A user selects Primary: Technology & Software → IT Operations/Infrastructure, Secondary: Cybersecurity → Cloud Security/Architecture.

- IT Ops/Infrastructure authority adjustments apply to the primary domain's authority tier (primary sources level).
- Cloud Security/Architecture authority adjustments apply to the secondary domain's contributed sources (secondary sources level, per Section 2 merge rules).
- If both sub-domains promote NIST SP 800-53, it appears in the primary tier (because IT Ops promoted it within the primary domain).
- CIS Benchmarks (promoted by Cloud Security sub-domain) appear in the secondary tier (because they're promoted within a secondary domain).
- The user can manually promote CIS Benchmarks to the primary tier if their work warrants it.

**Multi-select example:** A user selects Primary: AI & Machine Learning → [Generative AI & LLMs, Agentic AI Systems].

- Both sub-domains' authority adjustments merge: OWASP Top 10 for LLMs (from Generative AI) and OWASP Agentic Top 10 (from Agentic AI) both appear as promoted sources.
- Scope hints combine: prompt engineering (Generative AI) and agent permission boundaries (Agentic AI) are both in-scope.
- Out-of-scope narrows: only topics that both sub-domains list as out-of-scope remain out-of-scope. "Specific model weights or architecture internals" appears in both, so it stays out-of-scope. "Supply chain risks for agent frameworks" is in-scope for Agentic AI, so it is not out-of-scope in the merged result even if the other sub-domain doesn't mention it.

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

**Threat Intelligence & Hunting** *(new in 1.3)*
- Authority adjustments:
  - Promote: MITRE ATT&CK (tactics, techniques, and procedures mapping), CISA Known Exploited Vulnerabilities (KEV) catalog, NIST SP 800-150 (Guide to Cyber Threat Information Sharing)
  - Add: STIX/TAXII standards documentation (OASIS), Mandiant/Google Threat Intelligence reports, VirusTotal and OSINT aggregator methodology (official documentation only), Diamond Model of Intrusion Analysis
  - Deprioritize: ISO/IEC 27001 (governance framework, not operationally primary for threat hunting)
- Escalation refinements:
  - Add: Active threat campaign attribution decisions, intelligence confidence level assessments (use analytic standards: almost certainly, probably, roughly even chance — avoid unqualified certainty)
  - Elevate: Urgency override triggers on by default (Section 5, Edge Case 5) — time-sensitive threat intelligence requires immediate escalation pathways
- Scope hints:
  - In-scope: Indicator of compromise (IOC) analysis, threat actor profiling, hunting hypothesis development, detection engineering, intelligence report interpretation, OSINT methodology, kill chain and diamond model application
  - Out-of-scope: Compliance certification, penetration testing execution, vulnerability remediation implementation, incident containment procedures

**Penetration Testing & Red Team** *(new in 1.3)*
- Authority adjustments:
  - Promote: OWASP (Testing Guide, Web Security Testing Guide, ASVS), MITRE ATT&CK (adversary emulation), NIST SP 800-115 (Technical Guide to Information Security Testing and Assessment)
  - Add: PTES (Penetration Testing Execution Standard), CREST certification body methodology, Offensive Security documentation (official publications only), SANS SEC560/SEC660 curriculum references
  - Deprioritize: CIS Benchmarks (defensive hardening focus, not primary for offensive assessment)
- Escalation refinements:
  - Add: Rules of engagement boundary questions, scope creep during active engagements, findings that indicate active compromise by a real threat actor
  - Elevate: Any question involving exploitation of production systems, social engineering methodology targeting real individuals, or creation of functional exploit code — always escalate. This sub-domain provides methodology guidance and report writing support, not active exploitation assistance.
- Scope hints:
  - In-scope: Methodology guidance, tool usage explanation, report writing, vulnerability classification, attack surface analysis, post-exploitation documentation, purple team coordination
  - Out-of-scope: Writing functional exploit code, providing active attack tools, specific vulnerability exploitation steps for named production targets, social engineering scripts targeting real people

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
  - Add: HITRUST CSF, CHIME/AEHIS resources, vendor-specific EHR documentation (Epic, Cerner/Oracle Health — official documentation only), FDA guidance on AI/ML-based Software as Medical Device (SaMD) including Predetermined Change Control Plan (PCCP, finalized December 2024) and AI/ML Lifecycle Management (January 2025)
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

**Medical Devices & Equipment** *(new in 1.3)*
- Authority adjustments:
  - Promote: FDA regulations (21 CFR Parts 800-1299), FDA guidance on cybersecurity in medical devices (final June 2025, implements Section 524B of FD&C Act)
  - Add: IEC 62443 (industrial cybersecurity, applied to medical device networks), AAMI TIR57 (Principles for medical device security — risk management), UL 2900 standards, IMDRF guidance documents
  - Deprioritize: General hospital operations guidance (relevant context but not primary for device-specific work)
- Escalation refinements:
  - Add: Device classification decisions (Class I/II/III), premarket submission pathway determinations (510(k) vs PMA vs De Novo)
  - Elevate: Any question involving specific patient safety implications, device recall determinations, or post-market adverse event reporting obligations — always escalate to regulatory affairs professional
- Scope hints:
  - In-scope: Device classification guidance, premarket submission documentation, quality system compliance, software validation methodology, cybersecurity risk management for devices, SBOM preparation, postmarket surveillance
  - Out-of-scope: Clinical treatment decisions, pharmaceutical dosing, direct patient diagnosis, specific device repair procedures

**Pharmaceuticals & Clinical Research** *(new in 1.3)*
- Authority adjustments:
  - Promote: FDA regulations (21 CFR Parts 210/211 for cGMP, 21 CFR Part 11 for electronic records), ICH Guidelines (Q7 Good Manufacturing Practice, E6(R2) Good Clinical Practice, Q9 Quality Risk Management)
  - Add: EMA guidelines on clinical trial data management, ClinicalTrials.gov registration requirements, WHO Good Manufacturing Practices, NIH clinical research policies
  - Deprioritize: General hospital operations guidance (relevant context but not primary for pharma/research)
- Escalation refinements:
  - Add: Clinical trial protocol interpretation, adverse event classification decisions, drug interaction assessments
  - Elevate: Any question involving specific patient treatment recommendations, off-label use guidance, or clinical trial eligibility determinations — always escalate to qualified medical professional
- Scope hints:
  - In-scope: Regulatory pathway guidance, GMP/GCP compliance documentation, clinical trial design methodology, pharmacovigilance processes, submission formatting (NDA/BLA/ANDA), data integrity requirements
  - Out-of-scope: Specific drug prescribing, patient diagnosis, clinical treatment selection, adverse event causality determination for specific patients

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

**Payments & Fintech** *(new in 1.3)*
- Authority adjustments:
  - Promote: PCI DSS v4.0.1 (Payment Card Industry Data Security Standard), FFIEC IT Examination Handbook, Consumer Financial Protection Bureau (CFPB) guidance
  - Add: PSD2/PSD3 documentation (EU Payment Services Directives), Nacha Operating Rules (ACH network), SWIFT Customer Security Programme, EMVCo specifications (chip/contactless/tokenization)
  - Deprioritize: Investment-specific regulations (SEC, FINRA) — adjacent but not primary for payments
- Escalation refinements:
  - Add: Transaction fraud pattern classification, payment processing compliance determinations, merchant category code interpretation for specific businesses
  - Elevate: Any question involving specific consumer dispute resolution, chargeback liability determination, or money transmission licensing requirements
- Scope hints:
  - In-scope: Payment security standards, transaction processing architecture, compliance mapping, fraud detection methodology, open banking API standards, digital wallet implementation, regulatory reporting requirements
  - Out-of-scope: Specific investment advice, insurance underwriting, loan approval decisions, individual consumer financial planning

**Financial Compliance (SEC/FINRA/AML)** *(new in 1.3)*
- Authority adjustments:
  - Promote: SEC regulations and guidance (Securities Exchange Act, Investment Advisers Act), FINRA rules and regulatory notices, BSA/AML regulations (Bank Secrecy Act, FinCEN guidance)
  - Add: FATF Recommendations (Financial Action Task Force — international AML/CFT standards), OCC guidance (Office of the Comptroller of the Currency), OFAC sanctions compliance guidance, Dodd-Frank Act implementing regulations
  - Deprioritize: PCI DSS (payments-specific, not primary for securities/AML compliance)
- Escalation refinements:
  - Add: Suspicious Activity Report (SAR) filing threshold determinations, Know Your Customer (KYC) enhanced due diligence triggers, sanctions screening interpretation
  - Elevate: Any question involving specific enforcement action interpretation, insider trading analysis, or Suspicious Activity Report filing decisions for specific transactions — always escalate to compliance officer or legal counsel
- Scope hints:
  - In-scope: Regulatory framework mapping, compliance program design, AML/KYC methodology, sanctions screening processes, regulatory examination preparation, recordkeeping requirements, compliance training content
  - Out-of-scope: Specific legal defense strategy, enforcement action outcome prediction, individual transaction approval/denial, specific investment suitability determinations

---

### AI & Machine Learning

*Renamed from "AI Governance" in Draft 1.3. Parent defaults updated.*

**Parent defaults:** NIST AI RMF (AI 100-1), EU AI Act (official text), ISO/IEC 42001, OECD AI Principles, IEEE standards on AI ethics

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

**AI Ethics & Responsible AI** *(new in 1.3)*
- Authority adjustments:
  - Promote: NIST AI RMF (AI 100-1, with revision in progress per AI Action Plan), EU AI Act implementing guidance (European Commission), ISO/IEC 42001 (AI management system)
  - Add: UNESCO Recommendation on the Ethics of AI, OECD AI Policy Observatory resources, Algorithmic Accountability Act provisions (where enacted), Partnership on AI responsible practices documentation, IEEE 7000 series (ethical considerations in system design)
  - Deprioritize: Technical ML implementation standards (relevant context but ethics/governance focus takes precedence here)
- Escalation refinements:
  - Add: Bias impact assessment decisions, fairness metric selection for specific populations, AI system risk classification under EU AI Act (prohibited/high-risk/limited/minimal)
  - Elevate: Any question involving specific harm determinations for protected groups, AI-driven decisions in high-stakes domains (criminal justice, employment, credit), or whistleblower protection scenarios
- Scope hints:
  - In-scope: AI governance frameworks, bias detection methodology, fairness and transparency requirements, impact assessment design, AI ethics policy development, stakeholder engagement processes, responsible AI maturity models
  - Out-of-scope: Model architecture design, training pipeline optimization, specific model performance tuning, MLOps infrastructure

**Generative AI & LLMs** *(new in 1.3)*
- Authority adjustments:
  - Promote: OWASP Top 10 for LLM Applications (2025 edition), NIST AI 100-2e2025 (Adversarial Machine Learning taxonomy), EC Guidelines for General-Purpose AI (GPAI) providers
  - Add: OWASP AI Exchange, MITRE ATLAS (Adversarial Threat Landscape for AI Systems), NIST SP 800-218A (SSDF Community Profile for Generative AI and Dual-Use Foundation Models), Stanford HAI AI Index Report (annual, research reference only)
  - Deprioritize: Traditional software testing frameworks (relevant but insufficient for generative AI-specific risks like hallucination and prompt injection)
- Escalation refinements:
  - Add: Hallucination risk classification for specific use cases, prompt injection vulnerability assessments, content safety boundary determinations
  - Elevate: Any question involving generative AI for regulated industries (healthcare, legal, financial), deepfake detection methodology for specific cases, or AI-generated content attribution/disclosure requirements
- Scope hints:
  - In-scope: Prompt engineering best practices, hallucination mitigation strategies, guardrail design, content filtering methodology, RAG architecture guidance, fine-tuning governance, red teaming for LLMs, evaluation framework design
  - Out-of-scope: Specific model weights or architecture internals, training data curation for proprietary models, compute infrastructure sizing

**Agentic AI Systems** *(new in 1.3)*
- Authority adjustments:
  - Promote: OWASP Top 10 for Agentic Applications (2026 edition, released December 2025), OWASP Agentic AI Threats and Mitigations taxonomy (v1.1)
  - Add: OWASP Agentic Threat Modelling Guide, NIST IR 8596 (Cybersecurity Framework Profile for AI, draft December 2025), MCP (Model Context Protocol) security documentation, NVIDIA Safety and Security Framework for Real-World Agentic Systems
  - Deprioritize: Static LLM-only security frameworks (agentic systems require distinct autonomous-action threat models beyond content generation risks)
- Escalation refinements:
  - Add: Agent permission boundary decisions, tool-use authorization scope determinations, multi-agent orchestration trust model questions
  - Elevate: Any question involving autonomous agent actions in production environments, agent-to-agent trust establishment, or agentic systems interacting with critical infrastructure — always escalate to security architect or system owner
- Scope hints:
  - In-scope: Agentic architecture security patterns, tool-use authorization frameworks, memory and context poisoning prevention, agent identity and privilege management, orchestration loop security, kill-switch and human-in-the-loop design, supply chain risks for agent frameworks
  - Out-of-scope: Specific agent framework implementation code, proprietary orchestration platform internals, real-time agent monitoring tool configuration

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

**Regulatory Compliance** *(new in 1.3)*
- Authority adjustments:
  - Promote: Federal Register (official rulemaking source), CFR (Code of Federal Regulations), relevant agency-specific guidance (EPA, OSHA, FTC, FCC — depending on industry context)
  - Add: State-level regulatory databases, GAO reports (Government Accountability Office), Congressional Research Service reports, Administrative Procedure Act provisions
  - Deprioritize: Case law databases (relevant for litigation, less primary for compliance program design)
- Escalation refinements:
  - Add: Regulatory interpretation questions where agency guidance is ambiguous or conflicting, compliance timeline determinations for new regulations
  - Elevate: Any question involving specific enforcement risk assessment, regulatory self-disclosure decisions, or compliance determinations that could trigger reporting obligations — always escalate to legal counsel
- Scope hints:
  - In-scope: Regulatory framework mapping, compliance program design, rulemaking process explanation, comment period guidance, compliance gap analysis methodology, regulatory change monitoring processes
  - Out-of-scope: Specific legal advice for individual cases, litigation strategy, regulatory negotiation tactics, penalty amount estimation

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

**Corporate Learning & Development** *(new in 1.3)*
- Authority adjustments:
  - Promote: ATD (Association for Talent Development) competency models, ISO 21001 (Educational organizations management systems)
  - Add: Kirkpatrick Model documentation (evaluation framework), ADDIE framework references, SCORM/xAPI standards (eLearning interoperability), Bersin by Deloitte research (workforce learning trends — use as industry reference, not regulatory authority)
  - Deprioritize: K-12 curriculum standards (CCSS, NGSS) and higher education accreditation frameworks — different audience and regulatory context
- Escalation refinements:
  - Add: Mandatory compliance training content accuracy determinations (e.g., OSHA, harassment prevention, data privacy), training effectiveness claims requiring statistical evidence
  - Elevate: Any question involving legally mandated training content (anti-harassment, safety compliance, export controls), ADA/accessibility compliance for training materials, or training record requirements for regulatory audits
- Scope hints:
  - In-scope: Instructional design methodology, learning management system strategy, training needs analysis, competency framework development, learning measurement and ROI, microlearning and blended learning design, onboarding program structure
  - Out-of-scope: Academic degree program curriculum design, K-12 pedagogy, student assessment methodology, university accreditation processes

---

### Technology & Software

*Renamed from "Software / Technology" in Draft 1.3.*

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
  - Promote: Vendor-specific infrastructure documentation (AWS, Azure, GCP, VMware — official docs only)
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

**Product Management** *(new in 1.3)*
- Authority adjustments:
  - Promote: Pragmatic Institute framework references, SVPG (Silicon Valley Product Group) methodology documentation
  - Add: Lean Product Playbook methodology, Jobs-to-Be-Done framework documentation, Product-Led Growth references (OpenView), ProductPlan and Pendo research (industry benchmarks — use as reference, not regulatory authority)
  - Deprioritize: Deep software engineering standards (IEEE, SWEBOK) — relevant context but product management operates at the strategy and requirements layer
- Escalation refinements:
  - Add: Product roadmap prioritization decisions involving legal, regulatory, or safety considerations, pricing strategy recommendations
  - Elevate: Any question involving specific competitive intelligence claims (verify sources), market sizing with specific revenue projections, or product decisions with regulatory implications (healthcare, financial, children's products)
- Scope hints:
  - In-scope: Product strategy frameworks, user research methodology, roadmap planning, prioritization techniques, stakeholder communication, product metrics and analytics, A/B testing methodology, go-to-market strategy, feature specification writing
  - Out-of-scope: Specific code implementation, infrastructure architecture, financial modeling for investor presentations, legal contract terms

---

### Government & Public Sector *(new in 1.3)*

*NEW parent domain. Risk tier: Regulated.*

**Parent defaults:** NIST SP 800-53, FISMA, FedRAMP, OMB Circulars (A-130, A-123), GAO Standards for Internal Control, CISA guidance, FAR/DFARS (where applicable)

**Sub-domains:**

**Federal Government**
- Authority adjustments:
  - Promote: NIST SP 800-53 Rev. 5, FedRAMP requirements, OMB memoranda (M-24-15 and current), FISMA implementation guidance
  - Add: CIO Council publications, Federal IT Dashboard data references, FITARA (Federal Information Technology Acquisition Reform Act) scorecard criteria, Section 508 accessibility standards, CISA Binding Operational Directives (BODs)
  - Deprioritize: State and local government frameworks (relevant context but federal agencies operate under distinct statutory authority)
- Escalation refinements:
  - Add: Authority to Operate (ATO) determination questions, FOIA/Privacy Act classification decisions, CUI (Controlled Unclassified Information) handling determinations
  - Elevate: Any question involving classified information handling, interagency data sharing agreements, or federal records management decisions — always escalate to designated agency official
- Scope hints:
  - In-scope: Federal IT policy guidance, compliance framework mapping, ATO process documentation, cybersecurity program design for agencies, cloud migration strategy (FedRAMP pathway), federal acquisition cybersecurity requirements, zero trust architecture implementation per OMB mandates
  - Out-of-scope: Classified system architecture, specific intelligence community methods, specific appropriations/budget decisions, political policy recommendations

**State & Local Government**
- Authority adjustments:
  - Promote: NIST CSF 2.0 (voluntary but widely adopted at state/local level), MS-ISAC (Multi-State Information Sharing and Analysis Center) guidance, CISA Cross-Sector Cybersecurity Performance Goals (CPG 2.0, released December 2025)
  - Add: NASCIO (National Association of State CIOs) publications, state-specific data breach notification laws reference, NGA (National Governors Association) cybersecurity resources, SLTT-specific CISA resources
  - Deprioritize: FedRAMP (federal cloud authorization — some states adopt similar approaches but not directly applicable), DFARS (defense contracting focus)
- Escalation refinements:
  - Add: Public records request handling decisions, inter-jurisdictional data sharing questions, election infrastructure security determinations
  - Elevate: Any question involving citizen PII handling decisions, public safety system configuration, or election system security — always escalate to designated official and legal counsel
- Scope hints:
  - In-scope: Cybersecurity program design for state/local agencies, incident response planning, constituent data protection, IT modernization guidance, grant-funded technology program compliance, emergency management technology coordination
  - Out-of-scope: Federal-specific compliance (FedRAMP, DFARS), classified systems, specific political policy recommendations, judicial system IT (specialized jurisdiction)

**Defense & Intelligence**
- Authority adjustments:
  - Promote: NIST SP 800-53 Rev. 5, CMMC (Cybersecurity Maturity Model Certification) requirements, DoD Instruction 8510.01 (Risk Management Framework for DoD Systems), DFARS 252.204-7012
  - Add: DISA STIGs (Security Technical Implementation Guides), NSA Cybersecurity Advisories and Technical Guidance, CNSSI 1253 (Committee on National Security Systems), DoD CIO publications, ITAR/EAR export control guidance references
  - Deprioritize: Commercial-only frameworks (SOC 2, PCI DSS) — relevant where DoD uses commercial services but not primary authority
- Escalation refinements:
  - Add: CUI/CDI (Covered Defense Information) handling determinations, CMMC level assessment scope questions, supply chain risk decisions for defense systems
  - Elevate: Any question involving classified information (even referencing classification levels), specific weapons system details, intelligence collection methods, or ITAR-controlled technical data — always escalate. This sub-domain explicitly does not handle classified content.
- Scope hints:
  - In-scope: CMMC compliance guidance, DoD cybersecurity policy interpretation, DFARS compliance documentation, STIG implementation guidance, zero trust architecture for DoD environments, supply chain security for defense contractors, CUI protection programs
  - Out-of-scope: Classified system architecture or operations, specific intelligence methods or sources, weapons system design, operational planning, anything requiring security clearance to discuss

**Critical Infrastructure**
- Authority adjustments:
  - Promote: CISA Cross-Sector Cybersecurity Performance Goals (CPG 2.0), NIST CSF 2.0, NIPP 2013 (National Infrastructure Protection Plan, with 2025 National Plan update in development per NSM-22)
  - Add: Sector-specific plans (CISA 2015 series — Energy, Water, Transportation, Communications, etc.), NERC CIP (North American Electric Reliability Corporation Critical Infrastructure Protection, for energy sector), TSA Security Directives (pipeline and surface transportation), sector-specific ISACs (Information Sharing and Analysis Centers), ICS-CERT advisories
  - Deprioritize: General IT-focused frameworks (SOC 2, ISO 27001) — relevant for corporate IT but insufficient for operational technology and industrial control system environments
- Escalation refinements:
  - Add: IT/OT boundary configuration decisions, safety-instrumented system interactions, cascading failure risk assessments across interconnected infrastructure
  - Elevate: Any question involving real-time operational decisions for utilities, transportation, or public safety systems — always escalate to system operators and engineers. AI guidance is advisory only for systems where incorrect configuration could cause physical harm.
- Scope hints:
  - In-scope: Critical infrastructure security frameworks, IT/OT convergence guidance, sector risk assessment methodology, resilience planning, incident response for industrial environments, supply chain security for critical components, cybersecurity performance goal implementation
  - Out-of-scope: Specific control system programming, real-time operational decisions for utilities/transportation, physical infrastructure engineering, emergency response operational command

---

### General / Cross-Industry

*Renamed from "General" in Draft 1.3.*

No sub-domain picker is shown. The parent defaults from Section 2 apply directly. This domain serves users who don't fit a specific vertical or who need broad, multi-topic coverage.

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

**Multi-domain fallback behavior:** Each domain's sub-domain selection is independent. The user can select a sub-domain for their primary domain but skip it for a secondary domain (or vice versa). There is no requirement for consistency — each domain's refinement level is the user's choice.

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

## Initialization Acknowledgment Guidance *(new in 1.3)*

When the model receives a GAIO configuration block, it should provide a brief initialization acknowledgment before proceeding with the user's first substantive request. This serves two purposes: (1) confirms the configuration was received and parsed, and (2) gives the user a clear signal that guardrails are active.

**Format:** 2–3 sentences. State the primary domain, specialization(s) if selected, and enforcement mode. Do not recite the full configuration.

**Example:**

> Configuration received. Operating in **Cybersecurity → Cloud Security / Architecture** with Full Enforcement. Source authority is anchored to CIS Benchmarks, CSA CCM, and cloud provider documentation. Ready for your first question.

**Rules:**
- The acknowledgment is informational, not a commitment to specific behavior. The model's actual behavior is governed by the full configuration.
- If the configuration is malformed or incomplete, the acknowledgment should note what's missing and apply the closest valid fallback (per Section 10, Session Persistence rules).
- The acknowledgment is a one-time event per session. Do not repeat it after every message.
- In Integrity Lock mode (Mode B), the acknowledgment should explicitly state: "Integrity Lock active — no configuration modifications permitted during this session."

---

## Widget Field Definitions

| Field | Widget Input | Required | Default | Trigger |
|---|---|---|---|---|
| Primary Sub-Domain(s) | Checkbox list (populated from primary domain, max 3) | No | "General / No specialization" | Appears after domain selection in Section 2 (hidden for Custom and General / Cross-Industry) |
| Secondary Sub-Domain(s) 1 | Checkbox list (populated from first secondary domain, max 3) | No | "General / No specialization" | Appears only when a secondary domain is selected (hidden for Custom and General / Cross-Industry) |
| Secondary Sub-Domain(s) 2 | Checkbox list (populated from second secondary domain, max 3) | No | "General / No specialization" | Appears only when a second secondary domain is selected (hidden for Custom and General / Cross-Industry) |
| Custom: Source Types | Checkboxes (7 options + Other text field) | No | None | Appears only when domain is "Custom" |
| Custom: Regulatory Requirements | Yes/No toggle + text field | No | No | Appears only when domain is "Custom" |
| Custom: Named Authorities | Repeating text field | No | None | Appears only when domain is "Custom" |
| Custom: Closest-Match Fallback | Dropdown of existing domains | No | None | Appears only when domain is "Custom" and user skips guided questions |

**Checkbox contents by domain:**

| Domain | Sub-Domain Options |
|---|---|
| Cybersecurity | General / No specialization, Security Operations / Incident Response, Governance Risk & Compliance (GRC), Cloud Security / Architecture, Application Security, Identity & Access Management (IAM), Threat Intelligence & Hunting, Penetration Testing & Red Team |
| Healthcare | General / No specialization, Clinical Operations, Health IT / Informatics, Healthcare Compliance / Privacy, Medical Devices & Equipment, Pharmaceuticals & Clinical Research |
| Financial Services | General / No specialization, Banking / Lending, Investment / Wealth Management, Insurance, Payments & Fintech, Financial Compliance (SEC/FINRA/AML) |
| AI & Machine Learning | General / No specialization, AI Risk Management, AI Regulatory Compliance, AI Ethics & Responsible AI, Generative AI & LLMs, Agentic AI Systems |
| Legal | General / No specialization, Corporate / Commercial, Employment / Labor, Privacy / Data Protection, Regulatory Compliance |
| Education | General / No specialization, K-12 Education, Higher Education, EdTech / Instructional Design, Corporate Learning & Development |
| Technology & Software | General / No specialization, Software Development, IT Operations / Infrastructure, Data / Analytics, Product Management |
| Government & Public Sector | General / No specialization, Federal Government, State & Local Government, Defense & Intelligence, Critical Infrastructure |
| Custom | No sub-domain picker shown |
| General / Cross-Industry | No sub-domain picker shown |

**Widget presentation for multi-domain sub-domain selection (updated in 1.3 for multi-select):**

The sub-domain pickers are presented as checkbox groups with a cap of 3 selections per domain:

```
Your primary domain: Technology & Software
  Specialization(s): (select up to 3)
  ☐ General / No specialization
  ☐ Software Development
  ☐ IT Operations / Infrastructure
  ☐ Data / Analytics
  ☐ Product Management

Your secondary domain: Cybersecurity
  Specialization(s): (select up to 3)
  ☐ General / No specialization
  ☐ Security Operations / Incident Response
  ☐ Governance, Risk & Compliance (GRC)
  ☐ Cloud Security / Architecture
  ☐ Application Security
  ☐ Identity & Access Management (IAM)
  ☐ Threat Intelligence & Hunting
  ☐ Penetration Testing & Red Team
```

Each checkbox group operates independently. Selections update the merged authority tier preview in real time. Selecting "General / No specialization" clears other selections for that domain (mutually exclusive with specific sub-domains).

When multiple sub-domains are selected, the widget shows a combined scope preview with any Promote/Deprioritize conflicts highlighted for user review.

---

## Model-Consumed Output (Assembled Example — Multi-Domain with Multi-Select Sub-Domains)

When a user selects Primary: AI & Machine Learning → [Generative AI & LLMs, Agentic AI Systems]:

```
## Domain Configuration

**Primary Domain:** AI & Machine Learning
**Primary Specialization(s):** Generative AI & LLMs, Agentic AI Systems

## Initialization Acknowledgment

Operating in **AI & Machine Learning** with dual specialization: **Generative AI & LLMs** and **Agentic AI Systems**. Source authority is anchored to OWASP LLM Top 10, OWASP Agentic Top 10, NIST AI frameworks, and MITRE ATLAS. [Enforcement mode] active. Ready for your first question.

## Source Authority (merged from selected specializations)

**Primary Sources (prioritize these):**
- NIST AI RMF (AI 100-1)
- EU AI Act
- ISO/IEC 42001
- OWASP Top 10 for LLM Applications (2025 edition)
- NIST AI 100-2e2025 (Adversarial Machine Learning taxonomy)
- EC Guidelines for General-Purpose AI (GPAI) providers
- OWASP Top 10 for Agentic Applications (2026 edition)
- OWASP Agentic AI Threats and Mitigations taxonomy (v1.1)
- OWASP AI Exchange
- MITRE ATLAS
- NIST SP 800-218A
- OWASP Agentic Threat Modelling Guide
- NIST IR 8596 (Cybersecurity Framework Profile for AI)
- MCP security documentation
- NVIDIA Safety and Security Framework for Real-World Agentic Systems
- Stanford HAI AI Index Report (research reference only)

**Deprioritized (from both sub-domains):**
- Traditional software testing frameworks
- Static LLM-only security frameworks (when addressing agentic concerns)

## Escalation Triggers (merged from both specializations)

In addition to universal triggers:
- Hallucination risk classification for specific use cases
- Prompt injection vulnerability assessments
- Content safety boundary determinations
- Generative AI use in regulated industries (healthcare, legal, financial)
- Deepfake detection methodology for specific cases
- AI-generated content attribution/disclosure requirements
- Agent permission boundary decisions
- Tool-use authorization scope determinations
- Multi-agent orchestration trust model questions
- Autonomous agent actions in production environments
- Agent-to-agent trust establishment
- Agentic systems interacting with critical infrastructure

## Scope Hints (merged, union for in-scope, intersection for out-of-scope)

**Suggested in-scope topics:**
- Prompt engineering best practices, hallucination mitigation strategies
- Guardrail design, content filtering methodology
- RAG architecture guidance, fine-tuning governance
- Red teaming for LLMs, evaluation framework design
- Agentic architecture security patterns, tool-use authorization frameworks
- Memory and context poisoning prevention
- Agent identity and privilege management
- Orchestration loop security, kill-switch and human-in-the-loop design
- Supply chain risks for agent frameworks

**Suggested out-of-scope topics:**
- Specific model weights or architecture internals
- Training data curation for proprietary models
- Compute infrastructure sizing
- Proprietary orchestration platform internals
```

## Model-Consumed Output (Assembled Example — Cross-Domain with Sub-Domains)

When a user selects Primary: Technology & Software → IT Operations/Infrastructure, Secondary: Cybersecurity → Cloud Security/Architecture:

```
## Domain Configuration

**Primary Domain:** Technology & Software
**Primary Specialization:** IT Operations / Infrastructure
**Secondary Domain:** Cybersecurity
**Secondary Specialization:** Cloud Security / Architecture

## Source Authority (refined by specializations)

**Primary Sources (prioritize these):**
- Vendor-specific infrastructure documentation (AWS, Azure, GCP, VMware — official docs only)
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

**Source priority when domains conflict:** Primary domain (Technology & Software) sources take precedence over secondary domain (Cybersecurity) sources.

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

## Model-Consumed Output (Assembled Example — Single Domain, unchanged from 1.1)

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

### Multi-Domain Sub-Domain Tests (from 1.2)
12. **Multi-domain sub-domain independence test:** Select a sub-domain for the primary domain but skip for the secondary domain. Does the primary domain get refined defaults while the secondary domain keeps parent defaults?
13. **Multi-domain authority merge with sub-domains test:** Select sub-domains for both primary and secondary domains. Do both sub-domains' authority adjustments apply at the correct tier level (primary sub-domain adjustments at primary tier, secondary sub-domain adjustments at secondary tier)?
14. **Cross-domain escalation merge test:** Select sub-domains with different escalation refinements across primary and secondary domains. Do all escalation triggers appear in the combined list?
15. **Multi-domain scope hint merge test:** Select sub-domains whose scope hints overlap. Do the in-scope hints combine (union) and out-of-scope hints narrow (intersection)?
16. **Override chain with multi-domain sub-domains test:** Manually edit an authority source contributed by a secondary domain sub-domain, then change the secondary sub-domain selection. Does the widget warn before overwriting the manual edit?
17. **Single-domain equivalence test:** Configure a primary domain with sub-domain and no secondary domains. Is the output identical to Draft 1.1 single-domain format?

### Phase A Tests (new in 1.3)
18. **Multi-select sub-domain merge test:** Select two sub-domains within one domain. Do authority sources union correctly? Do in-scope topics union and out-of-scope topics intersect?
19. **Multi-select cap test:** Attempt to select more than 3 sub-domains within one domain. Does the widget enforce the cap?
20. **Multi-select General exclusion test:** Select a specific sub-domain, then select "General / No specialization." Does the widget clear the specific sub-domain selection?
21. **Domain rename propagation test:** Select a renamed domain (AI & Machine Learning, Technology & Software, or General / Cross-Industry). Does the correct label appear throughout all output sections?
22. **New domain profile test:** Select Government & Public Sector and each of its sub-domains. Do authority adjustments, escalation triggers, and scope hints populate correctly?
23. **New sub-domain profile test:** For each of the 16 new sub-domains, verify the profile loads correctly and all authority sources are real.
24. **Multi-select Promote/Deprioritize conflict test:** Select two sub-domains where one promotes a source and the other deprioritizes it. Does Promote win per merge rules?
25. **Multi-select cross-domain test:** Select multiple sub-domains in primary domain AND multiple sub-domains in secondary domain. Does the full merge (multi-select within domains + cross-domain hierarchy) produce correct output?
26. **Government regulated tier test:** Select Government & Public Sector as primary domain. Does the weight determination assign Full weight (regulated domain)?
27. **Initialization acknowledgment test:** Generate a configuration with sub-domains selected. Does the model-consumed output include the initialization acknowledgment with correct domain and specialization names?
28. **Initialization acknowledgment — multi-select test:** Select multiple sub-domains. Does the acknowledgment correctly name all selected specializations?
29. **Initialization acknowledgment — single domain test:** Select a single domain with no sub-domains. Does the acknowledgment correctly name the domain and specialization(s)?
30. **Initialization acknowledgment — Integrity Lock test:** Generate a Mode B (Integrity Lock) configuration. Does the initialization acknowledgment include the explicit Integrity Lock notice?
31. **Cross-domain new profile test:** Select a new sub-domain (e.g., Agentic AI Systems) as primary and an existing sub-domain (e.g., Cloud Security / Architecture) as secondary. Does the multi-domain merge work correctly across new and existing profiles?

---

## Source Verification Summary (new in 1.3)

All authority sources in Phase A profiles are verified organizations, standards, or publications:

- OWASP Top 10 for Agentic Applications (2026 edition, released December 2025) — genai.owasp.org
- OWASP Agentic AI Threats and Mitigations taxonomy v1.1 — genai.owasp.org
- NIST IR 8596 (Cybersecurity Framework Profile for AI) — preliminary draft December 2025, csrc.nist.gov
- CISA CPG 2.0 (Cross-Sector Cybersecurity Performance Goals) — released December 2025
- FDA Cybersecurity in Medical Devices guidance — final June 2025, implements Section 524B of FD&C Act
- NIPP 2013 with 2025 National Plan update in development per NSM-22
- STIX/TAXII standards — OASIS open standards for threat intelligence sharing
- Diamond Model of Intrusion Analysis — established threat analysis framework
- ICH Guidelines (Q7, E6(R2), Q9) — International Council for Harmonisation
- PCI DSS v4.0.1 — Payment Card Industry standard, current version
- FATF Recommendations — Financial Action Task Force, international AML/CFT standard
- UNESCO Recommendation on the Ethics of AI — adopted November 2021
- CMMC (Cybersecurity Maturity Model Certification) — DoD contractor cybersecurity standard
- DISA STIGs — Defense Information Systems Agency, technical implementation guides
- ATD (Association for Talent Development) — professional learning and development body
- SVPG, Pragmatic Institute — recognized product management methodology sources
- MS-ISAC (Multi-State Information Sharing and Analysis Center) — CISA partnership
- NASCIO (National Association of State CIOs) — state government IT leadership
- CNSSI 1253 — Committee on National Security Systems
- NERC CIP — North American Electric Reliability Corporation Critical Infrastructure Protection standards
- TSA Security Directives — Transportation Security Administration, pipeline/surface transportation
