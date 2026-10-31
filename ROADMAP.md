# PathSaathi AI — 60-Day Delivery Roadmap

**SIH Problem Statement:** 26241 — AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education  
**Owner:** Solo developer  
**Daily allocation:** Target up to 4 focused hours (240 planned hours over 60 days)  
**Priority:** Resume-first, portfolio-quality implementation  
**Stack:** Python, Streamlit, FastAPI, SQLAlchemy, SQLite/PostgreSQL-ready, Pandas, Pytest, Ruff, GitHub Actions

The full SIH brief is now recorded in `docs/PROBLEM_STATEMENT_26241.md`. The roadmap is rebalanced around the actual judging requirements: joint family counselling, localised verified outcomes, NSQF progression, bilingual/low-literacy access, human escalation and scheme-admin analytics.

| Phase | Days | Focus | Exit evidence | Status |
|---|---:|---|---|---|
| 1. Problem validation & requirements | 1–5 | Official brief, users, SRS, data contract, risks and success criteria | Approved requirements and acceptance checklist | In progress |
| 2. Platform foundation | 6–12 | Streamlit/FastAPI skeleton, auth, database, locale framework, CI | App/API starts, DB smoke test, CI green | Not started |
| 3. Outcome data backend | 13–21 | Import contract, validation, provider/trade/geography/cohort metrics | Tested outcome-data import and evidence-aware queries | Not started |
| 4. Joint bilingual counselling | 22–30 | Learner-parent conversation, English + Marathi, low-jargon flows | Shared bilingual family counselling journey | Not started |
| 5. Trade and NSQF explainers | 31–37 | Job-role mapping, qualification progression, contextual comparisons | Plain-language local pathway explanation | Not started |
| 6. Human escalation & admin analytics | 38–45 | Counsellor callback flow, engagement and resistance dashboard | Escalation workflow and privacy-safe dashboard | Not started |
| 7. Integration, evaluation & safeguards | 46–52 | End-to-end tests, data quality, usability, security and evidence review | Tested integrated flow and evaluation report | Not started |
| 8. Deployment & portfolio release | 53–60 | Hosting, documentation, demo, screenshots and resume story | Public demo, reproducible repo and final technical documentation | Not started |

## Daily execution protocol

Each daily run must inspect the repository, open issues, recent commits and CI; select the next incomplete task; implement one substantive vertical slice; run actual relevant checks; update the roadmap; and commit only validated work. A scheduler invocation does not prove four continuous hours elapsed.

## Core end-to-end experience

**learner + parent → bilingual guided conversation → local outcome evidence → trade/job-role/NSQF explanation → human escalation when needed → family summary → aggregate scheme-admin insights**

## Outcome data rules

- The SIH brief states that dummy placement/earnings datasets will be provided for hackathon evaluation. They have not been supplied in the current project files.
- Build an explicit import schema and validation tests now.
- Use clearly labelled synthetic fixtures for development only.
- Never substitute synthetic values for official evaluation evidence.
- Show the placement denominator, cohort size, location and reporting period.
- Show earnings period/currency/statistic and the number of observations.
- Do not claim causality or guarantee an individual's outcome.

## Privacy and human-centred safeguards

- Store household income as a broad optional bracket, not exact income.
- Use explicit consent for family linking and any sentiment/concern check-in.
- Measure concern shifts using transparent self-report before/after prompts, not covert sentiment inference.
- Show administrators aggregate trends only; suppress small cohorts and avoid household-level views.
- Offer human escalation; AI must admit when evidence is insufficient.

## Definition of done

- Learner and parent can participate in the same counselling journey.
- English and at least one regional language work for key user flows (MVP: English + Marathi).
- Verified trade/provider outcome records can be imported and queried by context.
- Earnings/placement evidence is presented with provenance, cohort, denominator and period.
- Plain-language trade, job-role and NSQF progression explainers work.
- A human counsellor request can be submitted and its status tracked.
- Admins can see privacy-safe aggregate engagement and family concern themes/shifts.
- The product has tests, CI, reproducible setup, deployment, demo and explicit limitations.

## Progress log

| Date | Phase | Increment | Evidence |
|---|---|---|---|
| 2026-11-01 | Phase 1 | Initial repository, SRS baseline and issue tracker | GitHub docs and issues exist |
| 2026-11-01 | Phase 1 | Official SIH PS 26241 details received and scope being revised | `docs/PROBLEM_STATEMENT_26241.md` |
