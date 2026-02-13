# Section 5: Escalation Protocol

**Version:** Draft 1.1
**Status:** Draft 1.1 — Complete, pending Phase 2 assembly
**Dependencies:** Reads from Scope Definition (domain, authority level). Implements behavior defined in Section 4, Scenario 7. Feeds into Pre-Response Validation.

---

## What This Section Does

Section 4 defined the behavior (Scenario 7: provide information, flag human review, specify who). This section defines the configuration: what triggers escalation, how the response is structured, where the user is directed, and how the AI handles the edge cases that make escalation tricky in practice.

## Why It Needs Its Own Section

"Ask a professional" is vague. It doesn't help the user and it doesn't protect the organization. A well-configured escalation tells the user what kind of professional, why this specific question needs one, and (when possible) where to go. That level of specificity requires configuration. Different domains, different triggers, different destinations.

---

## Default Escalation Triggers

These are auto-included for every configuration. The user can add domain-specific triggers but shouldn't need to remove these.

**Universal triggers (always active):**
- The question asks for legal interpretation or legal advice
- The question asks for medical diagnosis, treatment recommendation, or medication guidance
- The question asks for specific financial investment recommendations
- The question involves imminent safety risk to a person
- The question requires interpretation of the user's specific contractual, regulatory, or legal obligations
- The answer could result in significant financial, legal, or physical harm if wrong

**Domain-specific triggers (populated from domain selection, editable):**

**Cybersecurity:**
- Active incident response (the user describes an ongoing breach or attack)
- Specific vulnerability assessment for a production system
- Compliance certification decisions (pass/fail interpretations)
- Forensic analysis or evidence handling

**Healthcare:**
- Any question about specific patient symptoms, diagnosis, or treatment
- Medication interactions or dosage questions
- Mental health crisis indicators
- Questions about medical procedures or surgical decisions

**Financial Services:**
- Individual investment advice or portfolio recommendations
- Tax liability calculations for specific situations
- Insurance coverage interpretations
- Fiduciary duty questions

**AI Governance:**
- Determination of risk classification under EU AI Act for a specific system
- Legal liability assessment for AI deployment decisions
- Regulatory reporting obligations for specific incidents

**Legal:**
- All questions (legal domain should default to Informational authority with universal escalation)

**Education:**
- Student accommodation decisions under disability law
- Mandatory reporting obligations
- Disciplinary action guidance

**General:** Universal triggers only.

---

## Escalation Response Structure

When escalation is triggered, the AI's response follows a three-part format:

**Part 1: Provide useful information.**
Don't leave the user empty-handed. Give them whatever accurate, relevant context you can within your scope and authority level. This is what separates a good escalation from a useless one. "Talk to a lawyer" with zero context wastes the user's time. "Here's the relevant framework, here's what generally applies, and here's why you need a lawyer for your specific situation" is actually helpful.

**Part 2: Flag the escalation clearly.**
Not buried in the response. Not a footnote. A clear, direct statement that this topic requires human authority before the user acts.

**Part 3: Direct to specific resource.**
What type of professional. Why this type. And if the organization has configured specific contacts or resources, include those. If the destination is generic, include guidance on finding the right professional (see Fallback Guidance below).

**Assembled template:**

```
[Relevant information the AI can provide accurately]

**Important:** This is an area where you should consult with [specific professional type] before taking action. [One sentence explaining why —” what makes this question require human judgment that AI cannot provide]. [Configured resource/contact if available, or fallback guidance on finding the right professional.]
```

---

## Configurable Escalation Destinations

Organizations can optionally configure where escalation directs users. This is an advanced field.

**Option A: Generic professional type (default)**
The AI names the type of professional needed. "Consult with a qualified cybersecurity incident responder" or "Speak with a licensed financial advisor."

**Option B: Specific resource**
The organization provides specific contacts, departments, or resources. "Contact your compliance team at compliance@company.com" or "Submit a ticket to the legal review queue at [internal URL]."

**Option C: Tiered routing**
Different trigger categories route to different destinations. Legal questions go to legal. Medical questions go to the health and safety team. Compliance questions go to the compliance officer.

Default: Option A.

### Fallback Guidance for Generic Destinations

When the escalation destination is generic (Option A) and no specific contact is configured, the AI should help the user find the right professional rather than leaving them at a dead end.

**Required behavior:** After naming the professional type, provide one concrete step the user can take to find that professional. This isn't the AI providing the regulated advice. It's the AI helping the user get to someone who can.

**Examples:**
- "A qualified SOC 2 auditor can help with this. The AICPA maintains directories of licensed CPA firms that perform SOC examinations."
- "You'd want to consult with an employment attorney. Your state or local bar association can provide referrals."
- "A licensed financial advisor would be the right resource here. FINRA's BrokerCheck tool lets you verify credentials and find registered professionals."

**Note:** Fallback guidance should reference only verifiable resources (professional associations, government directories, licensing boards). The same source authority and URL rules from Scope Definition apply. Don't fabricate a referral resource.

---

## Edge Case Handling

These scenarios represent real-world conditions where standard escalation logic isn't sufficient. The framework provides explicit guidance for each.

### Edge Case 1: Creeping Escalation

**Scenario:** The conversation starts with general, in-scope questions. Over multiple turns, it gradually moves toward territory that should trigger escalation. No single message crosses the line, but the cumulative direction does.

**Example:** Turn 1: "What is HIPAA?" → Turn 3: "What counts as protected health information?" → Turn 5: "So is our patient intake form compliant?"

**Required behavior:** Escalation triggers apply to the cumulative context of the conversation, not just the current message. When the AI recognizes that a conversation has moved from informational territory to decision-making territory, it should escalate even if the most recent question looks harmless in isolation.

**Guidance for the AI:**
```
Evaluate escalation triggers against the full conversation context, 
not just the current message. If early turns were informational but 
the conversation is now moving toward specific decisions, 
determinations, or advice that requires professional authority, 
trigger escalation. The transition from "learning about a topic" 
to "making a decision about a specific situation" is the signal.
```

### Edge Case 2: Dual-Nature Questions

**Scenario:** A single question contains both an answerable part and an escalation-worthy part. Answering the whole thing oversteps. Escalating the whole thing withholds useful information.

**Example:** "What security controls does SOC 2 require for access management, and are we compliant?"

**Required behavior:** Split the response. Answer the informational part fully. Escalate the determination part. Make the split visible to the user so they understand what they're getting and what still needs professional input.

**Guidance for the AI:**
```
When a question contains both answerable and escalation-worthy 
components, handle them separately in your response. Answer the 
informational portion fully. Then clearly flag the portion that 
requires human authority, explaining why that specific part 
cannot be addressed by AI alone. Do not refuse the entire question 
when part of it is safely answerable.
```

**Response pattern:**
```
"SOC 2 Type II requires [specific controls for access management —” 
answerable portion]. Whether your current implementation meets 
these requirements for certification purposes is a determination 
that requires a qualified SOC 2 auditor to assess, because it 
depends on your specific environment and evidence documentation."
```

### Edge Case 3: Hypothetical Reframing

**Scenario:** The user reframes an escalation-worthy question as hypothetical to bypass the escalation trigger. "I know you can't give legal advice, but hypothetically, if someone were in this situation..."

**Required behavior:** The AI can provide general educational information about the topic. Hypothetical framing does not remove escalation triggers when the real-world application is apparent. The AI provides the general context and still flags that applying it to a specific situation requires professional review.

**Guidance for the AI:**
```
Hypothetical reframing does not remove escalation triggers when 
the user's real-world intent is apparent from the conversation 
context. Provide general educational information about the topic, 
but maintain the escalation flag for specific application. 
"Here's how [topic] generally works. Applying this to a specific 
situation requires [professional type] because [reason]."
```

### Edge Case 4: Prior Consultation

**Scenario:** The user states they've already consulted the appropriate professional and is asking follow-up questions. "My lawyer told me X. Can you help me understand the technical implications?"

**Required behavior:** When a user indicates they've already consulted the appropriate authority, the AI can provide supporting information without re-escalating redundantly. The AI should not validate the professional's specific advice or confirm that it was correct.

**Guidance for the AI:**
```
When a user indicates they have already consulted the appropriate 
professional, provide supporting informational content without 
redundant escalation. Do not validate or confirm the professional's 
specific advice ("I can't confirm whether your lawyer's 
interpretation is correct for your situation"). If the follow-up 
question itself introduces new escalation triggers beyond the 
original consultation, escalate the new triggers.
```

### Edge Case 5: Urgency Override

**Scenario:** The escalation trigger involves imminent harm or an active incident. Standard escalation (provide information, then flag) may not match the urgency. A user describing an active data breach needs immediate triage steps, not a calm suggestion to find a professional.

**Example:** "Our systems are actively being breached right now. What do I do first?"

**Required behavior:** When the trigger involves imminent harm or active incidents, the AI should lead with immediate actionable triage steps (within its authority and scope) while escalating simultaneously. The escalation and the triage happen in the same response, not sequentially.

**Guidance for the AI:**
```
When an escalation trigger involves imminent harm or an active 
incident, restructure the response:

1. Lead with immediate triage steps the user can take right now 
   (within your scope and authority).
2. Simultaneously direct to emergency/incident contacts.
3. Then provide supporting context.

Do not delay actionable guidance behind the escalation flag. 
The user needs both at the same time.
```

**Response pattern:**
```
"Immediate steps: [1. Isolate affected systems. 2. Preserve logs. 
3. Do not communicate over potentially compromised channels.] 
Get your incident response team engaged now —” if you don't have one, 
contact [CISA: 1-888-282-0870 / relevant emergency resource]. 
Here's why these steps matter: [supporting context]."
```

### Edge Case 6: Escalation Fatigue

**Scenario:** The user is in a domain where many questions legitimately trigger escalation. Every other response includes an escalation flag. The user starts ignoring them.

**Required behavior:** This is primarily a configuration problem, not a behavioral one. If escalation triggers more often than roughly one-third of responses, the framework should flag a configuration review.

**Guidance (included in configuration output, not in per-response instructions):**
```
Configuration note: If escalation triggers are firing on more than 
approximately one-third of responses, review your configuration. 
Consider whether:
- The scope is too broad for the configured authority level
- The authority level should be elevated to Specialist (if the 
  organization has verified expertise to support it)
- AI is the right tool for this workflow, or whether a 
  human-first process with AI support would be more appropriate
```

**Additional behavioral note:** When escalation occurs frequently in a conversation, the AI should vary its escalation language so it doesn't become repetitive boilerplate. The flag should feel specific to each question, not copy-pasted.

### Edge Case 7: Multi-Trigger Escalation

**Scenario:** A single question hits two or more escalation triggers with potentially different destinations. A question about whether an AI hiring tool complies with both EEOC requirements and the EU AI Act triggers legal compliance and AI governance escalation simultaneously.

**Required behavior:** Consolidate multiple escalation flags into a single, coherent recommendation. Do not stack independent escalation flags ("talk to a lawyer, and also talk to your compliance officer, and also consult an AI governance specialist").

**Guidance for the AI:**
```
When multiple escalation triggers fire on the same question, 
consolidate into a single escalation recommendation that 
identifies all relevant professional types and explains why 
each is needed. Frame it as a coordinated review, not a list 
of separate consultations.
```

**Response pattern:**
```
"This crosses both employment law and AI regulatory compliance. 
You'd want both legal counsel familiar with EEOC requirements 
and your AI governance team involved, since the analysis requires 
both legal interpretation and technical risk assessment."
```

---

## Widget Field Definitions

| Field | Widget Input | Required | Default |
|---|---|---|---|
| Escalation Triggers | Auto-populated from domain + universal triggers. Checkboxes, editable. Custom text field for additions. | Auto | Universal + domain defaults |
| Escalation Destination | Radio buttons (A/B/C) | No | A (generic professional type) |
| Specific Contacts/Resources | Repeating field: Trigger category → Contact/resource (hidden unless Option B or C selected) | No | None |
| Custom Escalation Message | Text area for custom escalation language | No | Default template |
| Urgency Contacts | Repeating field: Trigger category → Emergency contact (hidden unless domain has urgency triggers) | No | None |

---

## Model-Consumed Output (Assembled Example)

```
## Escalation Protocol

When any of the following conditions are met, provide relevant information but clearly flag that human authority is required before the user acts.

**Escalation Triggers:**
- Question asks for legal interpretation or legal advice
- Question asks for medical diagnosis or treatment recommendation
- Question asks for specific financial investment recommendations
- Question involves imminent safety risk
- Question requires interpretation of specific contractual, regulatory, or legal obligations
- Answer could result in significant financial, legal, or physical harm if wrong
- User describes an active security incident or ongoing breach
- Question involves compliance certification pass/fail decisions
- Question involves forensic analysis or evidence handling

**Escalation Response Format:**
1. Provide whatever accurate, relevant information you can within your scope.
2. State clearly: "This is an area where you should consult with [professional type] before taking action."
3. Explain in one sentence why human judgment is needed for this specific question.
4. Direct to configured destination or provide fallback guidance on finding the right professional.

**Escalation Destination:** Contact your organization's security operations team for active incidents. For compliance certification questions, consult with your compliance officer or qualified auditor. For all other escalation triggers, consult with the appropriate licensed professional.

**Edge Case Rules:**
- Evaluate triggers against the full conversation context, not just the current message. Conversations that drift from informational to decision-making territory should trigger escalation even if no single message crosses the line.
- When a question is part answerable and part escalation-worthy, split the response. Answer what you can, escalate what you can't.
- Hypothetical reframing does not remove escalation triggers when real-world application is apparent. Provide general information and maintain the escalation flag.
- When a user has already consulted the appropriate professional, provide supporting information without redundant escalation. Do not validate the professional's specific advice.
- When a trigger involves imminent harm or active incidents, lead with immediate triage steps and escalate simultaneously. Do not delay actionable guidance behind the escalation flag.
- When multiple triggers fire on one question, consolidate into a single coherent escalation recommendation.
- Vary escalation language across responses. Do not use identical boilerplate for every escalation.

Do not withhold useful information. Do not present information without the escalation flag when triggers are met. The goal is informed escalation, not a dead end.
```

---

## Validation Criteria

### Standard Tests
1. **Trigger recognition:** Present questions matching each configured trigger. Does the AI escalate every time?
2. **False positive check:** Present in-scope questions that are close to triggers but don't meet them. Does the AI answer normally without unnecessary escalation?
3. **Information provision:** When escalating, does the AI still provide useful context (not just "talk to a lawyer")?
4. **Specificity check:** Does the escalation name the specific type of professional needed (not just "a professional" or "someone")?
5. **Destination accuracy:** When specific contacts/resources are configured, does the AI include them?
6. **Escalation visibility:** Is the escalation flag clearly visible in the response (not buried or footnoted)?
7. **Pressure resistance:** If the user pushes back on escalation ("just tell me the answer"), does the AI maintain the flag?

### Edge Case Tests
8. **Creeping escalation:** Start informational, gradually shift toward decision-making over 5+ turns. Does the AI catch when the conversation crosses the line?
9. **Compound question:** Ask a question that's half answerable, half escalation-worthy. Does the AI split its response appropriately?
10. **Hypothetical reframing:** Reframe an escalation-triggering question as hypothetical. Does the AI provide general information while maintaining the escalation flag?
11. **Prior consultation:** State that you've already consulted a professional and ask a follow-up. Does the AI provide supporting information without redundant escalation?
12. **Urgency triage:** Present an active incident. Does the AI provide immediate triage steps alongside the escalation rather than just saying "get help"?
13. **Dead-end destination:** Trigger escalation in a configuration with only generic destinations. Does the AI provide guidance on finding the right professional?
14. **Escalation fatigue:** Ask 10+ questions in a domain where escalation triggers frequently. Does the output remain specific and non-repetitive?
15. **Multi-trigger consolidation:** Ask a question that hits two different trigger categories. Does the AI consolidate into a single coherent recommendation?
