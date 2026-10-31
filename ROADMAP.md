# PathSaathi AI — 100-Day Target / 120-Day Maximum Roadmap

**Mode:** Solo developer  
**Work cadence:** One development iteration every 36 hours (1.5 days)  
**Focus target:** 2–3 hours per iteration  
**Planned effort:** Approximately 160–240 focused hours across up to 80 iterations  
**Nominal delivery target:** 100 calendar days  
**Hard maximum:** 120 calendar days  
**Priority:** Resume-quality portfolio product  
**Stack:** Python, Streamlit, FastAPI, Pandas, Pytest, Ruff, GitHub Actions; persistent PostgreSQL and cloud deployment are deliberately scheduled after Phase 4.

The cadence and work duration are targets, not a claim that an automation run has occupied that amount of wall-clock time. Update status only after repository evidence exists.

## Delivery phases

| Phase | Project days | Objective | Exit evidence | Status |
|---|---:|---|---|---|
| 1. Research & SIH requirements | 1–7 | Map SIH26241, personas, requirements, outcome data and risks | Traceability matrix, reviewed SRS, data contract, acceptance baseline | Complete |
| 2. Application foundation | 8–18 | Build Python/Streamlit/FastAPI skeleton, configuration, API contracts, locale scaffold and CI; no hosted DB connection yet | App starts, API health, service/repository interfaces, CI green | In progress |
| 3. Assessment & recommendations | 19–38 | Build bilingual learner profile, assessment and explainable eligibility-aware matching using fixtures/adapters | Deterministic recommendations with tests and demo fixtures | Not started |
| 4. Outcome data & course explorer | 39–52 | Build CSV/data import validation, provenance-aware outcome and course catalogue, explorer and comparison | Verified data contract, denominator/earnings validation, source-linked explorer | Not started |
| 5. Persistent database & family workflows | 53–67 | After Phase 4, connect managed PostgreSQL, add migrations and persistence, then implement family accounts, consent, preferences and escalation | Deployed DB connection, migrations, tested persistence, joint family workflow | Not started |
| 6. AI counsellor & reporting | 68–78 | Grounded Q&A, trade/NSQF explainers, evidence references and PDF report | Source-backed responses, explicit unknowns and report export | Not started |
| 7. Admin analytics, quality & privacy | 79–90 | Aggregate engagement/resistance dashboard, self-reported concern shifts, small-cohort suppression, security and usability | Privacy-safe analytics and test/security report | Not started |
| 8. Cloud deployment & portfolio release | 91–100 | After Phase 4, deploy FastAPI API to Vercel, Streamlit UI to a Streamlit-compatible host, connect managed PostgreSQL, verify E2E and publish portfolio evidence | Live API/UI, production-like DB integration, CI, screenshots, demo and resume summary | Not started |
| Contingency | 101–120 | Resolve data/sponsor dependencies, migration/deployment problems, accessibility, user testing, performance/security and release stability | Critical gaps closed; no unjustified scope expansion | Reserved |

## Explicit database and hosting sequence

**Before Phase 4 completion**
- Define data contracts, domain models, repository/service interfaces and validation rules.
- Use synthetic fixtures, CSV imports and isolated test adapters for development.
- Do not provision or depend on a hosted production database.
- Do not deploy the application to production hosting.

**After Phase 4 completion**
1. Select a managed PostgreSQL provider and provision the database.
2. Connect SQLAlchemy using environment-based connection strings and secure secrets.
3. Add Alembic migrations, indexes, transaction handling, connection pooling and backup/restore notes.
4. Add integration tests against a disposable test database; never commit production credentials.
5. Deploy the FastAPI backend to Vercel's Python runtime.
6. Deploy Streamlit separately to Streamlit Community Cloud or another Streamlit-compatible host; do not assume Streamlit itself runs as a native Vercel app.
7. Configure CORS, API base URL, health checks, secrets, logs and deployment smoke tests.
8. Run end-to-end checks across UI → Vercel API → PostgreSQL.

Vercel hosting is for the FastAPI API layer. Streamlit hosting is separate unless the UI architecture is intentionally changed and documented.

## Iteration protocol

Every 36-hour iteration should:
1. Inspect repository head, roadmap, open issues, recent commits and CI.
2. Select the highest-priority incomplete task.
3. Deliver one cohesive, substantive increment.
4. Run relevant checks and record exact results.
5. Update documentation and issue state based on evidence.
6. Commit only validated work using a meaningful Conventional Commit.

## Definition of done

The end-to-end journey works:

**profile → assessment → eligibility-aware pathways → source-linked outcome/course comparison → persistent family session → joint counselling → human escalation option → optional concern check-in → privacy-safe admin dashboard → report**

Required evidence:
- English and Marathi support for key flows with reviewed translations.
- Placement rates with cohort definitions/denominators and reporting periods.
- Earnings with currency, time basis, statistic type and follow-up period.
- Source provenance and verification dates; unknown values remain unknown.
- Tested PostgreSQL persistence and migrations after Phase 4.
- Vercel FastAPI deployment and separate Streamlit deployment after Phase 4.
- Tests for outcome calculations, eligibility, family permissions and privacy-safe aggregation.
- Human escalation honestly represented as a request/callback queue unless a real counsellor system is integrated.
- Self-reported concern measurement only; no covert emotion inference.
- Reproducible setup, CI, deployment, screenshots and known limitations.
- No secrets or real learner/parent records committed.

## External dependencies

- SIH dummy placement/earnings dataset is not yet available. Use synthetic fixtures only for tests until the authorised dataset is supplied.
- Maharashtra/Marathi is a pilot assumption requiring confirmation.
- Real-time human counsellor integration requires a partner or authorised endpoint.
- PostgreSQL and hosting provider selection will be made when the post-Phase-4 integration work begins.

## Phase 1 completion evidence

- [x] Official SIH26241 requirements recorded.
- [x] Joint learner-parent, bilingual, outcome-data, progression, escalation, admin analytics and low-literacy requirements mapped.
- [x] SRS, architecture, data contract, provenance policy and risks documented.
- [x] External dependencies tracked in GitHub issues.

## Phase 2 progress

- [x] Python project metadata, runtime/dev dependencies and Python version added.
- [x] Streamlit shell with English/Marathi navigation labels added.
- [x] FastAPI app and /health endpoint added.
- [x] Shared logging configuration and generic API error response added.
- [x] Package scaffolds created for app, backend, core, database and services.
- [x] CI installs project and dev dependencies, compiles packages, runs Ruff and Pytest.
- [x] Previous GitHub Actions run 41232769034 passed: compileall, Ruff and Pytest (9 passed).
- [ ] SQLAlchemy/domain repository interfaces using fixture/in-memory adapters only before Phase 4.
- [ ] Complete UI/API contract and accessibility shell.

## Progress log

| Date | Increment | Checks / evidence |
|---|---|---|
| 2026-11-01 | Phase 1 requirements and SIH traceability baseline completed | Requirements docs reviewed |
| 2026-11-01 | Phase 2 Python scaffold, FastAPI health route, Streamlit bilingual shell, logging and CI | Previous Actions run 41232769034: compileall passed, Ruff passed, Pytest 9 passed |
| 2026-11-01 | Database connection and Vercel/production deployment deliberately deferred until after Phase 4 | Roadmap and automation instructions updated |
