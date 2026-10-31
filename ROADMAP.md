# PathSaathi AI — 100-Day Target / 120-Day Maximum Roadmap

**Mode:** Solo developer  
**Work cadence:** One development iteration every 36 hours (1.5 days)  
**Focus target:** 2–3 hours per iteration  
**Planned effort:** Approximately 160–240 focused hours across up to 80 iterations  
**Nominal delivery target:** 100 calendar days  
**Hard maximum:** 120 calendar days, including contingency  
**Priority:** Resume-quality portfolio product  
**Stack:** Python, Streamlit, FastAPI, SQLAlchemy, SQLite/PostgreSQL-ready, Pandas, Pytest, Ruff, GitHub Actions

The cadence and work duration are targets, not a claim that an automation run has occupied that amount of wall-clock time. Update status only after evidence exists in the repository.

## Delivery phases

| Phase | Project days | Objective | Exit evidence | Status |
|---|---:|---|---|---|
| 1. Research & SIH requirements | 1–7 | Map SIH26241, personas, requirements, data and risks | Traceability matrix, reviewed SRS, data contract, acceptance baseline | Complete |
| 2. Application foundation | 8–18 | Build Streamlit/FastAPI skeleton, config, DB, locale and CI | App starts, API health, DB smoke test, CI green | Next |
| 3. Joint profile & recommendations | 19–38 | Bilingual learner/parent context, assessment, eligibility-aware matching | Deterministic recommendations with unit tests | Not started |
| 4. Outcome data & course explorer | 39–52 | Import/validate outcome evidence, sourced catalogue, explorer and comparison | Outcome data contract, metrics with denominators and provenance | Not started |
| 5. Family counselling & escalation | 53–67 | Shared bilingual counselling, distinct family views, human follow-up workflow | Joint counselling journey and trackable escalation | Not started |
| 6. AI counsellor & reporting | 68–78 | Grounded Q&A, trade/NSQF explainers and PDF report | Source-backed answers, explicit unknowns and report export | Not started |
| 7. Admin analytics, quality & privacy | 79–90 | Aggregate engagement/resistance dashboard, concern shifts, security and usability | Privacy-safe dashboard and test/security report | Not started |
| 8. Portfolio release | 91–100 | Deploy, validate end-to-end, document and demonstrate | Live demo, CI, screenshots, demo script and resume summary | Not started |
| Contingency | 101–120 | Resolve data/sponsor dependencies, improve accessibility, testing, stability and polish | Remaining critical gaps closed; no unnecessary feature expansion | Reserved |

## Iteration protocol

Every 36-hour iteration should:
1. Inspect repository head, roadmap, open issues, recent commits and CI.
2. Select the highest-priority incomplete task.
3. Deliver one cohesive, substantive increment.
4. Run relevant checks and record exact results.
5. Update documentation and issue state based on evidence.
6. Publish a Conventional Commit only after validation.

## Definition of done

The end-to-end journey works:

**profile → joint counselling → eligibility-aware recommendations → source-linked outcome/course comparison → trade/job-role/NSQF explainer → human escalation option → concern check-in → privacy-safe admin dashboard → report**

Required evidence:
- English and Marathi support for key flows, with reviewed translations.
- Placement rates with cohort definitions/denominators and reporting periods.
- Earnings with currency, time basis, statistic type and follow-up period.
- Source provenance and verification dates; unknown values remain unknown.
- Tests for outcome calculations, eligibility, family permissions and privacy-safe aggregation.
- Human escalation honestly represented as a request/callback queue unless a real counsellor system is integrated.
- Self-reported concern measurement only; no covert emotion inference.
- Reproducible setup, CI, deployment, screenshots and known limitations.
- No secrets or real learner/parent records committed.

## External dependencies

- SIH dummy placement/earnings dataset is not yet available in the repository. Use synthetic fixtures only for tests until the authorised dataset is supplied.
- Maharashtra/Marathi is a pilot assumption requiring confirmation.
- Real-time human counsellor integration requires an actual counsellor partner or authorised endpoint.

## Phase 1 completion evidence

- [x] Official SIH26241 requirements recorded.
- [x] Joint learner-parent, bilingual, outcome-data, progression, escalation, admin analytics and low-literacy requirements mapped.
- [x] SRS, architecture, data contract, provenance policy and risks documented.
- [x] External dependencies tracked in GitHub issues.

## Progress log

| Date | Increment | Checks / evidence |
|---|---|---|
| 2026-11-01 | Phase 1 requirements and SIH traceability baseline completed | Requirements and repository docs reviewed |
| 2026-11-01 | Schedule extended to 100-day target / 120-day maximum, with 36-hour iteration cadence | Automation configuration updated |
