# Phase 4 acceptance review — 28 November 2026

**Project window:** Day 27 of 60 (2 November–31 December 2026)  
**Phase window:** Days 23–29 (24–30 November 2026)  
**Review status:** Provisional implementation review; final phase exit remains scheduled for 30 November.

## Decision summary

The Phase 4 application components are implemented for the source material currently available. The authorised SIH26241 placement/earnings dataset and its data dictionary have not been supplied, so an organiser-specific mapping and real-data import cannot be accepted or claimed. This is an external dependency tracked in [issue #5](https://github.com/emtharva1047/PathSaathi-AI/issues/5), not permission to invent a schema or fabricate outcomes.

The fixed 60-day schedule is unchanged. The application can proceed to Phase 5 on 1 December while issue #5 remains open; if the authorised dataset arrives later, its versioned mapping must be implemented and validated without substituting synthetic data or silently changing metric meaning.

## Acceptance matrix

| Capability | Current evidence | Status and boundary |
|---|---|---|
| Canonical outcome CSV validation | services/outcome_import.py, tests/test_outcome_import.py, docs/OUTCOME_IMPORT.md | Implemented for the documented PathSaathi canonical schema; exact headers, row widths, provenance, geography, metric, denominator, rate and earnings semantics are checked. |
| Bilingual CSV review preview | app/outcome_import_flow.py, tests/test_outcome_import_flow.py | Implemented in English/Marathi. File checks, audit metadata, all findings and all-rows-valid preview gate are present. Preview only: no persistence, approval, authenticated steward role or verified-status promotion. |
| Read-only outcome explorer | app/outcome_explorer.py, tests/test_outcome_explorer.py | Implemented with exact scope filters, bounded pagination, provenance display, verified-value gate and conservative comparisons. No pooling or unsupported aggregate derivation. |
| Read-only course catalogue explorer | app/course_explorer.py, tests/test_course_explorer.py | Implemented with exact geography/trade/provider filters, half-step NSQF validation, provenance labels and safe source links. It displays API records only; an empty catalogue is not replaced with synthetic offers. |
| Source-backed qualification explainer | app/qualification_flow.py, docs/PHASE3_QUALIFICATION_EXPLAINERS.md | Existing NQR qualification example and progression remain separately sourced. It is not represented as a local provider offer or inserted into the API catalogue. |
| Cross-layer API/UI regression | tests/test_phase4_journey.py | Added on Day 27: actual FastAPI routes, request-scoped SQLAlchemy sessions and isolated in-memory SQLite are exercised through the Streamlit course, preview and outcome renderers in both locales. |
| Official SIH dataset mapping | [Issue #5](https://github.com/emtharva1047/PathSaathi-AI/issues/5) | **Blocked:** authorised files, data dictionary and licence are absent. Do not guess columns, units, cohorts, sample definitions or provider granularity. |
| Human language/accessibility validation | [Issue #14](https://github.com/emtharva1047/PathSaathi-AI/issues/14) | **Open cross-phase follow-up:** fluent Marathi review, target-user comprehension, keyboard, screen-reader, contrast and device checks remain unverified. |

## Cross-layer regression design

The Day 27 regression test:

1. Creates an isolated in-memory SQLite schema and overrides the real FastAPI database dependency with request-scoped sessions.
2. Seeds one clearly labelled synthetic course and one synthetic outcome containing a numeric value, numerator, denominator and sample size.
3. Routes the Streamlit explorer HTTP calls through a TestClient adapter into the real FastAPI endpoints; it does not mock the API response payload.
4. Renders the course catalogue, empty CSV-preview state and outcome evidence explorer in English and Marathi.
5. Asserts the course remains labelled synthetic and the API-withheld synthetic outcome value and count metadata do not reappear in the UI.

This is an in-process integration test, not a deployed-network test, source audit, real SIH import or human usability study.

## Non-negotiable data boundaries

- Synthetic fixtures are test-only and are never presented as labour-market facts.
- Placement, employment, trade-related employment, apprenticeship and self-employment remain distinct metrics.
- Missing values remain unknown, not zero.
- Provider-level evidence requires provider-level geography; broader aggregates are not relabelled as provider results.
- Numeric outcome values, numerators, denominators and sample sizes remain withheld until the API verification contract is satisfied.
- The canonical CSV preview is not an import-to-database workflow. Authentication, curator approval, persistence and audit permissions require a separately authorised design.
- Course records do not establish provider operation, seats, admission availability, fees, placement or earnings.
- No live counsellor service, production deployment or validated psychometric assessment is implied by this phase.

## Phase exit conditions

Before the scheduled Day 29 review on 30 November:

- [x] The cross-layer English/Marathi integration test passes in GitHub Actions run [#217](https://github.com/emtharva1047/PathSaathi-AI/actions/runs/46104298781): compileall, Ruff, 312 Pytest tests and the live Streamlit/FastAPI smoke check passed (one existing Starlette/httpx deprecation warning).
- [ ] README and ROADMAP identify the SIH dataset mapping as blocked by issue #5, not complete.
- [ ] The final Phase 4 status distinguishes implemented software from unavailable external data.
- [ ] No unverified or synthetic numeric outcome is exposed.

If issue #5 remains blocked, close the Phase 4 implementation gate only for the capabilities listed above, retain issue #5 as an external dependency, and begin Phase 5 on 1 December as scheduled. Do not extend the project or claim that SIH data ingestion has been completed.
