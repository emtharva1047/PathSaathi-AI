# PathSaathi AI

**SIH26241 — AI-enabled career counselling and family decision-support for vocational education.**

PathSaathi AI is a Python-first portfolio project that helps learners and families explore vocational pathways together using source-linked qualification and outcome evidence, bilingual counselling, human escalation and privacy-safe scheme analytics.

> This is a decision-support prototype, not a guarantee of admission, employment, placement, safety or salary outcomes.

## Why this project

The SIH challenge asks for a joint learner-parent counselling experience that addresses family concerns with credible local evidence, explains vocational progression in accessible language, supports regional languages, enables human escalation and gives administrators privacy-safe insight into engagement and parental concerns.

See [SIH requirement mapping](docs/PROBLEM_STATEMENT_MAPPING.md) and [project research](docs/PROJECT_RESEARCH.md).

## MVP focus

- English + Marathi pilot interface (Maharashtra scope assumption).
- Guided learner assessment and advisory pathway shortlisting.
- Qualification/course explorer with NCVET/NQR provenance.
- Outcome evidence model preserving trade/provider/region/cohort granularity and metric definitions.
- Shared learner-parent counselling session with separate preferences.
- Retrieval-grounded AI explanations with source links and explicit unknowns.
- Counsellor escalation request queue.
- Aggregate admin analytics based on opt-in events and self-reported feedback.
- PDF report, tests, CI and deployment documentation.

## Technology

Python 3.12+, Streamlit, FastAPI, Pytest, Ruff and GitHub Actions. Pandas is planned for the outcome-data ingestion phase. SQLAlchemy, Alembic and managed PostgreSQL are deliberately deferred until after Phase 4; no database engine or persistent database connection is part of the current foundation.

## Current status

**Phase 1 complete. Phase 2 foundation in progress.** The repository contains the Python project scaffold, FastAPI health endpoint, English/Marathi navigation, a resilient API-status indicator, shared logging/error handling and an initial CI pipeline. The UI remains usable as a demo when the API is unavailable.

The nominal delivery target is **100 calendar days**, with a **120-day hard maximum**. Development is planned as one iteration every 36 hours, targeting 2–3 focused hours per iteration. These are planning targets, not a claim that an automation run occupies that amount of wall-clock time.

Database persistence and production deployment are explicitly scheduled after Phase 4. Before then, use validated CSVs, fixture-backed repositories and in-memory adapters; do not provision a hosted database or deploy the application.

External dependencies are tracked in GitHub issues: the authorised SIH dummy outcome dataset, and confirmation of the pilot language/region and any live counsellor partner.

- [100-day roadmap](ROADMAP.md)
- [SRS](docs/SRS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [SIH traceability](docs/PROBLEM_STATEMENT_MAPPING.md)
- [Outcome data contract](docs/OUTCOME_DATA_CONTRACT.md)
- [Data-source policy](docs/DATA_SOURCE_POLICY.md)\n- [Repository contracts](docs/REPOSITORY_CONTRACTS.md)

## Engineering principles

- Eligibility is a hard gate when specific qualification criteria are known; unknown is not eligible.
- Pathway shortlisting is advisory, not a validated aptitude or psychometric assessment.
- Every outcome claim carries definition, cohort, geography, sample/denominator and source.
- Never derive provider-level outcomes from state-level studies.
- Use synthetic learner/outcome records for development; never commit real student data.
- AI answers are grounded in approved records; missing evidence is stated plainly.
- Use optional self-report for feedback, not covert emotion inference.
- Minimise personal data and review age-aware consent/legal requirements before production.

## Local setup

Requires Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn backend.main:app --reload
streamlit run app/streamlit_app.py
```

The Streamlit sidebar checks the API at `http://127.0.0.1:8000/health`. Set `PATHSAATHI_API_URL` when the API runs at another base URL. If the API is unavailable, the UI shows a status warning but keeps the informational shell available.

Run checks with:

```bash
ruff check .
pytest -q
```

The API health endpoint is at http://127.0.0.1:8000/health. The Streamlit UI is at http://localhost:8501.

## License

MIT. See LICENSE.
