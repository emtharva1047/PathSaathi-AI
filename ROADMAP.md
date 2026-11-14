# PathSaathi AI — 60-Calendar-Day Delivery Roadmap

**Owner-approved window:** 2 November–31 December 2026 (exactly 60 calendar days)  
**Mode:** Solo developer; resume-first engineering portfolio  
**Cadence:** One scheduled development run per day  
**Work allocation:** Up to four focused hours per day; this is a planning target, not a claim of elapsed runtime  
**Hard deadline:** 31 December 2026. Do not extend the plan without explicit owner approval.  
**Stack:** Python 3.12+, Streamlit, FastAPI, SQLAlchemy 2.x, SQLite locally, PostgreSQL-ready URL configuration, Pandas where justified, Pytest, Ruff, GitHub Actions, retrieval-grounded LLM API and PDF reporting.

## Calendar and phase plan

Day 1 is 2 November 2026. Day 60 is 31 December 2026.

| Phase | Project days | Calendar dates | Scope | Exit evidence | Status |
|---|---:|---|---|---|---|
| 1. Research and requirements | 1–5 | 2–6 Nov | Official SIH26241 review, personas/use cases, SRS, architecture, risks, outcome contract, traceability and acceptance | Requirements mapped, source policy and acceptance baseline | Complete |
| 2. Foundation | 6–12 | 7–13 Nov | Streamlit/FastAPI skeleton, config/logging, SQLAlchemy models, local SQLite, PostgreSQL-ready URL, API health, locale scaffold, read-only catalogue/evidence API, validation and CI | App/API start, explicit schema creation, request-scoped SQLite repositories, safe evidence responses and CI green | Complete (13 Nov) |
| 3. Counselling/profile/pathway | 13–22 | 14–23 Nov | Learner and parent context, guided bilingual prompts, advisory shortlisting, eligibility and source-backed explainers | Deterministic recommendations, eligible/ineligible/unknown outcomes, explainable tests | In progress (14 Nov) |
| 4. Course/outcome explorer | 23–29 | 24–30 Nov | SIH dummy-data importer when supplied, validation, source-linked qualifications/outcomes, filters and comparisons | Provenance-aware import report and accurate comparison semantics | Not started |
| 5. Family counselling/escalation | 30–36 | 1–7 Dec | Shared sessions, distinct learner/parent roles and preferences, consent and callback request workflow | Role separation, consent tests, honest escalation queue | Not started |
| 6. AI and reporting | 37–41 | 8–12 Dec | Retrieval-grounded bilingual Q&A, safe prompts, source display and PDF report | Evidence-backed responses with source/caveat display; report export | Not started |
| 7. Admin analytics, quality and privacy | 42–47 | 13–18 Dec | Aggregate dashboard, optional self-reported concern shifts, small-cohort suppression, security, data-quality and usability review | Privacy-safe analytics, QA and usability evidence | Not started |
| 8. Portfolio release | 48–60 | 19–31 Dec | Production database configuration, deployment, CI, docs, screenshots, diagrams, demo script, resume summary, limitations and end-to-end validation | Deployed API/UI, verified persistence, E2E smoke tests and portfolio evidence | Not started |

## Database and deployment sequence

**Phase 2 (local development):**
- SQLAlchemy 2.x models and repository adapters are part of the foundation.
- SQLite is the default local database (sqlite:///./data/pathsaathi.db).
- Schema creation is explicit; importing modules must not create files or open database connections.
- PATHSAATHI_DATABASE_URL accepts a PostgreSQL-compatible SQLAlchemy URL. The optional postgres dependency extra installs Psycopg 3.
- Unit and integration tests use isolated in-memory SQLite databases.
- Do not provision a managed production database or deploy the application during this phase.

**Phase 8 (production release):**
- Select and provision managed PostgreSQL only when release prerequisites are ready.
- Add/verify migrations, indexes, pooling, secret management, backup/restore notes and production integration tests.
- Deploy FastAPI and Streamlit separately to compatible hosts; do not assume Streamlit is a native Vercel app.
- Configure HTTPS, CORS, health checks, environment variables, logs and smoke tests.
- Verify the full UI → API → PostgreSQL journey.
- Never commit production credentials or real learner/family records.

## Product flow

Learner/parent onboarding and consent → joint bilingual counselling → contextual profile → verified outcome evidence → trade/job-role/NSQF explainer → human callback/escalation request → optional self-reported pre/post concern check-in → privacy-safe admin dashboard → shareable report.

## Responsible data and AI rules

- The SIH dummy dataset has not yet been received. Track it in [issue #5](https://github.com/emtharva1047/PathSaathi-AI/issues/5). Use synthetic fixtures only for tests and clearly labelled demonstrations.
- Use NCVET/NQR qualification records and exact qualification files for entry criteria/progression. Any DGT tracer study must retain exact state/cohort/sample/period caveats.
- Do not conflate placement, employment, trade-related employment, apprenticeship or self-employment.
- Never derive provider-level outcomes from state/trade aggregates.
- Earnings must retain currency, time basis, statistic type, follow-up period and observation count where available.
- Missing values remain unknown; LLM output cannot fill data gaps.
- AI answers retrieve approved evidence and disclose source date, cohort and geography. Deterministic evidence display must work without the LLM provider.
- Keep Maharashtra/Marathi as configurable pilot assumptions pending mentor confirmation ([issue #6](https://github.com/emtharva1047/PathSaathi-AI)).
- Keep learner and parent preferences distinct; preserve learner agency.
- Human escalation is a callback/request queue until a real partner/endpoint exists.
- Admin analytics are aggregate only, suppress small cohorts and never expose identities or raw transcripts.
- Sentiment/concern shifts are optional self-report, never covert emotion inference.
- Collect only broad optional income/location bands. Production use with minors requires appropriate consent, retention and legal/privacy review.
- Never guarantee admission, salary, placement or job security; do not claim validated psychometrics.

## Phase 1 completion evidence

- [x] Official SIH26241 requirements recorded.
- [x] Joint learner-parent, bilingual, outcome-data, progression, escalation, admin analytics and low-literacy requirements mapped.
- [x] SRS, architecture, data contract, provenance policy and risks documented.
- [x] External dependencies #5 and #6 tracked.

## Phase 2 progress

- [x] Python project metadata, Streamlit shell, FastAPI health route, shared logging and CI scaffold.
- [x] English/Marathi navigation and resilient API-status indicator.
- [x] Typed course/outcome domain records, repository protocols and in-memory adapters.
- [x] Local SQLAlchemy 2.x models for courses and outcome evidence.
- [x] SQLite engine/session helpers with explicit schema creation and isolated in-memory test support.
- [x] SQLAlchemy repositories implement exact-match course/outcome queries without broadening provider scope.
- [x] PostgreSQL-ready URL configuration and optional Psycopg 3 dependency.
- [x] Local database tests cover round trips, unknown values, exact filters, duplicate IDs and database constraints.
- [x] FastAPI lazily creates a reusable SQLAlchemy session factory on first database-backed request and disposes its engine at shutdown; schema creation remains explicit.
- [x] Read-only course and outcome list/detail endpoints expose provenance and exact filters; unverified outcome values and numeric numerator/denominator/sample-size metadata are withheld, while unknowns remain null.
- [x] Provider-specific API filters return only provider-geography evidence; the health route remains database-independent.
- [x] Fresh GitHub Actions validation for the repository/domain/database increment (run #99: compileall, Ruff and 42 tests passed).
- [x] Fresh GitHub Actions validation for the read-only API increment (run #103: compileall, Ruff and 50 tests passed; one Starlette/httpx deprecation warning).
- [x] Reopened and completed Phase 2 local SQLite issue #9; production PostgreSQL/deployment remain in Phase 8 issue #11.
- [x] Add locale-managed step progress, explicit Back/Continue controls and contextual Help to the Streamlit shell; rendering-contract tests cover English and Marathi states.
- [x] GitHub Actions validation for accessibility shell and rendering-contract tests (runs #112 and #113: compileall passed, Ruff passed, Pytest 52 passed each; one Starlette/httpx deprecation warning per run).
- [x] Add bounded `limit`/`offset` pagination to course and outcome list APIs (default 50, maximum 100), applying bounds in SQL and matching stable identifier ordering in in-memory adapters.
- [x] GitHub Actions validation for catalogue pagination (run #117: compileall passed, Ruff passed, Pytest 61 passed; one existing Starlette/httpx deprecation warning).
- [x] Add an end-to-end FastAPI/SQLite lifecycle smoke test using the real lazy database dependency; verify database-independent health, lazy engine/session-factory creation, engine reuse across requests and shutdown cleanup.
- [x] GitHub Actions validation for the lifecycle smoke test (run #120: compileall passed, Ruff passed, Pytest 62 passed; one existing Starlette/httpx deprecation warning).
- [x] Add a network-level local-stack smoke check that starts real Uvicorn and verifies the Streamlit health client through offline → online → offline states; GitHub Actions run #123 passed compileall, Ruff, 62 tests and the live-process smoke check (one existing Starlette/httpx deprecation warning).
- [x] Add offline-state Streamlit render-contract coverage for Home, Learner profile and Explore pathways in English and Marathi; assert the localised warning/fallback copy, page content, progress, Help and available navigation controls remain rendered when the API is unavailable.
- [x] GitHub Actions validation for offline-state UI coverage (PR #24 run #127: compileall passed, Ruff passed, 68 tests passed and the live FastAPI/Streamlit health-client smoke check passed; one existing Starlette/httpx deprecation warning).
- [x] Read `PATHSAATHI_API_URL` as the Streamlit health-client default, preserve explicit-argument precedence, validate absolute HTTP(S) URLs and fail closed without a request for blank/malformed, credential-bearing, query-bearing or fragment-bearing values.
- [x] Document the API URL override and add regression tests for environment override, explicit override and seven invalid URL configurations.
- [x] Extend the network smoke check to start the real Streamlit process, verify its health and HTML endpoints while FastAPI is offline, and confirm Streamlit remains healthy through the API offline → online → offline lifecycle.
- [x] Validate runtime configuration at startup: required text settings, API port range, explicit boolean tokens and supported SQLite/PostgreSQL SQLAlchemy URLs; reject invalid values before serving requests without opening a database connection.
- [x] GitHub Actions validation for runtime settings (PR #27 run #136: compileall passed, Ruff passed, Pytest 113 passed and the real Streamlit/FastAPI process smoke check passed; one existing Starlette/httpx deprecation warning).
- [x] GitHub Actions validation for API URL configuration (PR #25 run #130: compileall passed, Ruff passed, 77 tests passed and the live FastAPI/Streamlit health-client smoke check passed; one existing Starlette/httpx deprecation warning).
- [ ] Cross-phase usability/accessibility follow-up: validate understandability, contrast, focus order, screen-reader output, mobile behaviour, read-aloud need and translations with target users/human Marathi reviewer ([issue #14](https://github.com/emtharva1047/PathSaathi-AI)); this remains required before public accessibility/usability claims but does not block the Phase 2 foundation exit gate.

- [x] Add a direct regression test proving each database dependency invocation receives a distinct SQLAlchemy session and closes it at request completion (PR #28, Actions run #139).
- [x] Complete the Phase 2 foundation acceptance review; see [PHASE2_ACCEPTANCE.md](docs/PHASE2_ACCEPTANCE.md). Human/device accessibility validation remains an explicit cross-phase follow-up in issue #14.

## Phase 3 progress

- [x] Add immutable learner and parent context records with distinct preferences, participant references and preferred languages.
- [x] Restrict location to normalized broad-region codes and household income to a configured band identifier; no exact address or amount fields are present.
- [x] Add deterministic `eligible` / `ineligible` / `unknown` education-criterion evaluation. Missing, unverified or stale qualification criteria and unknown learner education remain unknown.
- [x] Require qualification code, accepted education levels, publisher, HTTP(S) source URL and verification date before criteria can produce an eligible/ineligible result.
- [x] Add 16 focused local tests for profile separation, data minimization, source provenance and all eligibility states. GitHub Actions validation is pending in PR #29.
- [ ] Add guided bilingual profile capture and advisory pathway shortlisting; do not present shortlisting as a validated aptitude test.

## Progress log

| Date | Increment | Evidence |
|---|---|---|
| 2026-11-02 | Project window began; Phase 1 documentation baseline carried forward and verified | Existing SRS, architecture, mapping, data contract and risk documents |
| 2026-11-02 | Bilingual Streamlit shell and API health fallback | GitHub Actions run 41380633847: compileall, Ruff and 13 tests passed |
| 2026-11-02 | Typed domain records and in-memory repository contracts | 19 focused repository tests reported passing locally; CI for this increment pending |
| 2026-11-03 | Added SQLAlchemy course/outcome models, SQLite session helpers, PostgreSQL-ready URL configuration and SQLAlchemy repositories; provider queries now require provider-level geography | GitHub Actions run #99: compileall passed, Ruff passed, Pytest 42 passed; PR #15 merged as 3efda43 |
| 2026-11-03 | Reconciled project documentation and issue plan to the owner's exact 60-day window | README/ROADMAP/architecture updated; issue #9 reopened then completed; issue #11 moved to Phase 8; issue #13 completed |
| 2026-11-04 | Added lazy request-scoped FastAPI database sessions and read-only course/outcome list/detail endpoints with provenance-aware value withholding and provider-scope filtering | PR #17 merged as e900263; GitHub Actions run #103: compileall passed, Ruff passed, 50 tests passed (one Starlette/httpx deprecation warning); issue #16 completed |
| 2026-11-04 | Tightened the API response contract so unverified numerator, denominator and sample-size metadata are withheld alongside unverified values | PR #19 merged as e31ff27; GitHub Actions run #108: compileall passed, Ruff passed, 50 tests passed (one Starlette/httpx deprecation warning); issue #18 completed |
| 2026-11-05 | Added three-step progress, explicit Back/Continue controls and contextual Help in English/Marathi; added rendering-contract tests and documented what static review cannot validate | PR #20 merged as aab687e; GitHub Actions runs #112 and #113 passed compileall, Ruff and 52 tests each (one Starlette/httpx deprecation warning per run); target-user and assistive-technology validation remain open in issue #14 |
| 2026-11-06 | Added bounded, stable offset pagination to course/outcome APIs and both repository adapters, with API-bound validation and integration tests | PR #21; GitHub Actions run #117 passed compileall, Ruff and 61 tests (one Starlette/httpx deprecation warning) |
| 2026-11-07 | Added a FastAPI/SQLite lifecycle smoke test against the real lazy database dependency, including database-independent health, engine reuse and shutdown cleanup | PR #22; GitHub Actions run #120 passed compileall, Ruff and 62 tests (one Starlette/httpx deprecation warning) |
| 2026-11-08 | Added a network-level smoke script that launches Uvicorn on an ephemeral loopback port and exercises the same health client used by Streamlit; added the smoke check to CI and documented manual startup/offline-fallback verification | GitHub Actions run #123 passed compileall, Ruff, 62 tests and the live-process smoke check (one existing Starlette/httpx deprecation warning) |
| 2026-11-09 | Added six offline UI render-contract cases covering all three informational pages in English and Marathi; the tests assert translated offline status/fallback copy and preserve page content, progress, Help and navigation controls | GitHub Actions run #127 on PR #24: compileall passed, Ruff passed, Pytest 68 passed and live-process smoke check passed (one existing Starlette/httpx deprecation warning) |
| 2026-11-10 | Hardened the Streamlit API health client to honour PATHSAATHI_API_URL, validate HTTP(S) base URLs and fail closed on unsafe/malformed configuration; added environment/explicit override and invalid-URL regression cases | PR #25 run #130: compileall passed, Ruff passed, Pytest 77 passed and live-process smoke check passed (one existing Starlette/httpx deprecation warning) |
| 2026-11-11 | Extended the live-process smoke check to start the actual Streamlit server, verify its health and HTML endpoints while the API is offline, and keep it healthy after FastAPI shutdown | PR #26 run #133: compileall passed, Ruff passed, Pytest 77 passed and real Streamlit/FastAPI process lifecycle smoke check passed (one existing Starlette/httpx deprecation warning) |
| 2026-11-12 | Added fail-fast runtime settings validation for required text values, API_PORT range, DATABASE_ECHO boolean tokens and SQLite/PostgreSQL SQLAlchemy URL syntax; added isolated regression coverage | PR #27 GitHub Actions run #136: compileall passed, Ruff passed, Pytest 113 passed and real Streamlit/FastAPI process smoke check passed (one existing Starlette/httpx deprecation warning) |
| 2026-11-13 | Added a direct request-scope session lifecycle regression test and completed the Phase 2 foundation acceptance review | PR #28 GitHub Actions run #139: compileall passed, Ruff passed, Pytest 114 passed and the real Streamlit/FastAPI process smoke check passed (one existing Starlette/httpx deprecation warning); human/device validation remains open in issue #14 |

## Release acceptance checklist

- [ ] Joint learner-parent flow with distinct roles/preferences and consent.
- [ ] Reviewed English/Marathi key flows with accessible guided steps and optional read-aloud.
- [ ] Eligibility states distinguish eligible, ineligible and unknown.
- [ ] Advisory recommendations explain why options are shortlisted and are not psychometric claims.
- [ ] Outcome import validates source, denominator, cohort, geography, period and units.
- [ ] Course/NSQF explanations cite official qualification records.
- [ ] Callback request queue is honest about partner availability.
- [ ] Admin dashboard is aggregate-only with small-cohort suppression.
- [ ] Optional concern changes are self-reported.
- [ ] Retrieval-grounded AI discloses evidence and unknowns; deterministic mode works offline.
- [ ] PDF report includes evidence references and caveats.
- [ ] Local SQLite and production PostgreSQL workflows are tested.
- [ ] FastAPI and Streamlit are deployed separately and E2E verified.
- [ ] CI, setup docs, screenshots, demo script, known limitations and resume summary are complete.

| 2026-11-14 | Started Phase 3 with separate immutable learner/parent context records and a source-backed three-state education eligibility evaluator | Local compileall passed; 16 focused Pytest tests passed. PR #29 CI validation pending; no official qualification criteria or real learner data added |
