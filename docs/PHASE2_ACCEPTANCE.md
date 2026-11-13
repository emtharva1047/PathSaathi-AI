# Phase 2 Foundation — Acceptance Review

**Review date:** 13 November 2026  
**Project window:** Days 6–12 (7–13 November 2026)  
**Decision:** **Accepted — Phase 2 foundation complete.** Phase 3 begins on 14 November 2026.

## Acceptance matrix

| Exit criterion | Result | Evidence |
|---|---|---|
| Streamlit and FastAPI application skeleton | Pass | Streamlit shell, FastAPI app and database-independent `/health` route are present. |
| English/Marathi navigation scaffold | Pass | Locale-managed page copy, visible progress, Back/Continue and contextual Help are implemented. Human translation/usability review remains open. |
| Runtime configuration and logging | Pass | Required settings, API port, boolean tokens and supported SQLite/PostgreSQL URL syntax are validated before serving. URL validation does not connect to a database. |
| SQLAlchemy 2.x and local SQLite | Pass | Course/outcome models, repositories, explicit `create_schema(engine)`, isolated in-memory SQLite tests and local SQLite default are implemented. Import/startup does not create tables. |
| PostgreSQL-ready configuration | Pass (configuration only) | PostgreSQL SQLAlchemy URL parsing and optional Psycopg 3 extra are supported. No managed database is provisioned in Phase 2. |
| Request-scoped database sessions | Pass | Lazy engine/session-factory lifecycle is tested; the additional regression test proves separate dependency invocations yield distinct sessions and close them on completion. |
| Read-only catalogue/evidence API | Pass | Course/outcome list/detail endpoints use exact filters and bounded pagination; provider filters require provider-level geography. |
| Evidence-display safeguards | Pass | Unverified numeric values and numerator/denominator/sample-size counts are withheld; absent values remain unknown/null. Source provenance is exposed with cohort, geography and period context. |
| Automated quality gate | Pass | GitHub Actions run #139 completed successfully for PR #28. |

## Verified CI evidence

[PR #28](https://github.com/emtharva1047/PathSaathi-AI/pull/28) was validated by [GitHub Actions run #139](https://github.com/emtharva1047/PathSaathi-AI/actions/runs/43358907285) on 13 November 2026:

- `python -m compileall -q app backend core database services scripts` — passed.
- `ruff check .` — passed (`All checks passed!`).
- `pytest -q` — **114 passed**, with one existing Starlette/httpx deprecation warning.
- `python scripts/smoke_test.py` — passed. The real Streamlit process remained healthy while the configured FastAPI service transitioned offline → online → offline.

This is GitHub Actions evidence; no claim is made that a four-hour local work session elapsed.

## Scope boundaries and known limitations

- SQLite is the local development database. PostgreSQL support in this phase is URL/driver configuration only; credentials, connectivity, migrations, managed hosting and deployment are Phase 8 work.
- Catalogue and outcome endpoints are read-only. Dataset import, write workflows, authentication/production authorisation and family-session persistence are not part of this foundation gate.
- The SIH dummy placement/earnings dataset has not been supplied. Synthetic fixtures are test-only and must not be presented as real outcomes; see [issue #5](https://github.com/emtharva1047/PathSaathi-AI/issues/5).
- A `source_verified` response flag reflects the record's verification status and required provenance fields; it is not an independent audit or guarantee of source accuracy.
- Automated rendering and process tests do not establish WCAG conformance, screen-reader compatibility, contrast, mobile usability or comprehension. Human/device review and fluent Marathi review remain open in [issue #14](https://github.com/emtharva1047/PathSaathi-AI/issues/14).
- The Maharashtra/Marathi pilot assumption and availability of a real counsellor partner remain subject to external confirmation; until then, escalation must be described as a callback/follow-up request queue. See [issue #6](https://github.com/emtharva1047/PathSaathi-AI/issues/6).
- Production PostgreSQL, migrations and deployment remain scheduled for Phase 8 under [issue #11](https://github.com/emtharva1047/PathSaathi-AI/issues/11).

## Phase 3 entry sequence (14–23 November)

1. Define separate typed learner and parent context models. Keep learner preferences, parent concerns and contributions attributed to their participant roles.
2. Collect only broad optional location and household-income bands plus relevant academic background; never require exact income or address.
3. Represent eligibility as exactly `eligible`, `ineligible` or `unknown`, with rule reasons and source references. Missing or ambiguous entry criteria must remain unknown.
4. Implement deterministic, explainable pathway shortlisting. It is advisory exploration, not a validated aptitude or psychometric assessment.
5. Add guided English/Marathi prompts and tests for learner agency, role separation, missing data and eligibility boundaries.
