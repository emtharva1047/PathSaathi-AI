# Phase 3 Acceptance Review

**Review date:** 23 November 2026  
**Project day:** 22/60  
**Phase window:** 14–23 November 2026  
**Status:** Implementation exit review; automated validation of the Day 22 cross-flow regression is pending.

## Decision boundary

Phase 3 is intended to deliver a deterministic learner/parent profile, advisory pathway exploration, source-backed qualification explanation and a guided bilingual family conversation. This review assesses that implementation scope. It does **not** certify production readiness, accessibility conformance, language quality, admission eligibility or employment outcomes.

The profile and family conversation remain session-only. Role ownership is prompt-defined, not identity-authenticated. No consent is captured for persistent sharing because persistent shared sessions belong to Phase 5.

## Acceptance evidence

| Requirement | Implemented behaviour | Evidence and limitation |
|---|---|---|
| Separate learner and parent context | Immutable `LearnerProfile` and `ParentContext` records; distinct references, fields and language preferences | `core/profiles.py`, `tests/test_profiles.py`; no names, contact details, exact address or exact income |
| Guided profile | Seven short English/Marathi steps for education, broad region, learner interests/work preferences and parent self-reported concerns/priorities | `app/profile_flow.py`; session-only; household-income band remains disabled pending an approved taxonomy |
| Advisory pathway exploration | Exact learner interest/work-preference overlaps, stable reason codes, no aptitude score; parent concerns do not rank pathways | `core/pathways.py`, `app/pathway_flow.py`; four catalogue themes are synthetic demonstrations, not official course listings |
| Eligibility | Distinct eligible/ineligible/unknown states; only verified-eligible matches can enter the eligible shortlist; unknown matches are separated and ineligible options remain explorable | `core/eligibility.py`, `core/multi_route_eligibility.py`; no admission decision |
| Alternative qualification routes | Four NQR 12209 entry routes modelled as OR alternatives with AND conditions and claim-level provenance | `data/qualifications/assistant_baking_technician_entry_routes.json`; source last checked 17 November 2026; incomplete learner facts remain unknown |
| Qualification explainer | One national NQR example shows job role, entry routes, modules, 300-hour duration, NSQF level and published progression with exact source references | `data/qualifications/assistant_baking_technician.json`; not a local provider offer, seat/fee listing or employment outcome |
| Joint family conversation | Six fixed bilingual prompts with learner, parent and shared ownership; skip/back/continue/revise and distinct response states | `app/counselling_flow.py`; no free text, covert emotion inference, API/database writes, analytics, LLM or live counsellor call |
| Profile-to-conversation handoff | Learner profile and parent self-reported context appear in separate review sections; profile data never pre-fills or overwrites prompt answers | `tests/test_counselling_flow.py`; the Day 22 cross-flow test adds a complete profile → shortlist → qualification → family-review regression |
| Read-aloud | Explicit browser-native Read/Stop for page introductions only; matching installed locale voice required; visible-text fallback; no audio recording/upload | `app/read_aloud.py`; dynamic prompts are not read aloud; browser/device and pronunciation validation remains open |

## Cross-flow invariants

The Day 22 integration test must demonstrate all of the following in English and Marathi:

1. Learner and parent references remain distinct.
2. Only learner interests/work preferences contribute shortlist reason codes.
3. Parent-reported concerns remain visible for discussion but do not become learner matching signals.
4. Synthetic catalogue options remain labelled and cannot become eligible without verified criteria.
5. The NQR multi-route result remains `unknown` when age/prior-qualification/experience evidence is missing; it never becomes an admission decision.
6. Profile context is displayed separately from the role-owned counselling answers; the learner's next-step choice and parent prompt answer remain unchanged.

The test uses fixed synthetic profile values and a Streamlit test double. It does not launch a browser, call external services or write persistent records.

## Human and external dependencies still open

- **Issue #14 — accessibility/usability:** no target-user sessions, fluent Marathi review, screen-reader testing, keyboard/focus audit, contrast measurement, mobile-device review or installed voice/pronunciation test has been completed. Automated tests do not establish WCAG conformance or user comprehension.
- **Issue #5 — SIH dummy outcome dataset:** not supplied. No placement/earnings importer or real outcome claim is accepted in this phase.
- **Issue #6 — pilot and counsellor partner:** Maharashtra/Marathi remains provisional. The current family conversation is not identity-authenticated and does not create a counsellor request.
- **Phase 5:** persistent shared sessions, participant authentication/role verification, consent and callback/follow-up queue remain future work.
- **Phase 4:** official course/outcome ingestion, source-aware import validation, filters and comparisons remain future work.
- **Phases 6–8:** retrieval-grounded LLM, PDF reporting, aggregate analytics, production PostgreSQL and deployment remain future work.

## Data and safety limitations

- The four preference-matching catalogue themes are synthetic demo records and are not official courses, NSQF qualifications, fees, placements or earnings.
- The Assistant Baking Technician record is a national qualification example. It does not establish a local training provider, district availability, admission, salary, placement, workplace safety or job security.
- The learner profile does not collect age, date of birth, prior qualification evidence or work history. Missing eligibility facts remain unknown.
- Marathi strings are drafts pending fluent human review.
- No real learner/parent records are used in development. Production use with minors requires approved consent, retention, access control and legal/privacy review.

## Phase 3 exit

The deterministic implementation scope can be marked complete only after the Day 22 cross-flow regression passes the repository's GitHub Actions checks: Python compilation, Ruff, Pytest and the live Streamlit/FastAPI smoke test. Human/device validation remains a cross-phase blocker in issue #14, not a result that may be inferred from CI.

**Next phase:** Phase 4 starts 24 November 2026 (Day 23/60). Build the provenance-aware course/outcome import and validation path using synthetic fixtures until the official SIH dataset is supplied. Keep the 31 December 2026 deadline unchanged.
