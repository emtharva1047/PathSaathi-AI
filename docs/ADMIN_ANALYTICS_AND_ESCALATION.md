# Admin Analytics and Human Escalation Design

## Human counsellor escalation

### Trigger conditions
- A user explicitly requests a human counsellor.
- The AI cannot find sufficient or current evidence.
- The question is sensitive, complex or outside the approved counselling scope.
- The family reports unresolved disagreement and asks for support.

### MVP workflow
1. Explain whether the user is requesting follow-up or an actual live connection.
2. Ask for explicit contact consent and only the minimum contact details needed.
3. Capture concern category and a short summary.
4. Create a request reference and status: submitted, queued, contacted, resolved or cancelled.
5. Make request status visible to the family.
6. Restrict case details to authorised counsellors.

No call-centre endpoint or counsellor integration has been supplied. The MVP must implement a truthful callback/follow-up request and clearly identify the integration point.

## Scheme administrator dashboard

### Aggregate measures
- Sessions started and completed.
- Learner-parent joint participation.
- Conversation language.
- Concern themes: earning potential, safety, job security, social standing, affordability and progression.
- Escalation requests and resolution status.
- Optional explicit self-reported concern ratings before/after counselling.
- Region/trade/provider/language trends when the cohort size permits.

### Sentiment shift
For the MVP, use optional explicit self-report prompts (such as concern level before and after counselling) and selected objection categories. Do not covertly infer emotion from private chats or treat automated sentiment labels as ground truth.

### Privacy rules
- Show aggregate data only to scheme administrators.
- Suppress cohorts below a configurable minimum group size.
- Do not expose individual transcripts, names or contact details in general analytics.
- Restrict detailed case records to counsellors with an authorised purpose.
- Explain what is collected and why; obtain consent for optional check-ins.
