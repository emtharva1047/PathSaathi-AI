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

**Phase 1 — Research and requirements.** The official SIH26241 listing has been reviewed and mapped to product requirements. The complete SRS, scope and data assumptions are being refined before application implementation.

- [60-day roadmap](ROADMAP.md)
- [SRS](docs/SRS.md)
- [Architecture](docs/ARCHITECTURE.md)
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

Implementation commands will be added with the Phase 2 application skeleton.

## License

MIT. See LICENSE.
