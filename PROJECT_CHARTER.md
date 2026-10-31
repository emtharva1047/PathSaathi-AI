# Project Charter

## Project
PathSaathi AI — AI-enabled career counselling and family decision-support platform for vocational education.

## Problem
Students exploring vocational education and their families may lack structured guidance, accessible course information, and a collaborative way to compare pathways against interests, eligibility, cost, distance, duration, and further-study options.

## Product vision
Provide a transparent decision-support workflow that helps students explore realistic vocational options and enables families to discuss them using evidence rather than assumptions.

## Target users
- Students after Class 10 or Class 12 considering vocational education.
- Parents/guardians supporting education decisions.
- Counsellors reviewing assessments and advising students.
- Administrators maintaining course and career information.

## Objectives
1. Gather a structured student profile and preferences.
2. Filter out courses for which eligibility is not met or not known.
3. Rank suitable pathways using explainable, configurable matching criteria.
4. Present course facts with provenance and freshness metadata.
5. Support student-parent comparison and discussion.
6. Generate a shareable report with caveats and next steps.
7. Demonstrate professional software engineering through tests, CI, deployment and documentation.

## In scope
Student assessment, profile, eligibility-aware recommendation, vocational course catalogue, career pathway information, family decision room, grounded AI counsellor, PDF report, basic admin/counsellor tools, tests and deployment.

## Out of scope for the 60-day solo build
Custom foundation-model training, nationwide real-time course scraping, guaranteed job/salary prediction, automated admissions/enrolment, native mobile apps, facial/emotion analysis, and production-grade institutional integrations.

## Success measures
- Core student-to-report workflow completes without manual database edits.
- At least three suitable options are shown when the dataset contains them; otherwise the platform explains why fewer are available.
- Every recommendation exposes its matching factors and eligibility status.
- Factual course records include source URL and last verified date.
- Parent and student preferences remain distinct and visible.
- Unit/integration tests cover core rules and access restrictions.
- Reproducible setup, CI, deployment instructions and known limitations are documented.

## Constraints and assumptions
Solo project, approximately four focused hours daily, 60 calendar days, Python-first stack, existing LLM API rather than training a model, synthetic test profiles, small initial curated dataset.

## Governance
The developer owns implementation and release. Recommendation assumptions and course facts require review; production deployment for minors requires privacy/legal review and appropriate consent controls.
