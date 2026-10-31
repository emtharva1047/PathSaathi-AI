# Architecture Decision Records

## ADR-001: Python-first modular application
**Status:** Accepted  
Use Streamlit for the interface and FastAPI for API/domain access. Keep business rules in testable Python services.

## ADR-002: Eligibility and evidence are explicit
**Status:** Accepted  
Eligibility is not inferred from preference scores. Missing data is unknown. Outcome figures must carry denominator, cohort, time basis and provenance.

## ADR-003: Deterministic evidence first, LLM second
**Status:** Accepted  
Outcome metrics and qualification mappings come from structured records. LLM is used to explain retrieved evidence in accessible language, not to invent data.

## ADR-004: English + Marathi for the first demonstrator
**Status:** Accepted for MVP, pending target-user validation  
Use locale-managed strings and human-reviewed translations. Keep additional regional languages possible without redesign.

## ADR-005: Sentiment shift through explicit self-report
**Status:** Accepted  
Measure optional pre/post concern ratings and objection categories. Do not covertly infer emotion from private conversations. Admin analytics are aggregate and suppress small cohorts.

## ADR-006: Honest counsellor escalation
**Status:** Accepted  
If no real-time counsellor integration exists, expose a consented callback/follow-up request with status. Never imply that a live person is connected when they are not.
