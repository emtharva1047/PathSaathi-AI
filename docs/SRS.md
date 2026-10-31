# Software Requirements Specification — PathSaathi AI

**SIH Problem Statement ID:** 26241  
**Sponsor:** Ministry of Skill Development and Entrepreneurship (MSDE)  
**Theme:** Smart Education

## 1. Purpose

Specify a portfolio MVP for a bilingual AI-enabled counselling platform that engages vocational learners and their families together, uses localised trade/provider outcome evidence, explains career and NSQF progression, and provides human escalation and scheme-admin insights.

## 2. Problem context from the SIH brief

The brief states that family perception can influence enrolment, retention and willingness to pursue NSQF-aligned progression. Parent concerns include earning potential, safety, job security and social standing. Existing career guidance is described as largely learner-facing. The proposed system must therefore support the family unit, not merely provide an individual career quiz.

The expected solution includes:
- joint learner-parent conversational counselling in regional language(s) plus English;
- verified trade/training-provider outcome data, including post-training earnings and placement rates;
- contextual plain-language explainers for trade/job-role mapping and NSQF progression;
- human counsellor escalation;
- an administrator dashboard showing where resistance is concentrated and how engagement/expressed sentiment changes;
- design suitable for low-literacy and low-digital-familiarity users.

The SIH entry notes that dummy placement/earnings datasets will be supplied for hackathon evaluation. Those files are not yet present in the repository.

## 3. User classes

### Learner
A student exploring vocational options who wants understandable guidance, realistic local evidence and a voice in the family decision.

### Parent/guardian
A family member who may influence or support enrolment and may have questions about earnings, safety, job security, social perception, affordability and progression.

### Human counsellor
A trained person who receives escalations, reviews complex concerns and provides guidance beyond the AI's evidence or competence.

### Scheme administrator
An authorised user who views aggregate engagement, objection themes and concern shifts to identify where outreach or support may be needed.

### Data administrator
An authorised user who imports/maintains outcome records and source metadata.

## 4. Functional requirements

### Joint counselling and language
- FR-01: The system shall support a learner and parent/guardian in the same counselling journey, with their roles and contributions distinguishable.
- FR-02: The system shall provide key user flows in English and at least one regional language. The MVP target is English and Marathi, using reviewed locale strings and templates.
- FR-03: The conversation shall address common concerns including income potential, placement/job security, safety, social perception, affordability and progression.
- FR-04: The system shall use short, low-jargon explanations and guided prompts suitable for users with limited digital familiarity.
- FR-05: The system shall support optional contextual tailoring using broad location, household-income bracket and learner academic background. Exact household income should not be required.
- FR-06: The system shall preserve learner and parent perspectives separately and shall not silently let one overwrite the other's preferences.

### Outcome-data backend
- FR-07: The system shall import the SIH-provided dummy placement/earnings dataset when it becomes available.
- FR-08: The system shall validate schema, types, missing values, duplicates, impossible ranges, cohort denominators and source metadata during import.
- FR-09: The system shall store outcome data at an appropriate trade/provider/geographic/cohort/time-period granularity.
- FR-10: Placement rates shall be displayed with placed count, eligible/completed cohort denominator, cohort size and reporting period whenever provided; denominator definitions must be explicit.
- FR-11: Earnings figures shall show currency, time basis (e.g. monthly/annual), statistic type (mean/median/range), follow-up period and observation count where available.
- FR-12: The system shall never invent missing outcomes; unavailable or insufficient data must be labelled unknown/unavailable.
- FR-13: Outcome comparisons shall expose source, last-updated/verification date and relevant cohort limitations.

### Trade, job-role and NSQF explainer
- FR-14: The system shall explain a selected trade, typical job-role mapping, skills and working-context information in plain language.
- FR-15: The system shall show verified NSQF qualification level and possible level-up/further-education routes when source information exists.
- FR-16: The system shall tailor examples and comparisons to broad location, income bracket and academic background without implying that these factors determine a learner's ability or future.
- FR-17: The system shall distinguish verified facts, contextual explanation and unknown information.

### Human escalation
- FR-18: The user shall be able to request a human counsellor when the AI cannot answer adequately or the family asks for human help.
- FR-19: The system shall capture the minimum contact and concern information needed for follow-up, with explicit consent.
- FR-20: The system shall create a request reference and status (submitted, queued, contacted, resolved/cancelled).
- FR-21: If no live counsellor integration exists, the MVP shall clearly label the workflow as a callback/follow-up request rather than pretending a live connection has occurred.

### Admin analytics and engagement
- FR-22: The administrator dashboard shall show aggregate engagement by available dimensions such as region, trade, training provider, language and conversation stage.
- FR-23: The dashboard shall aggregate common family concern/objection categories such as income, safety, job security, social standing, affordability and progression.
- FR-24: The system shall support an optional explicit self-reported concern/sentiment check-in before and after counselling, and show aggregate shifts.
- FR-25: The system shall not perform covert emotion inference. Any text sentiment analysis, if later added, must be disclosed, consented, evaluated and secondary to self-report.
- FR-26: The dashboard shall suppress small cohorts and avoid exposing household identities or individual conversation transcripts to general administrators.

### Reports and administration
- FR-27: The system shall generate a shareable summary containing discussed concerns, relevant outcome evidence, progression options, unresolved questions, escalation status and source references.
- FR-28: Authorised data administrators shall manage outcome records and provenance.
- FR-29: Authorised counsellors shall view only escalations and case information required for follow-up.
- FR-30: The system shall provide exportable, privacy-safe aggregate dashboard summaries for scheme review.

## 5. Non-functional requirements

- NFR-01 Security: hash passwords; protect secrets through environment variables; validate authorisation server-side.
- NFR-02 Privacy: minimise personal data, use broad optional income brackets, define retention and deletion, and use synthetic profiles for development.
- NFR-03 Consent: family linking, contact follow-up and optional sentiment/concern analytics require transparent consent.
- NFR-04 Explainability: outcome summaries expose definitions, denominator, cohort, period and provenance.
- NFR-05 Reliability: deterministic evidence retrieval and explainers must continue if the LLM API is unavailable.
- NFR-06 Maintainability: separate UI, API, domain services, data ingestion, analytics and AI integrations.
- NFR-07 Accessibility: mobile-friendly, high-contrast, labelled controls, short steps, simple text, and text alternatives to icons.
- NFR-08 Localisation: UI strings and reusable content must be locale-managed; translations must be reviewed before release.
- NFR-09 Testability: data calculations, eligibility, privacy aggregation and family comparison must be unit-testable.
- NFR-10 Safety: no guaranteed salary, admission, placement or job-security claims.

## 6. Outcome-data model and integrity rules

The data contract is specified in `docs/OUTCOME_DATA_CONTRACT.md`. Key dimensions include trade, training provider, district/state, cohort/batch, qualification/NSQF level, completion denominator, placement numerator, earnings fields, follow-up period, source and verification date.

The SIH-provided dummy data is the intended evaluation dataset. Until it is supplied, use only explicitly synthetic fixtures to test the importer and UI. Do not make demo statistics look official.

## 7. Sentiment and resistance measurement

For the MVP, capture an optional self-reported concern rating and objection categories before and after counselling. This provides an interpretable shift measure without covertly inferring emotions. Admin views must aggregate data and suppress small groups. Raw family conversation content must not be exposed in general scheme-admin dashboards.

## 8. Initial data entities

- User: role, locale, authentication fields
- LearnerProfile: education, broad region, optional income bracket, preferences
- FamilySession: learner, invited parent/guardian, consent and status
- ConversationMessage: session, participant role, language, content and timestamp (retention-limited)
- ConcernCheckIn: session, stage (pre/post), concern category and self-reported rating
- Trade: code, title, description, skills and source metadata
- TrainingProvider: provider code/name, location and verified metadata
- OutcomeRecord: trade/provider/region/cohort, completion count, placed count, earnings metrics, units, follow-up period, source and verification
- QualificationPathway: qualification, NSQF level and progression edges with sources
- EscalationRequest: session, reason, contact consent, reference and status
- AggregateEngagement: privacy-safe derived metrics
- Report: session, generated summary and source references

## 9. Acceptance criteria

- A learner and parent can participate in one bilingual counselling flow.
- The system can import and validate the eventual SIH dummy outcome dataset using a documented contract.
- Outcome cards show trade/provider/region/cohort/time context and denominators.
- The system refuses to invent unavailable earnings or placement data.
- A plain-language trade and NSQF progression explainer can be generated from verified records.
- A user can submit a human follow-up request and see its status.
- Admin dashboard shows aggregate engagement, objection categories and explicit self-reported concern shifts with small-cohort suppression.
- Low-literacy usability choices are visible and tested.
- Unit/integration tests and CI pass; deployment and data limitations are documented.


## 10. Supporting pathway exploration (portfolio enhancement)

This feature supports counselling but does not replace the SIH brief's central family conversation and outcome-evidence requirements.

- FR-31: The learner may complete a short guided exploration of interests, education background, practical preferences and constraints to shortlist relevant vocational trades/qualifications for discussion.
- FR-32: Pathway shortlisting shall be transparent and advisory. It shall not be presented as a validated aptitude test, psychometric assessment or prediction of success.
- FR-33: Where a specific qualification has published entry criteria, the system shall distinguish eligible, ineligible and unknown eligibility. Unknown information shall not be represented as eligible.
- FR-34: Any shortlist shall show why an option was surfaced, which profile factors were considered, which source supports its entry criteria, and what information is missing.
- FR-35: A learner may explore options outside the shortlist; the shortlist shall not block access to other vocational information.
