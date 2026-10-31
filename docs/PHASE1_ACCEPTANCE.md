# Phase 1 Acceptance Checklist

## SIH problem and product scope
- [x] Review the complete SIH26241 problem statement on the official SIH portal.
- [x] Record the challenge's joint learner-parent, bilingual, outcome-data, low-literacy, escalation and admin-analytics requirements.
- [x] Define initial learner cohort: students considering vocational pathways after Class 10 or Class 12, with an extensible model.
- [x] Document Maharashtra + English/Marathi as an MVP pilot assumption, not a sponsor mandate.
- [x] Define explicit exclusions for a solo 60-day build.

## Requirements and architecture
- [x] Update student, parent, counsellor, administrator and data-curator journeys.
- [x] Review functional and non-functional requirements in docs/SRS.md.
- [x] Map official requirements to product modules and acceptance tests.
- [x] Review architecture and initial data entities.
- [x] Review risks: data freshness, outcome metric semantics, translation, privacy, escalation and scope.
- [x] Define recommendation eligibility hard-gate and explainability requirements.

## Data and privacy
- [x] Define qualification source hierarchy using NCVET/NQR and official provider records.
- [x] Define outcome evidence metadata, metric definitions and granularity rules.
- [x] Record SIH listing note that dummy placement/earnings datasets are to be provided for evaluation.
- [x] Prohibit invented values and extrapolation from state-level to provider-level data.
- [x] Define synthetic-only development fixtures and age-aware consent/privacy review.

## Remaining external confirmations (not blockers for the prototype baseline)
- [ ] Confirm with mentor/sponsor whether Maharashtra/Marathi is the preferred pilot context.
- [ ] Obtain the authorised SIH dummy outcome dataset and its usage terms when made available.
- [ ] Confirm whether a real counsellor partner is available for live escalation.

## Sign-off
Phase 1 baseline is ready for implementation planning. External confirmations above remain tracked as integration/data dependencies; they must not be represented as completed.
