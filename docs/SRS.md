# Software Requirements Specification (SRS)

## 1. Purpose
Specify a portfolio MVP for PathSaathi AI, a vocational career counselling and family decision-support platform for students in India.

## 2. Product scope
The platform collects student preferences and educational context, applies explicit eligibility rules, ranks suitable vocational pathways using an explainable scoring model, provides source-linked course information, supports family discussion, and generates reports. The platform offers guidance, not a final or binding career decision.

## 3. User classes

### Student
Creates a profile, completes an assessment, explores recommendations, compares courses, invites/links a parent or guardian, and views a report.

### Parent/guardian
With student-authorised linking and appropriate consent, views shared recommendations, records their own priorities, and participates in comparisons.

### Counsellor
Reviews assessment summaries and adds human feedback. The counsellor does not silently alter student responses.

### Administrator
Maintains course/career reference data and its source metadata.

## 4. Functional requirements
- FR-01: The system shall allow a student profile to record education level, relevant subjects/qualifications, broad location, interests, skills/confidence indicators, preferences and practical constraints.
- FR-02: The system shall present a structured assessment and preserve the response version used for a recommendation.
- FR-03: The system shall evaluate course eligibility using explicit rules and return eligible, ineligible or unknown; unknown eligibility must not be represented as eligible.
- FR-04: The recommendation engine shall rank only eligible options unless the UI clearly separates exploratory options with unknown eligibility.
- FR-05: Each recommendation shall show its factors, weights, data limitations and explanation.
- FR-06: Recommendation weights shall be configurable and documented as prototype assumptions pending counsellor validation.
- FR-07: Course records shall include provider/title, qualification level where known, duration where known, eligibility, source URL, last-verified date and data-confidence status.
- FR-08: Users shall search, filter, view and compare course/career options.
- FR-09: A student shall be able to link a parent/guardian through a consent-aware flow.
- FR-10: Student and parent preferences shall be stored separately.
- FR-11: The family decision view shall show preference alignment, disagreements and trade-offs without declaring one party the winner.
- FR-12: The AI counsellor shall retrieve relevant platform records and provide grounded answers with source references where available.
- FR-13: The AI counsellor shall state when evidence is missing or stale and shall not invent admission, fee, salary or placement facts.
- FR-14: The system shall generate a PDF report containing profile summary, recommendations, matching explanation, relevant source links, uncertainty and next steps.
- FR-15: Counsellors/admins shall have appropriately restricted access to review or maintain reference data.

## 5. Non-functional requirements
- NFR-01 Security: passwords must be hashed; secrets supplied through environment variables; access to linked family records authorised server-side.
- NFR-02 Privacy: collect minimum necessary data; use synthetic development data; provide data deletion; document consent and retention.
- NFR-03 Explainability: all match scores must be decomposable into documented factors.
- NFR-04 Reliability: validation errors should be clear; unavailable AI services must not break deterministic recommendations.
- NFR-05 Maintainability: separate UI, API, domain logic, persistence and integration layers.
- NFR-06 Testability: core eligibility and scoring functions must be deterministic and independently unit-testable.
- NFR-07 Accessibility: forms have labels, errors and keyboard-usable controls.
- NFR-08 Portability: reproducible local setup and environment-based configuration.
- NFR-09 Provenance: factual course claims carry source URLs and verification dates.
- NFR-10 Safety: never guarantee employment, salary, admission or outcomes.

## 6. Recommendation model requirements
Eligibility is a hard filter. A course may be marked eligible only when all required criteria are satisfied by available profile data. Missing student or course data results in unknown.

The MVP can use a transparent weighted match across interest alignment, skill alignment, work-style preference, progression preference and practical fit. Initial weights are prototype assumptions, configurable and versioned. Eligibility is not merely a weighted dimension.

## 7. Data entities (initial)
- User: id, role, email, password_hash, created_at
- StudentProfile: user_id, education_level, location_region, profile fields
- Assessment: id, student_id, version, completed_at
- AssessmentResponse: assessment_id, question_id, response
- Career: id, title, sector, description, skill_tags, source metadata
- Course: id, career_id, title, provider, level, duration, eligibility_rule, fee_info, source_url, last_verified_at, confidence
- RecommendationRun: id, student_id, assessment_id, model_version, created_at
- RecommendationItem: run_id, career_id/course_id, eligibility_status, score, factor_breakdown
- FamilyLink: student_id, parent_user_id, status, consent metadata
- FamilyPreference: family_link_id, owner_role, option_id, priority_values
- Report: id, recommendation_run_id, generated_at, storage reference

## 8. Acceptance criteria
- A synthetic student profile can complete an assessment.
- Eligibility rules correctly distinguish eligible/ineligible/unknown.
- Recommendation ordering is deterministic for a fixed profile, dataset and model version.
- Reasons and factor breakdown are visible.
- Course explorer exposes source and verification metadata.
- Student and parent can submit separate preference sets.
- Family comparison correctly displays agreements and differences.
- AI answers cite retrieved records or explicitly say when information is unavailable.
- PDF report includes caveats and source links.
- Automated tests and CI pass.
