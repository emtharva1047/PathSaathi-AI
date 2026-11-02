# PathSaathi AI — Target Architecture

## High-level system

```text
[Streamlit learner + parent interface]
  |-- English / Marathi locale
  |-- Guided, low-jargon interaction
  |-- Shared family counselling session
  v
[FastAPI application]
  |-- Authentication, roles and consent
  |-- Family session/conversation orchestration
  |-- Context profile (broad region, education, income bracket)
  |-- Trade/provider outcome retrieval
  |-- Job-role and NSQF progression explainer
  |-- Human counsellor escalation
  |-- Concern check-ins and engagement events
  |-- Report generation
  |-- Scheme-admin analytics API
  v
[Domain services]
  |-- Outcome data validation and calculation
  |-- Evidence retrieval and freshness checks
  |-- Prompt/context assembly and grounded answer validation
  |-- Privacy aggregation and small-cohort suppression
  v
[Repository interfaces]
  |-- Pre-Phase 4: CSV, fixture and in-memory adapters only
  |-- After Phase 4: SQLAlchemy repositories and managed PostgreSQL
  v
[Verified course and outcome records]

[AI provider] is called only with retrieved, relevant evidence; the core app remains useful if it is unavailable.
```

## Persistence and deployment gate

Persistent storage is intentionally not part of the Phase 2 foundation. Before Phase 4 exit criteria are met, the application must use fixture-backed or in-memory adapters and validated CSV workflows. Do not create a database engine, connect to SQLite/PostgreSQL, provision a hosted database or deploy the application during Phases 2–4.

After Phase 4 sign-off, add SQLAlchemy, Alembic and managed PostgreSQL as tracked in [issue #11](https://github.com/emtharva1047/PathSaathi-AI/issues/11). The FastAPI API is planned for Vercel; the Streamlit interface requires a separate Streamlit-compatible host.

## Main flows

### 1. Joint counselling
1. Learner starts a session and selects English or Marathi.
2. Parent joins through an authorised invitation or shared session flow.
3. Participants' roles remain distinguishable.
4. The application gathers broad context and concern categories.
5. The orchestrator retrieves outcome and progression evidence using trade/provider/region filters.
6. The AI explains retrieved facts in low-jargon language, including sample/period caveats.
7. Unanswered or sensitive concerns can be escalated to a human counsellor.

### 2. Outcome data
- Import SIH-provided dummy data through a versioned CSV/JSON contract.
- Validate data types, units, counts, denominators, missingness and provenance.
- Calculate rates only when numerator and denominator definitions are compatible.
- Query with trade/provider/region/cohort/time filters.
- Present source, sample size, date and limitations next to each figure.

### 3. NSQF progression
- Store qualifications and progression links as sourced records.
- Render a graph/list of verified next-level and further-education routes.
- If no verified edge exists, display no data rather than generating a plausible route.

### 4. Admin analytics
- Derive engagement funnel and concern-theme aggregates.
- Compare explicit self-reported pre/post concern ratings.
- Restrict access and suppress cohorts smaller than a configurable privacy threshold.
- Never expose raw chat transcripts or household identities in general admin views.

## Component boundaries
- UI: presentation, language selection and accessible guided interactions.
- API: validation, role checks, consent and response contracts.
- Domain services: outcome calculations, NSQF mapping, concern tracking, aggregation and escalation.
- Data import: schema versioning, provenance, validation and audit.
- AI integration: retrieval-grounded explanation, not a source of unverified statistics.
- Persistence: introduced only after Phase 4; SQLAlchemy models and repositories use managed PostgreSQL.

## Security and privacy
- Enforce access server-side.
- Keep exact household income out of scope; use optional broad brackets.
- Keep learner and parent preference/concern entries attributed by role.
- Minimise raw conversation retention.
- Use aggregate views, consent and small-cohort suppression for scheme analytics.
- Do not use real student or family data in development.

## Deployment
After Phase 4 and database integration, host FastAPI and Streamlit as separate Python services. Use managed PostgreSQL for deployed persistence, HTTPS, environment-based secrets, logging without sensitive message contents, CI checks and a documented demo dataset clearly marked as synthetic until SIH data is supplied.
