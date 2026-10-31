# PathSaathi AI

**AI-enabled career counselling and family decision-support for vocational education.**

PathSaathi AI helps students explore vocational pathways using structured assessments, transparent eligibility-aware recommendations, verified course information, and collaborative family decision tools.

> This is an educational decision-support tool, not a psychometric diagnosis or a guarantee of admission, employment, salary, or career outcomes.

## Portfolio goals

- Demonstrate Python application engineering with Streamlit and FastAPI.
- Build an explainable recommendation engine with eligibility as a hard constraint.
- Curate vocational course/career information with provenance and verification dates.
- Support student and parent decision-making without allowing either party to override the student's agency.
- Provide tests, reproducible setup, CI, deployment documentation, and a transparent limitations section.

## Planned stack

Python 3.12+, Streamlit, FastAPI, SQLAlchemy, SQLite (PostgreSQL-ready configuration), Pandas, scikit-learn where justified, Pytest, Ruff, GitHub Actions, retrieval-grounded LLM integration, and PDF reporting.

## Status

**Current phase: Phase 1 — Research and requirements.** See [ROADMAP.md](ROADMAP.md) and [docs/SRS.md](docs/SRS.md).

## Planned user journey

1. Student creates a profile and completes an interest/skills/preferences assessment.
2. The platform validates course eligibility separately from preference matching.
3. A transparent scoring engine ranks suitable pathways and explains its reasoning.
4. Student explores source-linked vocational courses and progression options.
5. Student and parent independently record priorities and compare options in a family decision room.
6. The platform produces a report with recommendations, evidence, uncertainties, and practical next steps.

## Local setup

Implementation instructions will be added in Phase 2. The intended developer setup is:

```bash
python -m venv .venv
pip install -r requirements.txt
```

## Repository structure (target)

```text
app/                 Streamlit interface
backend/             FastAPI routes, schemas, services
core/                Configuration and shared utilities
database/            SQLAlchemy models and session management
data/                Licensed/official seed data and provenance
docs/                SRS, architecture, research and decisions
tests/               Unit and integration tests
.github/workflows/   Continuous integration
```

## Engineering principles

- Eligibility is a hard filter, not a small term in a weighted score.
- Recommendation weights are configurable prototype assumptions until validated by qualified counsellors.
- Use synthetic profiles for development and demos; never commit real student records.
- Store source URLs and last-verified dates for factual course claims.
- Keep AI responses grounded in curated sources and clearly mark missing or uncertain information.
- Minimise personal data and document age-aware consent requirements before any real deployment.
- Do not fabricate fees, placement rates, salaries, or outcome statistics.

## Contributing

This is currently a solo portfolio project. Work is tracked through GitHub Issues and ROADMAP.md. Use focused changes, tests, and Conventional Commit messages.

## Licence

MIT. See LICENSE.
