# PathSaathi AI

**SIH26241 — AI-enabled career counselling and family decision-support for vocational education.**

PathSaathi AI is a Python-first portfolio project that helps learners and families explore vocational pathways together using source-linked qualification and outcome evidence, bilingual counselling, human escalation and privacy-safe scheme analytics.

> This is a decision-support prototype, not a guarantee of admission, employment, placement, safety or salary outcomes.

## Why this project

The SIH challenge asks for a joint learner-parent counselling experience that addresses family concerns with credible local evidence, explains vocational progression in accessible language, supports regional languages, enables human escalation and gives administrators privacy-safe insight into engagement and parental concerns.

See [SIH requirement mapping](docs/PROBLEM_STATEMENT_MAPPING.md) and [project research](docs/PROJECT_RESEARCH.md).

## MVP focus

- English + Marathi pilot interface (Maharashtra scope assumption, subject to mentor confirmation).
- Guided learner assessment and advisory pathway shortlisting.
- Qualification/course explorer with NCVET/NQR provenance.
- Outcome evidence model preserving trade/provider/region/cohort granularity and metric definitions.
- Shared learner-parent counselling session with separate preferences.
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

See the [60-day roadmap](ROADMAP.md) for exit criteria and verified progress, and [database setup](docs/DATABASE.md) for local persistence configuration.

## Current status

**Phase 1 requirements baseline is complete; Phase 2 foundation is in progress.** The repository contains the Python project scaffold, FastAPI health endpoint, English/Marathi navigation, resilient API-status indicator, shared logging/error handling, typed course/outcome domain records, storage-independent repository contracts, SQLAlchemy models and SQLite-backed repository adapters.

The local default database URL is sqlite:///./data/pathsaathi.db. The application creates tables only when the explicit create_schema() helper is called; importing the API does not create a database or connect to a hosted service. PATHSAATHI_DATABASE_URL can be set to a PostgreSQL URL, with the optional Psycopg driver installed when needed.

Production PostgreSQL provisioning and application deployment are reserved for Phase 8. Local SQLite is part of Phase 2 and is not blocked by the production-hosting gate.

## Data integrity and limitations

- The authorised SIH dummy placement/earnings dataset has not yet been supplied. Synthetic fixtures are labelled and are never presented as real outcomes.
- Placement, employment, trade-related employment, apprenticeship and self-employment remain separate metrics.
- Every outcome claim must retain its definition, denominator, cohort, geography, period and provenance where available.
- Unknown earnings, placement and qualification values remain unknown.
- Eligibility is a hard gate when official entry criteria are known; unknown is not eligible.
- Pathway shortlisting is advisory, not a validated aptitude or psychometric assessment.
- Learner and parent preferences remain distinct. Human escalation is a request queue until a real service is connected.
- Use optional self-report for concern changes; no covert emotion inference.
- Do not use real student/family data in development. Production use involving minors requires consent, retention and legal/privacy review.

## Local setup

Requires Python 3.12+.

~~~
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn backend.main:app --reload
~~~

In a second terminal:

~~~
streamlit run app/streamlit_app.py
~~~

The local SQLite URL defaults to sqlite:///./data/pathsaathi.db. To create the schema explicitly for local development:

~~~
python -c "from database.session import create_database_engine, create_schema; create_schema(create_database_engine())"
~~~

To configure PostgreSQL later, install the optional driver and set a secret-managed URL:

~~~
pip install -e ".[postgres]"
export PATHSAATHI_DATABASE_URL="postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME"
~~~

Do not commit database credentials. No managed production database is required for current development.

The Streamlit sidebar checks the API at http://127.0.0.1:8000/health. Set PATHSAATHI_API_URL when the API runs at another base URL. If the API is unavailable, the UI shows a status warning but keeps the informational shell available.

Run checks with:

~~~
ruff check .
pytest -q
~~~

The API health endpoint is at http://127.0.0.1:8000/health. The Streamlit UI is at http://localhost:8501.

## License

MIT. See LICENSE.