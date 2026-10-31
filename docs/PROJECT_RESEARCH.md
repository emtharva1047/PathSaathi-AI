# Project Research — SIH Problem Statement 26241

## Official challenge metadata supplied by project owner

- **Problem Statement ID:** 26241
- **Title:** AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education
- **Organisation:** Ministry of Skill Development and Entrepreneurship (MSDE)
- **Department:** Ministry of Skill Development and Entrepreneurship (MSDE)
- **Category:** Software
- **Theme:** Smart Education
- **Dataset field:** "NA - dummy placement/earnings datasets to be provided for hackathon evaluation"
- **YouTube link / contact info:** blank in the supplied details.

The complete background, challenge description and expected outcomes transcribed from the provided SIH screenshot/text are recorded in `docs/PROBLEM_STATEMENT_26241.md`.

## Problem interpretation

The brief identifies family perception as a factor shaping vocational enrolment, retention and progression. It describes an important gap in learner-only career guidance: parents may influence or veto vocational choices, particularly when concerned about earning potential, safety and social standing. The product must therefore make the family unit part of counselling.

The challenge is not satisfied by a generic chatbot, a static course catalogue or an individual career score. Its centre of gravity is:
1. joint learner-parent conversation;
2. credible and localised outcome evidence for trades and training providers;
3. plain-language explanation of trade-to-job-role and NSQF progression;
4. human escalation for unresolved concerns;
5. administrator visibility into engagement and where resistance is concentrated;
6. low-literacy and low-digital-familiarity design.

## Product hypothesis

PathSaathi AI will provide one shared counselling journey where learner and parent can ask questions in English or a regional language, see relevant local evidence and understand qualification pathways. A human counsellor request is available when the evidence is insufficient or the family needs personal support. Scheme administrators see privacy-protected aggregate trends.

## MVP choices

- Streamlit + FastAPI + SQLAlchemy, Python-first.
- English + Marathi for the first demonstrator; locale-ready architecture for more languages.
- Use broad location, academic background and optional household-income bracket for context.
- Use SIH dummy dataset when received; synthetic fixtures only before then.
- Track sentiment shift through explicit pre/post self-report rather than hidden emotion inference.
- Implement callback request and status if live counsellor integration is unavailable; label it accurately.
- Admin views are aggregate with small-cohort suppression.

## Important data caveats

The SIH entry says datasets will be provided, but they are not in the supplied materials. No earnings/placement figures can be responsibly claimed yet. The import contract is in `docs/OUTCOME_DATA_CONTRACT.md`.

## Validation still needed

- Inspect organiser-provided dataset schema, definitions, licence and permitted use when received.
- Confirm which regional language is preferred for the actual target pilot; Marathi is the initial MVP language choice, not a restriction on later locales.
- Validate wording and accessibility with representative learners and parents.
- Confirm live counsellor escalation expectations and whether the organisers offer an endpoint or contact directory.
- Confirm privacy, consent and retention requirements for any pilot.

## Initial conclusion

The current 60-day roadmap has been rebalanced to cover every expected SIH outcome while protecting a demonstrable end-to-end workflow. Phase 1 remains open until data and user assumptions are validated and the acceptance checklist is reviewed.
