# PathSaathi AI

**SIH26241 — AI-enabled career counselling and family decision-support for vocational education.**

PathSaathi AI is a Python-first portfolio project that helps learners and families explore vocational pathways together using source-linked qualification and outcome evidence, bilingual counselling, human escalation and privacy-safe scheme analytics.

> This is a decision-support prototype, not a guarantee of admission, employment, placement, safety or salary outcomes.

## Why this project

The SIH challenge asks for a joint learner-parent counselling experience that addresses family concerns with credible local evidence, explains vocational progression in accessible language, supports regional languages, enables human escalation and gives administrators privacy-safe insight into engagement and parental concerns.

See [SIH requirement mapping](docs/PROBLEM_STATEMENT_MAPPING.md) and [project research](docs/PROJECT_RESEARCH.md).

## MVP focus

- English + Marathi pilot interface (Maharashtra scope assumption, subject to mentor confirmation).
- Guided learner profile capture and transparent advisory pathway shortlisting; no validated aptitude or psychometric testing.
- Qualification/course explorer with NCVET/NQR provenance.
- Outcome evidence model preserving trade/provider/region/cohort granularity and metric definitions.
- Guided joint learner-parent conversation with role-separated questions, parent self-reported concerns and a session-only review; persistent shared sessions and consent are Phase 5.
- Retrieval-grounded AI explanations with source links and explicit unknowns.
- Counsellor callback/follow-up request queue until a real partner is connected.
- Aggregate admin analytics based on opt-in events and self-reported feedback.
- PDF report, automated tests, CI and deployment documentation.

## Technology

Python 3.12+, Streamlit, FastAPI, SQLAlchemy 2.x, SQLite for local development, PostgreSQL-compatible connection configuration, Pytest, Ruff and GitHub Actions. Pandas is planned for the outcome-data ingestion phase. The optional postgres extra installs the Psycopg 3 driver.

## Delivery window

The owner-approved delivery window is **60 calendar days: 2 November–31 December 2026**. The final day is 31 December 2026; the plan is not extendable to 100 or 120 days without explicit owner approval.

| Phase | Project days | Dates |
|---|---:|---|
| Research and requirements | 1–5 | 2–6 Nov |
| Foundation | 6–12 | 7–13 Nov |
| Counselling/profile/pathway | 13–22 | 14–23 Nov |
| Course/outcome explorer | 23–29 | 24–30 Nov |
| Family counselling/escalation | 30–36 | 1–7 Dec |
| AI and reporting | 37–41 | 8–12 Dec |
| Admin analytics, quality and privacy | 42–47 | 13–18 Dec |
| Portfolio release | 48–60 | 19–31 Dec |

See the [60-day roadmap](ROADMAP.md) for exit criteria and verified progress, [database setup](docs/DATABASE.md) for local persistence configuration, and the [read-only API contract](docs/API.md) for endpoint, evidence-display and local smoke-test behaviour.

## Current status

**Phase 1 and Phase 2 foundation gates are complete; Phase 3 is in progress (Day 20/60).** The bilingual learner/parent profile journey and transparent advisory shortlisting are implemented. Only verified-eligible preference matches enter the eligible shortlist; unknown matches are shown for verification and ineligible options remain explorable. The pathways page includes one source-backed national NQR example: Assistant Baking Technician (Food Processing, NSQF Level 3), with job-role details, four alternative entry routes, learning modules, 300-hour duration and published progression to Plant Biscuit Production Specialist (NSQF Level 4). NQR lists the record as valid through 26 August 2027; the record and qualification file were checked on 17 November 2026. PR #36 is merged as commit 8f681248; its PR run #165, merged-main run #166 and documentation-sync run #167 passed compilation, Ruff, 176 Pytest tests and the live Streamlit/FastAPI smoke test (one existing Starlette/httpx deprecation warning). A separate multi-route evaluator now models the four entry routes as OR alternatives with AND conditions, preserves unknowns for missing or unverified learner evidence, and provides English/Marathi explanations. It stores age only as completed years and does not store employer names. PR #38 merged as commit c1e659a; PR Actions run #168 and merged-main run #169 both passed Python compilation, Ruff, 192 Pytest tests and the live Streamlit/FastAPI smoke test (one existing Starlette/httpx deprecation warning per run). Issue #37 is closed. The pathways page now renders route-by-route eligibility explanations for the NQR example, reusing only the education level from a saved session-only learner profile. Age, prior qualification and experience are not collected by this screen, so those conditions remain unknown until independently supplied and verified. This is not a local provider offer; no seats, fees, district availability or employment outcomes are inferred. Marathi wording is a draft pending fluent human review. Fractional NSQF levels (for example 2.5) are preserved as exact Decimal values in the domain and SQLite/PostgreSQL-ready persistence model. PR #39 merged as commit 493024c; merged-main Actions run #177 passed Python compilation, Ruff, 197 Pytest tests and the live Streamlit/FastAPI smoke check (one existing Starlette/httpx deprecation warning). A new Family conversation page adds six deterministic bilingual prompts for learner questions/preferences, parent self-reported concerns/information needs and a shared discussion topic, followed by a role-separated review with skip, Back, Continue and revise controls. Empty, skipped, unanswered and revised responses remain distinguishable; the draft is session-only and makes no API, database, counsellor, analytics or LLM calls. Marathi wording is labelled as draft pending human review. PR #41 merged into main as `0f03eb3`; PR validation runs #181, #182 and #183 passed compilation, Ruff, 211 Pytest tests and the live Streamlit/FastAPI smoke test (one existing Starlette/httpx deprecation warning). Role ownership is prompt-defined, not identity-authenticated; this single-session prototype does not capture consent or create persistent shared sessions. The family conversation review now also displays saved learner education, broad region, interests and work preferences separately from parent/guardian self-reported concerns and priorities. Missing profile context is labelled not provided; profile values never prefill or overwrite prompt-ID answers. PR #43 merged as `e8b7f4f`; PR run #187 and merged-main run #188 passed compilation, Ruff, 214 Pytest tests and the live Streamlit/FastAPI smoke check (one existing Starlette/httpx deprecation warning per run).

The local default database URL is sqlite:///./data/pathsaathi.db. The application creates tables only when the explicit create_schema() helper is called; importing the API does not create a database or connect to a hosted service. PATHSAATHI_DATABASE_URL can be set to a PostgreSQL URL, with the optional Psycopg driver installed when needed.

Production PostgreSQL provisioning and application deployment are reserved for Phase 8. Local SQLite is part of Phase 2 and is not blocked by the production-hosting gate.

## Project documentation

- [Software Requirements Specification](docs/SRS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [SIH requirement mapping](docs/PROBLEM_STATEMENT_MAPPING.md)
- [Outcome data contract](docs/OUTCOME_DATA_CONTRACT.md)
- [Data-source policy](docs/DATA_SOURCE_POLICY.md)
- [Repository contracts](docs/REPOSITORY_CONTRACTS.md)
- [Database setup](docs/DATABASE.md)
- [Read-only catalogue API and local smoke check](docs/API.md)
- [Phase 3 learner/parent profile and eligibility domain](docs/PHASE3_PROFILE_DOMAIN.md)
- [Phase 3 source-backed NQR qualification explainers](docs/PHASE3_QUALIFICATION_EXPLAINERS.md)
- [Phase 3 multi-route eligibility](docs/PHASE3_MULTI_ROUTE_ELIGIBILITY.md)
- [Phase 3 joint counselling prompts](docs/PHASE3_JOINT_COUNSELLING.md)
- [Accessibility implementation review](docs/ACCESSIBILITY_REVIEW.md)

## Data integrity and limitations

- The authorised SIH dummy placement/earnings dataset has not yet been supplied. Synthetic fixtures are labelled and are never presented as real outcomes.
- Placement, employment, trade-related employment, apprenticeship and self-employment remain separate metrics.
- Every outcome claim must retain its definition, denominator, cohort, geography, period and provenance where available.
- Unknown earnings, placement and qualification values remain unknown.
- Eligibility is a hard gate when official entry criteria are known; unknown is not eligible.
- Pathway shortlisting is advisory, not a validated aptitude or psychometric assessment.
- Learner and parent preferences remain distinct. Human escalation is a request queue until a real service is connected. The current family conversation labels fixed prompt roles but does not authenticate participants; consent and persistent shared-session handling remain Phase 5 work.
- Use optional self-report for concern changes; no covert emotion inference.
- Do not use real student/family data in development. Production use involving minors requires consent, retention and legal/privacy review.

## Local setup

Requires Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run the network-level API/Streamlit health-client smoke check:

```bash
python scripts/smoke_test.py
```

The check starts FastAPI on an ephemeral local port and verifies that the Streamlit health client reports offline before startup, online while the API is serving, and offline after shutdown. It uses the database-independent health route and does not create a SQLite database or schema.

For manual UI use, start the API in one terminal:

```bash
uvicorn backend.main:app --reload
```

In a second terminal:

```bash
streamlit run app/streamlit_app.py
```

The local SQLite URL defaults to sqlite:///./data/pathsaathi.db. To create the schema explicitly for database-backed local development:

```bash
python -c "from database.session import create_database_engine, create_schema; engine = create_database_engine(); create_schema(engine); engine.dispose()"
```

To configure PostgreSQL later, install the optional driver and set a secret-managed URL:

```bash
pip install -e ".[postgres]"
export PATHSAATHI_DATABASE_URL="postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME"
```

Do not commit database credentials. No managed production database is required for current development.

The Streamlit sidebar checks the API at http://127.0.0.1:8000/health. Set PATHSAATHI_API_URL to an absolute HTTP(S) base URL when the API runs elsewhere; do not include credentials, a query string or a fragment. Blank or malformed configuration is treated as offline without a network request. If the API is unavailable, the UI shows a status warning but keeps the informational shell available.

Run checks with:

```bash
ruff check .
pytest -q
python scripts/smoke_test.py
```

The API health endpoint is at http://127.0.0.1:8000/health. The Streamlit UI is at http://localhost:8501.

## License

MIT. See LICENSE.
