# Phase 3 — Guided joint learner-parent counselling prompts

## Purpose

This module adds a short, deterministic conversation guide so the learner and parent/guardian can record their own questions, concerns and preferences separately, then review them together. It is a discussion aid, not an automated counsellor.

## Prompt sequence

The current prototype contains six prompts followed by a review screen:

| Order | Owner | Category | Purpose |
|---:|---|---|---|
| 1 | Learner | Information to verify | Learner chooses facts they want checked before deciding |
| 2 | Parent/guardian | Self-reported concern | Parent chooses only questions or concerns they personally wish to raise |
| 3 | Learner | Preference | Learner records what matters to them |
| 4 | Parent/guardian | Information to verify | Parent chooses which official information would help a family discussion |
| 5 | Learner | Preference | Learner chooses a preferred next step |
| 6 | Shared | Family discussion | Both identify a topic to review together |

Each prompt is a fixed, optional multi-select question. There is no free-text field. The category is explicit: an information request is not evidence, a preference is not a suitability score, and a parent concern is not inferred by the system.

## Language

- English is the current prototype copy.
- Marathi keys and options are present and structurally match English.
- Marathi wording is explicitly a draft pending fluent human review. It must not be described as validated.
- The Maharashtra/Marathi pilot assumption remains subject to mentor confirmation in issue #6.

## Response state and revision semantics

Responses are stored in `st.session_state["joint_counselling_answers"]`, keyed by fixed prompt ID. Each stored record includes the prompt's fixed role and category, selected option IDs, a status and a revision count.

| State | Meaning |
|---|---|
| `not_answered` | The participant has not reached or submitted this prompt |
| `empty` | The participant continued without selecting an option |
| `skipped` | The participant explicitly used Skip |
| `answered` | One or more known options were selected |
| Revised | A prior response's status or selected options changed; the review displays the revision count alongside the current state |

Unknown option identifiers are discarded. A response is accepted only under the role assigned to its fixed prompt. Revising a learner prompt cannot overwrite a parent prompt.

The review screen preserves the learner's own next-step choice and labels parent concerns as self-reported. A parent response never overrides the learner's response.

## Privacy and integration boundary

- The flow uses only fixed option IDs; it does not collect names, phone numbers, exact income, date of birth, addresses, employer names or free-text narratives.
- Draft answers stay in the current Streamlit session.
- No API request, SQLAlchemy session, database write, counsellor request, analytics event or LLM call is made.
- The "keep" control only marks the session draft as reviewed. It is not persistent storage and does not contact a human counsellor.
- Closing or losing the Streamlit session may clear the draft.
- Do not use real learner/family data in development. Production use involving minors requires appropriate consent, retention, access-control and legal/privacy review.

## Out of scope

- No LLM-generated counselling, diagnosis, emotion inference or psychometric/aptitude score.
- No automated resolution of family disagreement.
- No claim that requested fees, safety, placement, earnings or provider facts are available.
- No live counsellor connection. A callback/follow-up request queue remains a separate, partner-dependent feature.
- No persistent shared session until Phase 5 consent and retention design is approved.

## Automated acceptance

Tests cover matching English/Marathi prompt keys and option IDs, one question at a time, fixed role ownership, self-reported parent concerns, distinct evidence/preference/discussion categories, unanswered/empty/skipped/revised states, Back/Continue, review/revise, learner agency and the session-only boundary.

Automated render tests do not establish WCAG conformance, real-device usability, screen-reader support, participant comprehension or fluent Marathi quality. Those checks remain open in issue #14.
