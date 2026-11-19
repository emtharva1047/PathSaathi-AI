# Phase 3 — Multi-route qualification eligibility

**Implementation slices:** Day 17 (18 November) and Day 18 (19 November 2026)  
**Scope:** Deterministic, provenance-backed evaluation of alternative qualification entry routes. This is advisory screening, not an admission decision.

## Route semantics

The domain model in core/multi_route_eligibility.py treats each published alternative entry route as an OR branch. Every condition within a route is an AND requirement.

- A route is eligible only when every condition is met.
- A route is ineligible only when every condition has been evaluated and at least one condition is not met.
- A route is unknown when any required fact or source is missing, stale or unverified.
- A qualification is eligible when at least one complete route is met.
- A qualification is ineligible only when every alternative route is conclusively not met.
- A qualification is unknown in all other cases.

This is deliberately conservative. An unknown route is never converted into a failure or a successful match.

## Curated NQR example

The data file data/qualifications/assistant_baking_technician_entry_routes.json records the four alternative routes published for Assistant Baking Technician:

| Route | AND conditions |
|---|---|
| Grade 10 | Grade 10 pass + minimum age 16 |
| Grade 8 | Grade 8 pass + 36 months relevant Food Industry experience + minimum age 16 |
| Prior NSQF 2.5 | Verified relevant prior qualification at NSQF 2.5 or above + 18 months relevant Food Industry experience + minimum age 16 |
| Prior NSQF 2 | Verified relevant prior qualification at NSQF 2 or above + 36 months relevant Food Industry experience + minimum age 16 |

Every condition carries its exact qualification-file source location, publisher, URL and verification date. The record preserves the exact qualification code/version and NQR validity date.

Sources:
- [NQR record 12209](https://www.nqr.gov.in/qualifications/12209)
- [Assistant Baking Technician qualification file](https://www.nqr.gov.in/qualification/file/English%20Q-file%20Baking%20Tech..pdf), Section 1, items 9(a)-9(b), page 3.

The NQR record and qualification file were checked on 17 November 2026. The qualification record lists validity through 26 August 2027.

## Learner evidence and privacy

LearnerEligibilityEvidence accepts only the minimum route-screening facts:

- Normalized education level.
- Age in completed years (not date of birth).
- Prior qualification code/version, NSQF level, verified relevance and source provenance.
- Relevant experience category and total verified months, with an opaque evidence reference.

No employer names, exact address, date of birth, identity document number or contact information is stored. Experience is represented as one non-overlapping total per industry category; the evaluator does not add potentially overlapping jobs or periods.

A missing tuple (None) means the learner has not supplied that information. An explicitly empty tuple means the learner reported none. Self-reported or unverified prior qualification/experience evidence remains unknown until verified. Prior qualification equivalence must be explicitly confirmed; a numeric NSQF level alone does not establish relevance.

Age is used as a reported completed-year value for preliminary screening. A provider or awarding body may still require documentary verification.

## Assistant Baking Technician behaviour

All four published routes are represented. The qualification remains unknown for an empty learner evidence record. It can produce a preliminary eligible result only when every condition of at least one route is met by the supplied evidence.

The previous education-only evaluator in core/eligibility.py remains unchanged and is not used to collapse these routes into a single Grade 10 check.

The evaluator returns English and Marathi condition-level and overall explanations, reason codes, missing-information labels and source provenance. Marathi strings are draft translations pending human review.

## Limitations

- This is not a provider admission decision or a guarantee of enrolment.
- Learner evidence may require verification by the awarding body or provider.
- The pathways eligibility panel reuses only the education level from a profile explicitly saved in the current Streamlit session. It deliberately does not collect age, prior qualifications or experience; those conditions remain unknown until the facts are independently supplied and verified.
- No local course availability, seats, fees, salary, placement or employment claims are inferred.
- No aptitude, psychometric, admission, employment or earnings prediction is produced.

## Validation

Tests cover OR/AND route semantics, Grade 10 and Grade 8 routes, NSQF 2.5 and 2.0, half-level precision, experience thresholds, minimum age, missing/unverified evidence, stale/expired criteria, source provenance, bilingual explanations and privacy-minimized inputs.


## Streamlit eligibility explanation

The pathways page now renders the multi-route result immediately after the source-backed qualification explainer.

- It reads only the saved session-only learner education level. An unsaved draft is not used.
- It does not add inputs for age, date of birth, prior qualification documents, employer names or work history.
- It displays the overall eligible / ineligible / unknown result, every alternative route, every AND condition, the bilingual condition explanation and the exact qualification-file source reference/link.
- With the current profile schema, age, prior qualification and experience are absent. The Assistant Baking Technician example therefore remains unknown; a saved Grade 10 profile can satisfy the Grade 10 education condition, but the missing minimum-age condition keeps that route unknown.
- Criteria that are expired or not currently source-verified are displayed as unknown rather than assessed against learner facts.
- The screen explicitly describes this as preliminary advisory screening, not an admission decision. No learner evidence is written to the API or database.

Automated rendering tests cover an empty profile, a saved Grade 10 profile, English and Marathi explanations, all four routes, exact source links and expired criteria. They do not establish human Marathi quality or accessibility conformance; issue #14 remains open.
