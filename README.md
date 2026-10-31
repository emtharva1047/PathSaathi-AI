# PathSaathi AI

**SIH26241 — AI-enabled career counselling and family decision-support for vocational education.**

PathSaathi AI is a Python-first portfolio project that helps learners and families explore vocational pathways together using explainable eligibility-aware matching, source-linked qualification and outcome evidence, bilingual counselling, and a human-escalation workflow.

> This is a decision-support prototype, not a psychometric diagnosis or a guarantee of admission, employment, placement, safety or salary outcomes.

## Why this project

The SIH challenge is not just to recommend a course to a learner. It asks for a joint learner-parent counselling experience that addresses family concerns with credible local evidence, explains vocational progression in accessible language, supports regional languages, enables human escalation and gives administrators privacy-safe insight into engagement and parental concerns.

See [SIH requirement mapping](docs/PROBLEM_STATEMENT_MAPPING.md) and [project research](docs/PROJECT_RESEARCH.md).

## MVP focus

- English + Marathi pilot interface (Maharashtra scope assumption).
- Guided learner assessment and eligibility-aware recommendations.
- Qualification/course explorer with NCVET/NQR provenance.
- Outcome evidence model that preserves trade/provider/region/cohort granularity and metric definitions.
- Shared learner-parent counselling session with separate preferences.
- Retrieval-grounded AI explanations with source links and explicit unknowns.
- Counsellor escalation request queue.
- Aggregate admin analytics based on opt-in events and self-reported feedback.
- PDF report, tests, CI and deployment documentation.

## Planned stack

Python 3.12+, Streamlit, FastAPI, SQLAlchemy, SQLite (PostgreSQL-ready), Pandas, scikit-learn only where justified, Pytest, Ruff, GitHub Actions, retrieval-grounded LLM integration and PDF reporting.

## Current status

**Phase 1 complete — research and requirements baseline.** Official SIH26241 requirements are mapped to the product, and the SRS, architecture, data model, risk register and acceptance baseline are documented. Phase 2 application implementation is next.

External dependencies are tracked in GitHub issues: the authorised SIH dummy outcome dataset, and confirmation of the pilot language/region and any live counsellor partner.

- [60-day roadmap](ROADMAP.md)
- [SRS](docs/SRS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [SIH traceability](docs/PROBLEM_STATEMENT_MAPPING.md)
- [Outcome data model](docs/OUTCOME_DATA_MODEL.md)
- [Data-source policy](docs/DATA_SOURCE_POLICY.md)

## Engineering principles

- Eligibility is a hard filter, not a weighted preference.
- Matching weights are configurable prototype assumptions, not validated psychometrics.
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
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

pip install -e ".[dev]"
```

Run the API and UI in separate terminals:

```bash
uvicorn backend.main:app --reload
streamlit run app/streamlit_app.py
```

Run checks:

```bash
ruff check .
pytest -q
```

The API health endpoint is available at http://127.0.0.1:8000/health. The Streamlit shell starts at http://localhost:8501.

## License

MIT. See LICENSE.
