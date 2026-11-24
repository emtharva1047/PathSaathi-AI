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
| 3. Counselling/profile/pathway | 13–22 | 14–23 Nov | Learner and parent context, guided bilingual prompts, advisory shortlisting, eligibility and source-backed explainers | Deterministic recommendations, eligible/ineligible/unknown outcomes, explainable tests | Complete (23 Nov) |
| 4. Course/outcome explorer | 23–29 | 24–30 Nov | SIH dummy-data importer when supplied, validation, source-linked qualifications/outcomes, filters and comparisons | Provenance-aware import report and accurate comparison semantics | In progress (24 Nov) |
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
- [x] Add 16 focused local tests for profile separation, data minimization, source provenance and all eligibility states. GitHub Actions PR run #142 and merged-main run #144 both passed compileall, Ruff, 130 Pytest tests and the live Streamlit/FastAPI process smoke check (one existing Starlette/httpx deprecation warning).
- [x] Add seven-step, one-question-at-a-time profile capture in English and Marathi for learner education, broad optional region, learner interests/work preferences, parent-reported concerns and parent priorities.
- [x] Keep the draft in Streamlit session state only; do not write profiles to the API/database before consent and retention design. Leave household-income bands uncollected until a pilot taxonomy is approved.
- [x] Add bilingual UI/domain integration tests for one-question rendering, back/continue navigation, role separation, optional unknowns, Marathi language and session-only save. PR #32 merged as `b2c9ee6`; GitHub Actions run #148 passed compileall, Ruff, 138 Pytest tests and the live Streamlit/FastAPI process smoke check (one existing Starlette/httpx deprecation warning).
- [x] Build deterministic advisory shortlisting from learner-stated interests and work preferences only; return exact reason codes and English/Marathi explanations without aptitude or ability scores.
- [x] Keep every catalogue option explorable when preferences are empty or unmatched; use stable identifier tie-breaking and no learner ranking.
- [x] Apply eligibility as a hard gate: only verified-eligible preference matches enter the eligible shortlist; unknown matches are separated for verification and ineligible matches remain explore-only.
- [x] Add a bilingual Streamlit explorer with four clearly labelled synthetic themes and no fabricated course, NSQF, fee or outcome claims.
- [x] GitHub Actions PR run #154 and merged-main run #155 passed compilation, Ruff, 159 Pytest tests and the live Streamlit/FastAPI smoke check; eligibility-gate follow-up PR #35 run #157 also passed the same checks (one existing Starlette/httpx deprecation warning per run).

- [x] Add a curated, source-backed NQR qualification explainer with job description, alternative entry routes, minimum age, learning modules, total duration, NSQF level, progression and NQR validity.
- [x] Withhold claims when the qualification is expired, archived, unknown or lacks complete claim-level provenance; mark Marathi translation as draft until human review.
- [x] Support whole and half-step NSQF levels with Decimal domain values, SQL NUMERIC(3,1), query validation and API numeric serialization.
- [x] Model alternative qualification entry routes as OR branches with AND conditions, using exact qualification code/version and source provenance per condition.
- [x] Add education, verified prior NSQF, verified relevant experience and minimum-age conditions with conservative eligible/ineligible/unknown evaluation.
- [x] Curate all four Assistant Baking Technician routes from NQR 12209 / the FICSI qualification file; the result stays unknown until required learner facts are supplied and verified.
- [x] Add English/Marathi condition and route explanations without collecting date of birth or employer names; keep the education-only evaluator unchanged.
- [x] Add focused tests for alternative routes, half-step NSQF levels, AND requirements, age boundaries, incomplete/unverified evidence, stale sources and privacy boundaries.
- [x] Integrate the multi-route evaluator into the Streamlit qualification explorer. Reuse only the saved session-only education level; display all four routes, every condition's bilingual status/explanation, exact source references and the reason the overall result remains unknown. Do not collect age, date of birth, prior-qualification documents or work history in this UI.
- [x] Add six deterministic joint counselling prompts in English and Marathi: learner evidence questions, parent self-reported concerns, learner priorities, parent information needs, learner next step and a shared family discussion topic.
- [x] Keep every answer under a fixed prompt ID and role; distinguish unanswered, empty, skipped and answered states, and record revision counts when a participant changes a response.
- [x] Add one-question-at-a-time controls, optional Skip, Back/Continue, a role-separated review and per-answer revision. The learner's own next-step choice remains visible and parent concerns are explicitly self-reported.
- [x] Keep the draft in Streamlit session state only; no API, database, counsellor, analytics or LLM call. Use fixed option IDs rather than free text; Marathi is marked draft pending human review.
- [x] Display saved learner education, broad region, interests and work preferences beside the family conversation review, separately from parent self-reported concerns/priorities; missing profile fields remain not provided and never prefill prompt answers.
- [x] Validate profile-context rendering and answer separation in English/Marathi, including populated, empty and absent profiles. PR #43 merged as `e8b7f4f`; PR run #187 and merged-main run #188 passed compileall, Ruff, 214 Pytest tests and the live Streamlit/FastAPI smoke check (one existing Starlette/httpx deprecation warning per run); issue #42 closed.
- [x] Add opt-in browser-native read-aloud for each page introduction in English and Marathi, with explicit Read/Stop controls, installed locale-matching voices, visible-text fallback and no audio recording/upload.
- [x] Test HTML escaping, locale labels, explicit activation, Stop behaviour and Streamlit integration.
- [x] Add a cross-flow Phase 3 regression for saved learner/parent context → learner-only advisory shortlist → source-backed multi-route eligibility → role-separated family review; verify missing evidence remains unknown and answers remain unchanged. PR #45 merged as `2e4e2d8`; PR run #193 and merged-main run #194 passed compileall, Ruff, 222 Pytest tests and live Streamlit/FastAPI smoke checks (one existing Starlette/httpx deprecation warning per run). PR #44 merged as `96f914c`; PR run #190 and merged-main run #191 passed compileall, Ruff, 220 Pytest tests and the live Streamlit/FastAPI smoke check (one existing Starlette/httpx deprecation warning per run). Browser/device voice availability, Marathi pronunciation and screen-reader behaviour remain open in issue #14.

## Phase 3 exit review — 23 November 2026

The implementation review is recorded in [PHASE3_ACCEPTANCE.md](docs/PHASE3_ACCEPTANCE.md). The Day 22 cross-flow regression merged as PR #45 (`2e4e2d8`); PR run #193 and merged-main run #194 passed Python compilation, Ruff, 222 Pytest tests and the live Streamlit/FastAPI smoke test. Phase 3's deterministic implementation scope is complete. Human Marathi, target-user, screen-reader, keyboard, contrast, mobile and device voice validation remain open in issue #14 and are not inferred from automated tests.

## Phase 4 progress — 24 November 2026

- [x] Create issue [#46](https://github.com/emtharva1047/PathSaathi-AI/issues/46) for the canonical provenance-aware CSV import boundary.
- [x] Add a strict UTF-8 CSV preview parser with exact header mapping, file/row limits, dataset identity, source filename, SHA-256 and UTC import timestamp.
- [x] Validate metric/geography/status semantics, source references, provider granularity, count bounds, rate reconciliation, earnings units/statistics and ISO dates.
- [x] Preserve blank values as unknown; derive a rate only from an explicit valid numerator/denominator pair and emit a warning.
- [x] Prevent uploaded files from asserting verified status; require all-or-nothing readiness before records can be staged.
- [x] Add synthetic-only row/header/provenance/numeric/error-path tests. The importer is preview-only and makes no database writes.
- [x] GitHub Actions run #199 passed compileall, Ruff, 249 Pytest tests and the live Streamlit/FastAPI smoke check; one existing Starlette/httpx deprecation warning.
- [ ] Add Streamlit import preview and controlled repository staging; map the official SIH file only after its data dictionary is received (issue #5).

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

| 2026-11-14 | Started Phase 3 with separate immutable learner/parent context records and a source-backed three-state education eligibility evaluator | PR #30 / Actions run #142 and merged-main run #144: compileall and Ruff passed, 130 Pytest tests passed and live Streamlit/FastAPI smoke check passed (one existing Starlette/httpx deprecation warning); no official qualification criteria or real learner data added |
| 2026-11-15 | Added a seven-step bilingual learner/parent profile wizard with separate role-owned fields, optional broad region, unknown-preserving defaults, full-width controls and a session-only review/save; income-band capture remains disabled pending an approved taxonomy | PR #32 merged as `b2c9ee6`; Actions run #148 passed compileall, Ruff, 138 Pytest tests and the live Streamlit/FastAPI process smoke check (one existing Starlette/httpx deprecation warning); issue #31 closed |
| 2026-11-16 | Added deterministic learner-preference pathway matching, exact reason codes, bilingual explanations, separate source-backed education eligibility and an unrestricted synthetic-demo exploration screen | PR #34 merged as `ea0a145`; PR run #154 and merged-main run #155 passed compileall, Ruff, 159 Pytest tests and the live Streamlit/FastAPI smoke check (one existing Starlette/httpx deprecation warning per run); issue #33 closed; eligibility-gate follow-up PR #35 run #157 passed compileall, Ruff, 159 tests and live smoke check |
| 2026-11-17 | Added a provenance-gated bilingual NQR qualification explainer using Assistant Baking Technician (NQR 12209; code/version QG-03-FI-02932-2024-V2-FICSI, V4.0), including alternative entry routes, learning modules, NSQF progression and validity; expanded NSQF domain, persistence and API filters to support exact half-levels | PR #36 merged as 8f681248; PR run #165 and merged-main run #166 passed compileall, Ruff, 176 Pytest tests and live Streamlit/FastAPI smoke checks (one existing Starlette/httpx deprecation warning per run); issue #37 opened for multi-route eligibility; no provider availability or outcome figures inferred; Marathi translation remains unreviewed |
| 2026-11-18 | Added source-backed OR/AND eligibility routes for Assistant Baking Technician: Grade 10; Grade 8 + 36 months; NSQF 2.5 + 18 months; NSQF 2 + 36 months; minimum age 16 on every route. Missing or unverified learner evidence remains unknown; age is completed years only and experience uses opaque evidence references. | PR #38 merged as c1e659a; PR run #168 and merged-main run #169 both passed compileall, Ruff, 192 Pytest tests and the live Streamlit/FastAPI smoke check (one existing Starlette/httpx deprecation warning per run); issue #37 closed. The education-only evaluator remains unchanged; no admission decision is made. |
| 2026-11-19 | Integrated the source-backed multi-route eligibility evaluator into the Streamlit qualification explorer, using only saved session-only education; rendered all four routes, every condition, bilingual explanations and exact source links; expired criteria now hide route thresholds and exact criterion references. | PR #39 merged as `493024c`; PR run #176 and merged-main run #177 passed Python compilation, Ruff, 197 Pytest tests and the live Streamlit/FastAPI smoke check (one existing Starlette/httpx deprecation warning); issue #40 opened for the guided joint counselling prompt flow. |
| 2026-11-20 | Added a six-prompt deterministic joint learner-parent conversation with role-owned answers, explicit question/preference/discussion categories, optional skip, Back/Continue, revision tracking and a final family review; integrated it as a fourth bilingual Streamlit page. All responses remain session-only with no external writes. | PR #41 merged as `0f03eb3`; PR validation runs #181, #182 and #183 passed Python compilation, Ruff, 211 Pytest tests and the live Streamlit/FastAPI smoke check (one existing Starlette/httpx deprecation warning); issue #40 closed. Role ownership is prompt-defined rather than identity-authenticated; consent and persistent shared sessions remain Phase 5 work. Issue #14 remains open for human Marathi, target-user, assistive-technology and device checks. |
| 2026-11-21 | Connected saved profile context to the joint conversation review: learner education/region/interests/work preferences and parent self-reported concerns/priorities appear in separate sections; missing context remains not provided and profile values never prefill prompt answers. | PR #43 merged as `e8b7f4f`; PR run #187 and merged-main run #188 passed compileall, Ruff, 214 Pytest tests and live Streamlit/FastAPI smoke checks (one existing Starlette/httpx deprecation warning per run); issue #42 closed. Marathi remains draft; issue #14 remains open for human/device validation. |
| 2026-11-22 | Added opt-in browser-native read-aloud for the page introduction on all four pages in English/Marathi, using an installed matching device voice only after explicit Read activation; added Stop, localised status/fallback, escaped text and no audio recording/upload. | PR #44 merged as `96f914c`; PR run #190 and merged-main run #191 passed compileall, Ruff, 220 Pytest tests and live Streamlit/FastAPI smoke check (one existing Starlette/httpx deprecation warning per run). Dynamic prompts are not read aloud; real-device voice availability, Marathi pronunciation and screen-reader behaviour remain open in issue #14. |
| 2026-11-23 | Completed the Phase 3 exit review with a cross-flow regression for saved learner/parent context → learner-only advisory shortlist → source-backed NQR multi-route eligibility → role-separated family review in English/Marathi. | PR #45 merged as `2e4e2d8`; PR run #193 and merged-main run #194 passed compileall, Ruff, 222 Pytest tests and live Streamlit/FastAPI smoke checks (one existing Starlette/httpx deprecation warning per run). |
| 2026-11-24 | Started Phase 4 with a canonical, provenance-aware CSV preview importer: strict headers/row widths, file hash and dataset metadata, metric/geography/status validation, provider-scope safeguards, rate/count reconciliation, earnings semantics and all-or-nothing readiness. | PR #47; GitHub Actions run #199 passed compileall, Ruff, 249 Pytest tests and the live Streamlit/FastAPI smoke check (one existing Starlette/httpx deprecation warning). Runs #196–198 exposed two test-fixture defects; both were corrected before the successful run. Official SIH dataset remains unavailable in issue #5; no data is persisted and no real outcomes are claimed. |

## Release acceptance checklist

- [x] Deterministic joint learner-parent prompt/review flow with distinct role-owned answers and learner-agency guardrails (session-only prototype).
- [x] Saved learner/parent profile context is displayed separately from conversation answers; missing values remain not provided and profile data never auto-fills prompt responses.
- [ ] Phase 5 consent, persistent shared-session workflow and counsellor callback request queue.
- [ ] Reviewed English/Marathi key flows with accessible guided steps and optional read-aloud.
- [x] Eligibility states distinguish eligible, ineligible and unknown.
- [x] Advisory recommendations explain why options are shortlisted and are not psychometric claims.
- [ ] Outcome import validates source, denominator, cohort, geography, period and units.
- [x] Add a source-backed NQR qualification explainer with exact record validity, entry routes, job-role summary and NSQF progression; full catalogue ingestion remains Phase 4.
- [ ] Callback request queue is honest about partner availability.
- [ ] Admin dashboard is aggregate-only with small-cohort suppression.
- [ ] Optional concern changes are self-reported.
- [ ] Retrieval-grounded AI discloses evidence and unknowns; deterministic mode works offline.
- [ ] PDF report includes evidence references and caveats.
- [ ] Local SQLite and production PostgreSQL workflows are tested.
- [ ] FastAPI and Streamlit are deployed separately and E2E verified.
- [ ] CI, setup docs, screenshots, demo script, known limitations and resume summary are complete.

