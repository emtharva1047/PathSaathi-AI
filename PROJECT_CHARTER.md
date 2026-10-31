# Project Charter

## Project
PathSaathi AI — SIH26241 AI-enabled career counselling and family decision-support platform for vocational education.

## Problem
Vocational pathway choices are shaped by learner interests and family perceptions. Students and parents need accessible, credible and localised information about qualifications, job roles, earnings and employment evidence, safety, progression and practical constraints. The platform must support both participants, not only the learner.

## Product vision
Provide a bilingual, low-jargon counselling experience that helps learners and families explore realistic vocational pathways together, compare evidence and request human counselling when needed.

## Target users
- Learners considering vocational education, initially after Class 10 or Class 12.
- Parents/guardians participating in the decision.
- Counsellors handling escalated questions.
- Scheme administrators reviewing aggregate engagement and concerns.
- Data curators maintaining qualification and outcome evidence.

## MVP scope
- Maharashtra pilot assumption, English + Marathi.
- Student assessment and eligibility-aware recommendations.
- Source-linked NQR/qualification and course explorer.
- Outcome evidence backend with exact metric, cohort, geography, sample and provenance.
- Shared learner-parent conversational session and separate preferences.
- Grounded AI explanations with source links and explicit uncertainty.
- Human-counsellor escalation request queue.
- Privacy-safe aggregate admin dashboard using opt-in events and self-reported feedback.
- Accessible simplified flow and PDF report.

## Out of scope for 60-day solo build
Custom foundation-model training, nationwide live course scraping, guaranteed job/salary prediction, automated admissions, native mobile apps, facial/emotion analysis, and production integrations without authorised APIs or partners.

## Success measures
- End-to-end learner-to-family-report flow works.
- English and Marathi cover the core pilot journey.
- Eligibility and recommendation logic is deterministic and tested.
- Outcome claims preserve metric definition, cohort, geography, denominator/sample and source.
- No provider-level claims are inferred from broader aggregates.
- Family preferences remain distinct and counsellor escalation requests are trackable.
- Admin analytics are aggregate and do not expose identifiable family sentiment.
- Reproducible setup, CI, deployment, screenshots and limitations are documented.

## Constraints and assumptions
Solo project, up to four focused hours per day, 60 calendar days, Python-first stack, existing LLM API rather than training a model, synthetic test profiles, small curated dataset, official SIH dummy evaluation data to be obtained through the authorised channel when available.

## Governance
The developer owns implementation. Qualification/outcome facts require source review. Production use involving minors or family data requires appropriate consent, retention controls and legal/privacy review.
