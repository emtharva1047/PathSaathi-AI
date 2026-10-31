# PathSaathi AI — 60-Day Roadmap

**Mode:** Solo developer  
**Time budget:** Up to 4 focused hours per day (approximately 240 planned hours)  
**Priority:** Resume-quality portfolio product  
**Stack:** Python, Streamlit, FastAPI, SQLAlchemy, SQLite/PostgreSQL-ready, Pandas, Pytest, Ruff, GitHub Actions

Day numbers are planning windows, not claims that four hours elapsed during an automation run. Update status only after repository evidence exists.

| Phase | Days | Objective | Exit evidence | Status |
|---|---:|---|---|---|
| 1. Research & requirements | 1–5 | Map official SIH26241 brief, users, SRS, data and risk | Traceability matrix, reviewed SRS, data model, acceptance baseline | Complete |
| 2. Application foundation | 6–12 | Build Streamlit/FastAPI skeleton, config, DB, locale and CI | App starts, API health, DB smoke test, CI green | Next |
| 3. Assessment & recommendations | 13–22 | Build assessment and explainable eligibility-safe matching | Deterministic recommendations with unit tests | Not started |
| 4. Course & outcome explorer | 23–29 | Import sourced qualifications and outcome evidence | Search/filter/detail/compare with provenance and metric semantics | Not started |
| 5. Family counselling & escalation | 30–36 | Shared bilingual session, separate preferences and counsellor request queue | Student-parent flow and trackable escalation request | Not started |
| 6. AI counsellor & reporting | 37–41 | Retrieval-grounded bilingual Q&A and PDF report | Source-backed responses, explicit unknowns and report export | Not started |
| 7. Admin analytics, quality & privacy | 42–47 | Aggregate engagement dashboard, testing and security review | Privacy-safe aggregate dashboard and test/security report | Not started |
| 8. Portfolio release | 48–60 | Deploy, document, demonstrate and polish | Live demo, CI, screenshots, demo script and resume summary | Not started |

## Scope decisions

- Initial pilot: Maharashtra; English + Marathi. This is a project assumption, not an SIH-mandated geography.
- Initial learner cohort: students considering vocational pathways after Class 10 or Class 12, with extension to current vocational/non-degree learners.
- Use NQR/NCVET qualification sources and authorised DGT/state tracer studies.
- SIH listing says dummy placement/earnings datasets will be provided for evaluation; until received, use clearly labelled synthetic fixtures.
- Do not infer provider-level outcomes from state/trade aggregates.
- Human escalation is a demonstrator request queue unless a real counsellor partner is connected.
- Sentiment change uses optional self-report, not covert emotion inference.

## Daily execution protocol

Each daily iteration should:
1. Inspect repository state, open issues, recent commits and Actions.
2. Select the highest-priority incomplete task.
3. Deliver one cohesive, substantive increment.
4. Run relevant checks and record exact results.
5. Update documentation and issue state based on evidence.
6. Commit only validated work.

A four-hour target is a planned allocation, not a claim that an automation run consumed four uninterrupted hours.

## Definition of done

The end-to-end journey works:

**profile → assessment → eligibility filter → ranked pathways → source-linked outcome/course comparison → shared family counselling → human escalation option → report**

Required evidence:
- Tests for eligibility, scoring, metric definitions, family permissions and analytics aggregation.
- Reproducible local setup and environment-based secrets.
- CI for lint and tests.
- No secrets or real learner/parent records committed.
- Source provenance and verification dates for qualification/outcome facts.
- Explicit limitations and data gaps.
- Deployed demonstration, screenshots and resume-ready documentation.

## Phase 1 completion evidence
- [x] Official SIH26241 listing reviewed and requirements summarised.
- [x] Problem-to-product traceability matrix added.
- [x] Initial learner cohort and Maharashtra/Marathi pilot assumption documented.
- [x] Learner, parent, counsellor, admin and data-curator journeys documented.
- [x] SRS, architecture, data-source policy, outcome data model and risk register updated.
- [x] Four Phase 1 issues closed with evidence.
- [x] External dependencies tracked in issues #5 and #6.
- [x] Documentation contract tests added; CI validation pending.

## Progress log

| Date | Phase / planned day | Increment | Checks | Commit |
|---|---|---|---|---|
| 2026-11-01 | Phase 1 / Days 1–5 | Official SIH brief research, traceability, requirements and data model | GitHub read-back verified; CI issue diagnosed and contract tests added; latest run pending | See commit history |
