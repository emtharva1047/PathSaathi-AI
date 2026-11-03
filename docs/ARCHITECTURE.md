# PathSaathi AI — Target Architecture

## High-level system

~~~text
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
  |-- In-memory adapters for deterministic tests/demo fixtures
  |-- SQLAlchemy adapters for local SQLite and PostgreSQL-compatible URLs
  v
[Course, qualification and outcome records]

[AI provider] is called only with retrieved, relevant evidence; deterministic core flows
remain available when the provider is unavailable.
~~~

## Persistence and deployment sequence

### Phase 2: local persistence foundation

- SQLAlchemy 2.x declarative models represent course/qualification and outcome-evidence records.
- SQLite is the default local database at sqlite:///./data/pathsaathi.db.
- PATHSAATHI_DATABASE_URL accepts another SQLAlchemy URL, including PostgreSQL with the optional Psycopg 3 driver.
- Engine and session creation are explicit helpers. Importing the API or database package must not open a connection or create tables.
- create_schema(engine) is an explicit local-development/test helper; production schema changes must use controlled migrations.
- Repository adapters preserve the same storage-independent contracts as the in-memory implementations.
- Local database tests use isolated in-memory SQLite databases.

### Phase 8: production release

- Provision managed PostgreSQL only during the release phase, after product workflows and data validation are ready.
- Add and verify Alembic migrations, indexes, transaction handling, connection pooling, secret management and backup/restore notes.
- Deploy FastAPI and Streamlit separately to compatible hosts. Do not assume Streamlit itself runs as a native Vercel application.
- Configure HTTPS, CORS, environment variables, health checks and smoke tests.
- Verify the complete UI → API → PostgreSQL journey before calling the product deployed.

## Main flows

### 1. Joint counselling
1. Learner starts a session and selects English or Marathi.
2. Parent joins through an authorised invitation or shared session flow.
3. Participants' roles remain distinguishable.
4. The application gathers broad context and concern categories.
5. The orchestrator retrieves outcome and progression evidence using trade/provider/region filters.
6. The AI explains retrieved facts in low-jargon language, including sample/period caveats.
7. Unanswered or sensitive concerns can be escalated to a human.

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
- Persistence: SQLAlchemy models and repositories are available in Phase 2; SQLite is the local default. Production PostgreSQL provisioning and migrations belong to Phase 8.

## Security and privacy

- Enforce access server-side.
- Keep exact household income out of scope; use optional broad brackets.
- Keep learner and parent preference/concern entries attributed by role.
- Minimise raw conversation retention.
- Use aggregate views, consent and small-cohort suppression for scheme analytics.
- Do not use real student or family data in development.

## Deployment

Production release is a Phase 8 task. Host FastAPI and Streamlit as separate Python services, use managed PostgreSQL, HTTPS, environment-based secrets, logging without sensitive message contents, CI checks and a documented demo dataset clearly marked as synthetic until SIH data is supplied.