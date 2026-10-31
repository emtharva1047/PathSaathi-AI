# PathSaathi AI

**AI-enabled career counselling and family decision-support for vocational education**  
**SIH Problem Statement ID: 26241 | Ministry of Skill Development and Entrepreneurship | Smart Education**

PathSaathi AI is a bilingual, family-inclusive vocational counselling platform. It helps learners and parents discuss vocational pathways using local, trade- and provider-specific outcome evidence, clear qualification progression explanations, and human counsellor escalation when needed.

> This is a decision-support and counselling aid. It does not guarantee admission, placement, salary, job security, or a particular career outcome.

## The problem we are addressing

The SIH brief highlights that family perception can influence vocational enrolment, retention and progression. A learner-facing course recommender alone does not resolve parental concerns about earnings, safety, job security and social standing. PathSaathi AI therefore treats the learner and family as participants in one guided counselling process.

## Core product capabilities

1. **Joint learner-parent counselling:** A shared conversational experience that captures learner goals and parent concerns without erasing either perspective.
2. **Bilingual, low-jargon interface:** English plus Marathi in the first demonstrator, with a locale-ready design, guided steps and accessible explanations.
3. **Verified outcome-data backend:** Trade- and provider-specific placement and post-training earnings data, with cohort size, time period, location, source and verification metadata.
4. **Localised career explainers:** Plain-language explanations of job roles, earning evidence, working conditions, qualification requirements and progression routes.
5. **NSQF progression map:** Explain how a vocational qualification can connect to higher NSQF levels, further training and education routes.
6. **Human counsellor escalation:** A clear way to request a callback or live counsellor and track the request status.
7. **Scheme administrator dashboard:** Aggregated engagement, parental concern themes and explicit pre/post self-reported concern shifts, with privacy safeguards.

## Planned technology

Python 3.12+, Streamlit, FastAPI, SQLAlchemy, SQLite locally with PostgreSQL-ready configuration, Pandas, scikit-learn only where justified, Pytest, Ruff, GitHub Actions, retrieval-grounded LLM integration and PDF reporting.

## Outcome data integrity

The SIH entry says dummy placement/earnings datasets will be provided for hackathon evaluation. That dataset has not yet been added to this repository. We will build and test the import contract first, use clearly labelled synthetic fixtures only for development, and replace them with the supplied evaluation data when available. No earnings, placement or provider statistics will be invented.

## User journey

1. Learner selects language and completes a short, guided context/interest flow.
2. Parent joins the same counselling session or receives a consent-aware invitation.
3. The family raises questions about income, safety, job security, social perception and progression.
4. The counsellor retrieves relevant local trade/provider outcome records and explains their sample size, period and limitations.
5. The family reviews job-role and NSQF progression explainers.
6. If questions remain unresolved, the user requests a human counsellor.
7. The interaction produces a summary and next steps; administrators see only appropriately aggregated analytics.

## Repository status

**Current phase: Phase 1 — official brief received; requirements and architecture being revised.** See [ROADMAP.md](ROADMAP.md), [docs/PROBLEM_STATEMENT_26241.md](docs/PROBLEM_STATEMENT_26241.md), and [docs/SRS.md](docs/SRS.md).

## Engineering principles

- Outcome claims must be specific to trade, provider, location, cohort and reporting period whenever available.
- Show sample sizes and denominators; do not imply that past outcomes guarantee an individual's future.
- Never treat unknown eligibility or missing outcome data as positive evidence.
- Preserve learner agency while making parent concerns visible.
- Track sentiment through explicit, consented self-report measures; do not secretly infer a family's psychological state.
- Aggregate administrator analytics and suppress small cohorts that could identify households.
- Use synthetic profiles only; never commit personal learner/family data or secrets.
- AI responses must be grounded in verified records and must disclose uncertainty.

## Local setup

Implementation setup will be completed in Phase 2. The intended developer setup is:

```bash
python -m venv .venv
pip install -r requirements.txt
```

## Planned structure

```text
app/                  Streamlit pages and components
backend/              FastAPI routes, schemas and services
core/                 Configuration, locale and shared utilities
database/             SQLAlchemy models and repositories
data/                 Licensed/official reference and outcome data
docs/                 SRS, data contract, architecture and research
tests/                Unit and integration tests
.github/workflows/    CI
```

## Licence

MIT. See [LICENSE](LICENSE).
