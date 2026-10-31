# PathSaathi AI — 60-Day Roadmap

**Mode:** Solo developer  
**Daily target:** Up to 4 focused hours  
**Total planned effort:** Approximately 240 focused hours over 60 calendar days  
**Priority:** Resume-quality portfolio product  
**Stack:** Python, Streamlit, FastAPI, SQLAlchemy, SQLite/PostgreSQL-ready, Pandas, Pytest, Ruff, GitHub Actions

The 60-day deadline is fixed by the project owner. Do not extend the project to 100/120 days unless the owner explicitly changes it. Day numbers are planning windows; work may advance when exit criteria are met. An automation run does not prove four hours of continuous work.

## Delivery phases

| Phase | Days | Objective | Exit evidence | Status |
|---|---:|---|---|---|
| 1. Research & SIH requirements | 1–5 | Map SIH26241, users, SRS, data and risks | Traceability matrix, reviewed SRS, data contract and acceptance baseline | Complete |
| 2. Application foundation | 6–12 | Build Streamlit/FastAPI skeleton, config, DB, locale and CI | App starts, API health, DB smoke test and CI green | In progress |
| 3. Joint profile & pathway exploration | 13–22 | Bilingual learner/parent context, guided assessment and advisory pathway shortlisting | Tested, transparent pathway exploration with eligibility states | Not started |
| 4. Outcome data & course explorer | 23–29 | Import/validate outcome evidence, sourced catalogue and comparison | Metrics with denominators, cohort, period and provenance | Not started |
| 5. Family counselling & escalation | 30–36 | Shared bilingual counselling, separate participant views and human follow-up workflow | Joint counselling journey and trackable escalation | Not started |
| 6. AI counsellor & reporting | 37–41 | Grounded Q&A, trade/NSQF explainers and PDF report | Source-backed answers, explicit unknowns and report export | Not started |
| 7. Admin analytics, quality & privacy | 42–47 | Aggregate engagement dashboard, tests, access control and usability review | Privacy-safe dashboard and test/security report | Not started |
| 8. Portfolio release | 48–60 | Deploy, validate end-to-end, document and demonstrate | Live demo, CI, screenshots, demo script and resume summary | Not started |

## Fixed scope decisions

- Initial pilot assumption: Maharashtra, English + Marathi; confirm with mentor/sponsor if required.
- Initial learner cohort: students considering vocational options after Class 10 or Class 12, extensible to other learners.
- The central product is joint learner-parent counselling grounded in local evidence, not a generic chatbot.
- Use SIH dummy placement/earnings data when supplied. Until then, use clearly labelled synthetic fixtures only.
- Never infer provider-level outcomes from state/trade aggregates.
- Human escalation is a truthful callback/request queue unless a real counsellor service is connected.
- Sentiment shifts use optional self-report, not covert emotion inference.
- No custom LLM training, native mobile app or nationwide live scraping in the 60-day MVP.

## Daily execution protocol

Each daily iteration should:
1. Inspect repository head, roadmap, open issues, recent commits and CI.
2. Select the highest-priority incomplete issue.
3. Deliver one cohesive, substantive increment.
4. Run relevant checks and record exact results.
5. Update documentation and issue state based on evidence.
6. Commit only validated work using a meaningful Conventional Commit.

## Definition of done

The end-to-end journey works:

**profile → joint counselling → advisory pathway shortlist → source-linked outcome/course comparison → trade/job-role/NSQF explainer → human escalation option → optional concern check-in → privacy-safe admin dashboard → report**

Required evidence:
- English and Marathi support for key flows with reviewed translations.
- Placement rates with cohort definitions/denominators and reporting periods.
- Earnings with currency, time basis, statistic type and follow-up period.
- Source provenance and verification dates; unknown values remain unknown.
- Tests for outcome calculations, eligibility, family permissions and privacy-safe aggregation.
- Human escalation honestly represented as a request/callback queue unless a real counsellor system is integrated.
- Self-reported concern measurement only; no covert emotion inference.
- Reproducible setup, CI, deployment, screenshots and known limitations.
- No secrets or real learner/parent records committed.

## Phase 1 completion evidence

- [x] Official SIH26241 requirements recorded.
- [x] Joint learner-parent, bilingual, outcome-data, progression, escalation, admin analytics and low-literacy requirements mapped.
- [x] SRS, architecture, data contract, provenance policy and risks documented.
- [x] External dependencies tracked in issues #5 and #6.
- [x] Phase 1 issues #1–#4 closed.

## Phase 2 progress

- [x] Python project metadata, runtime/dev dependencies and Python version added.
- [x] Streamlit shell with English/Marathi navigation labels added.
- [x] FastAPI app and /health endpoint added.
- [x] Shared logging configuration and generic API error response added.
- [x] Package scaffolds created for app, backend, core, database and services.
- [x] CI installs the project and dev dependencies, compiles packages, runs Ruff and Pytest.
- [x] GitHub Actions run 41232769034 passed: compileall, Ruff and Pytest (9 passed, no test warnings).
- [ ] SQLAlchemy engine/session and initial models.
- [ ] UI API-status integration and accessibility review.

## Progress log

| Date | Phase / planned days | Increment | Checks / evidence |
|---|---|---|---|
| 2026-11-01 | Phase 1 / Days 1–5 | Official SIH research, SRS, traceability, outcome contract, localization, escalation and admin analytics baseline | Ruff passed; Pytest 8 passed in Actions run 41232400382 |
| 2026-11-01 | Phase 2 / Days 6–12 (started early after Phase 1 exit) | Python scaffold, FastAPI health route, Streamlit bilingual shell, logging, safe error handling and CI dependency setup | Actions run 41232769034: compileall passed, Ruff passed, Pytest 9 passed |
