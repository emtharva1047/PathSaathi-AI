# Software Requirements Specification (SRS)

**Project:** PathSaathi AI  
**Problem statement:** SIH26241 — AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education  
**Baseline reviewed:** 1 November 2026

## 1. Purpose

Specify a solo-developer portfolio MVP that addresses the official SIH26241 requirements while remaining achievable in a 60-day Python-first build.

## 2. Problem and product scope

The official challenge is not only a student-facing career recommender. It requires joint learner-family counselling, credible local evidence about vocational outcomes, bilingual/regional-language access, low-jargon support, a route to human counsellors, and an administrator view of engagement and parental concerns.

PathSaathi AI will provide:
- a shared student-parent counselling journey with separate participant preferences;
- an eligibility-aware, explainable pathway explorer;
- source-linked qualification, provider and outcome evidence;
- a simple-language conversational assistant in English and Marathi for the initial Maharashtra pilot;
- a counsellor escalation request workflow;
- privacy-conscious aggregate engagement and concern analytics.

**MVP geography/language assumption:** Maharashtra pilot, English + Marathi. This is a practical product scope assumption, not a restriction in the SIH statement. The architecture should permit additional regional languages and regions later.

The platform is advisory. It does not make admission decisions, certify skills, guarantee jobs, or promise salary outcomes.

## 3. User classes

### Learner / student
Creates a minimal profile, completes an assessment, explores recommendations, asks questions in a shared family session, compares courses and views a report.

### Parent / guardian
Joins a student-authorised family session, asks questions about earning potential, job security, safety, recognition and progression, and records independent priorities.

### Counsellor
Receives an escalation request, reviews the student's consented summary and provides human guidance. Human review remains authoritative for individual counselling.

### Scheme administrator
Views aggregate engagement, concern categories and self-reported confidence changes; maintains approved reference data and outcome datasets.

### Data curator
Imports and verifies qualification, provider and outcome records with provenance and quality metadata.

## 4. Functional requirements

- FR-01: The system shall collect only necessary learner context: education/qualification, relevant subjects, interests, skills/confidence indicators, broad district/region, rural/semi-urban/urban context where volunteered, preferences and optional household-income band. It shall not require an exact household income or home address.
- FR-02: The system shall provide a structured assessment and retain the assessment/questionnaire version used for a recommendation.
- FR-03: The system shall evaluate course eligibility using explicit rules and return eligible, ineligible or unknown. Unknown must never be represented as eligible.
- FR-04: The recommendation engine shall rank eligible pathways using transparent, configurable preference matching and shall show the factor breakdown.
- FR-05: Each recommendation shall explain why it matched, identify missing information and show the model/weight version. Prototype weights are assumptions, not validated psychometrics.
- FR-06: The catalogue shall store qualifications, job roles, courses and providers with source URL, source publisher, verification date and confidence/status.
- FR-07: Users shall search, filter, view and compare course/provider/pathway information.
- FR-08: The platform shall explain progression routes, including NSQF-aligned levels and further education routes where verified by source material.
- FR-09: A student shall be able to invite/link a parent or guardian through a consent-aware flow.
- FR-10: Student and parent preferences shall be stored separately; the shared decision view shall expose trade-offs without declaring one party the winner.
- FR-11: The system shall provide a shared conversational counselling session in which learner and parent can ask questions and see the same evidence-backed explanation.
- FR-12: The MVP shall support English and Marathi for key navigation, assessment instructions, common counselling flows and response presentation. Translation quality must be reviewed; raw machine translation shall not be represented as professionally validated.
- FR-13: The AI counsellor shall retrieve from approved platform records and show source references for factual claims. It shall explicitly say when evidence is missing, stale, geographically mismatched or not granular enough.
- FR-14: The outcome-data backend shall store trade/provider/region/cohort-specific employment and earnings evidence with numerator/denominator or sample size, measurement definition, survey period, source, publication date and methodology.
- FR-15: The UI shall distinguish placement rate, post-training employment status, trade-related employment, apprenticeship, self-employment and unrelated employment. It shall not relabel one measure as another.
- FR-16: Outcome evidence shall only be displayed at the granularity supported by the source. State-level evidence must not be presented as provider-specific; old cohorts and small samples must be clearly labelled.
- FR-17: The platform shall provide a structured, low-jargon explainer tailored to broad location, optional household-income band and academic background.
- FR-18: The interface shall provide a simplified journey: one question at a time where useful, clear labels, large controls, icons paired with text, plain-language summaries and an easy review/back path. Audio read-out may be a stretch feature.
- FR-19: Users shall be able to submit a human-counsellor escalation request, choose a concern category and view request status. In the MVP this is a request queue/demo workflow; it must not claim a live counsellor is available unless a real service is connected.
- FR-20: The administrator dashboard shall show aggregate engagement and common parental concern categories (for example, income, job security, safety, social perception, distance and cost).
- FR-21: Sentiment/confidence change shall be based on explicit, optional self-reported feedback before/after counselling, not covert emotion inference. Analytics shall be aggregated and suppress small groups.
- FR-22: The system shall generate a PDF report with profile summary, recommendations, evidence, limitations, source links and next steps.
- FR-23: Counsellor/admin/data-curator functions shall have role-restricted access and auditable updates.

## 5. Non-functional requirements

- NFR-01 Security: passwords must be hashed; secrets supplied through environment variables; family and counsellor access authorised server-side.
- NFR-02 Privacy: minimise personal data, use synthetic development profiles, provide deletion/retention controls, and obtain appropriate consent before collecting personal or minor data in production.
- NFR-03 Explainability: recommendation scores must be decomposable into documented factors and versioned.
- NFR-04 Reliability: deterministic recommendations must work if an LLM provider is unavailable.
- NFR-05 Maintainability: separate UI, API, domain logic, persistence, data ingestion and AI integration.
- NFR-06 Testability: eligibility, scoring, outcome-metric definitions, family permissions and analytics aggregation must be independently testable.
- NFR-07 Accessibility: keyboard-usable controls, readable contrast, clear labels, simple language and responsive layouts.
- NFR-08 Portability: reproducible local setup and environment-based configuration.
- NFR-09 Provenance: every factual qualification/outcome claim must carry source and verification metadata.
- NFR-10 Safety: never guarantee employment, salary, admission or outcomes; AI must not replace a counsellor.
- NFR-11 Localisation: key user journeys must be available in English and Marathi for the pilot; translation updates must be versioned and reviewed.
- NFR-12 Analytics privacy: do not expose identifiable family-level sentiment or small-cohort breakdowns in administrator views.
- NFR-13 Low-bandwidth tolerance: prioritise lightweight text-first pages and graceful degradation when AI or network services are unavailable.

## 6. Recommendation model requirements

Eligibility is a hard filter. A course may be marked eligible only when required criteria are satisfied by available profile data. Missing learner or course data results in unknown.

The MVP may use a transparent weighted match across interest alignment, skill alignment, work-style preference, progression preference and practical fit. Initial weights are prototype assumptions, configurable and versioned. Eligibility is not a weighted dimension.

## 7. Outcome-data integrity requirements

Every outcome record must include:
- metric name and definition;
- numerator and denominator where applicable, or sample size;
- trade/job role and provider/ITI only if the source identifies them;
- geography and cohort/training completion period;
- survey/reference period and publication date;
- salary unit and whether the figure is mean, median, range or band distribution;
- source URL, publisher, page/table reference and methodology notes;
- confidence/status and last-verified date.

Do not infer provider-level results from state-level studies. Do not compare datasets with incompatible definitions without a warning. If the source only gives salary bands, display bands rather than inventing a mean.

## 8. Data entities (initial)

- User: id, role, email, password_hash, created_at
- LearnerProfile: user_id, education_level, broad_region, district, optional_income_band, preference fields
- Assessment: id, learner_id, version, completed_at
- AssessmentResponse: assessment_id, question_id, response
- Career: id, title, sector, description, skill_tags, source metadata
- Qualification: id, title, awarding_body, NSQF_level, entry_criteria, progression_links, source metadata
- Course/Provider: id, qualification_id, provider_id, duration, eligibility_rule, fee_info, source_url, last_verified_at, confidence
- OutcomeEvidence: id, metric, definition, trade_id, provider_id nullable, geography, cohort_period, numerator, denominator, sample_size, value/bands, unit, source_url, publication_date, methodology, verification_status
- FamilySession: id, learner_id, status, locale, consent metadata
- FamilyParticipant: session_id, user_id, participant_role
- FamilyPreference: session_id, owner_role, option_id, priority_values
- CounsellingMessage: session_id, sender_role, locale, content_reference/retention metadata
- EscalationRequest: id, session_id, concern_category, preferred_contact_method, status, created_at
- FeedbackPulse: session_id, owner_role, confidence_before, confidence_after, optional concern_category, consent flag
- EngagementEvent: pseudonymous session id, event_type, timestamp, consent flag
- RecommendationRun/Item: student/assessment/model version, eligibility status, score and factor breakdown
- Report: id, recommendation_run_id, generated_at, storage reference

## 9. AI and counselling guardrails

- Retrieve only from approved, source-linked records.
- Provide the source date, geographic scope and cohort when quoting outcomes.
- Say "no verified local/provider-level data found" when that is the case.
- Never fabricate income, placement, safety or job-security claims.
- Do not infer a family's financial status beyond the optional broad band they provide.
- Do not infer or label an individual's emotional state from their text, voice or face.
- Escalate unresolved, high-stakes or highly personal concerns to a human counsellor workflow.
- Make it clear that the tool supports, but does not decide, the family's choice.

## 10. Acceptance criteria

- A synthetic learner can complete an assessment and receive eligibility-safe, explainable recommendations.
- English and Marathi are available for the main pilot journey.
- A parent can join a shared session and submit separate preferences.
- Course and qualification pages show source and verification metadata.
- Outcome metrics display their definition, cohort, geography, sample/denominator and source.
- State-level or historical outcomes are never presented as current provider-specific guarantees.
- The family flow can create and track a counsellor escalation request.
- The admin dashboard shows only aggregate engagement/concern data and suppresses small groups.
- A simplified, low-jargon journey works on mobile and desktop.
- The PDF report includes evidence, limitations and source links.
- Tests cover eligibility, recommendation determinism, metric semantics, family access and analytics privacy.
