# Architecture (Target)

## High-level components

```text
[Streamlit multilingual, low-jargon UI]
        | HTTP / JSON
        v
[FastAPI application]
        +--> Authentication, family consent & authorisation
        +--> Learner profile and assessment
        +--> Eligibility + explainable recommendation service
        +--> Qualification/course/provider catalogue
        +--> Outcome evidence service (metric definitions + provenance)
        +--> Shared family counselling session
        +--> Counsellor escalation queue
        +--> Report service
        +--> Grounded multilingual AI service
        +--> Privacy-safe aggregate analytics
        |
        v
[SQLAlchemy repositories]
        |
        +--> SQLite local
        +--> PostgreSQL deployment
        |
        +--> Curated qualification/outcome evidence records
```

## Domain boundaries

- UI: accessible presentation, locale selection and interaction.
- API: request validation, authentication, authorisation and response contracts.
- Domain services: eligibility, scoring, family preference comparison, outcome-metric validation and escalation.
- Persistence: SQLAlchemy models and repositories.
- Data ingestion: CSV/JSON import with schema validation, source metadata and file hash.
- AI integration: retrieval over approved records; LLM generates explanations only from supplied evidence.
- Analytics: opt-in event and feedback aggregation; no individual emotion profiling.

## Recommendation flow

1. Load assessment version and learner profile.
2. Evaluate each qualification/course: eligible, ineligible or unknown.
3. Exclude ineligible options from eligible ranking.
4. Calculate deterministic weighted preference match for remaining options.
5. Return factor breakdown, source/eligibility explanation and confidence metadata.
6. Persist model version and input references.

## Outcome evidence flow

1. Import only an authorised dataset or curated official source record.
2. Validate metric definitions, denominator/sample size, cohort, geography, units and provenance.
3. Mark record verified, needs_review, stale or synthetic_demo.
4. Query only evidence matching the requested scope.
5. Display source date, cohort and geographic granularity; disclose gaps rather than extrapolate.

## Family counselling flow

1. Learner starts a session and authorises a parent/guardian invitation.
2. Each participant joins with a distinct role and consent state.
3. Both participants ask questions in the shared session.
4. Retrieval selects qualification, outcome and progression evidence.
5. AI responds in the selected locale with source references and uncertainty.
6. Either participant may request human counsellor follow-up.
7. Optional feedback pulses are aggregated for the admin dashboard.

## Security and privacy boundaries

- Enforce permissions in the API, not only in UI.
- Store password hashes; secrets live in environment variables.
- Family links grant only explicitly scoped shared data.
- Collect broad income bands only if needed; do not require exact income or address.
- Use synthetic profiles and outcome fixtures in development.
- Do not store full chat transcripts by default; define retention and consent before production.
- Analytics must be aggregate, consent-aware and suppress small groups.
- Treat AI output as untrusted; validate source references and never infer emotional state from voice/face.

## Deployment target

A Python-compatible host for Streamlit and FastAPI, PostgreSQL for persistent deployment, HTTPS, environment-based secrets, CI checks and clear service-health monitoring.
