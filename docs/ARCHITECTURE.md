# Architecture (Target)

```text
[Streamlit multipage UI]
        | HTTP / JSON
        v
[FastAPI application]
        +--> Authentication & authorisation
        +--> Assessment service
        +--> Eligibility + recommendation service
        +--> Course/career catalogue service
        +--> Family decision service
        +--> Report service
        +--> Grounded AI service -> source-linked records -> LLM explanation
        v
[SQLAlchemy repositories]
        v
[SQLite local / PostgreSQL deployment]
```

## Boundaries
- UI: presentation and interaction.
- API: request validation, authentication, response contracts.
- Domain services: eligibility, scoring, family comparison and reports.
- Persistence: SQLAlchemy models and repositories.
- Integrations: LLM provider and optional external data import.
- Data layer: controlled catalogue with provenance.

## Recommendation flow
1. Load assessment version and student profile.
2. Evaluate each option: eligible, ineligible or unknown.
3. Exclude ineligible options from eligible ranking.
4. Calculate deterministic weighted preference match for remaining options.
5. Return factor breakdown, explanation and data-confidence metadata.
6. Persist model version and input references.

## Security boundaries
- Enforce permissions in the API, not only in UI.
- Store password hashes; secrets live in environment variables.
- Family links grant only explicitly scoped shared data.
- Use synthetic profiles in tests and demos.
- Treat AI output as untrusted; constrain it to retrieved evidence and validate sources.

## Deployment target
A Python-compatible host for Streamlit and FastAPI, PostgreSQL for persistent production data, HTTPS, environment-based secrets and CI-based checks.
