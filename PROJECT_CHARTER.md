# Project Charter — PathSaathi AI

## Official challenge

- **Problem Statement ID:** 26241
- **Title:** AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education
- **Organisation/Department:** Ministry of Skill Development and Entrepreneurship (MSDE)
- **Category:** Software
- **Theme:** Smart Education
- **Source:** SIH problem statement details supplied by the project owner; transcribed in `docs/PROBLEM_STATEMENT_26241.md`.

## Problem

The SIH brief identifies family perception as an important influence on vocational training enrolment, retention and progression. Existing learner-facing guidance can help an individual choose a course but may not address parents' concerns about earning potential, safety, job security and social standing. The challenge is to engage the learner and family together with credible, localised evidence and accessible explanations.

## Vision

Build a bilingual, low-jargon, family-inclusive counselling platform that uses specific trade/provider outcome evidence to help learners and parents discuss vocational choices, understand job-role and NSQF progression, and reach a human counsellor when AI guidance is insufficient.

## Core objectives

1. Support a joint learner-parent conversational counselling journey.
2. Provide English plus at least one regional language (MVP target: Marathi).
3. Import and query verified or hackathon-provided placement and post-training earnings data by trade, provider and locality.
4. Explain outcome evidence with cohort size, denominator, time period and limitations.
5. Explain trade-to-job-role mapping and NSQF progression in plain language, tailored to broad location, household income bracket and academic background.
6. Provide human counsellor escalation.
7. Give scheme administrators aggregate insight into engagement, objection themes and self-reported concern shifts.
8. Demonstrate low-literacy and low-digital-familiarity design.

## Scope for 60-day solo MVP

- Streamlit UI and FastAPI backend.
- Student/parent role-aware shared conversation.
- English and Marathi key flows.
- Context profile with broad region, education and optional household income bracket.
- Outcome dataset import contract and validation; integrate the SIH dummy dataset once supplied.
- Source/provenance-aware placement and earnings summaries.
- Plain-language trade/job-role/NSQF explainers.
- Counsellor callback/escalation request and status.
- Aggregate admin dashboard with privacy controls.
- Explicit self-reported concern check-in before/after counselling.
- Tests, CI, deployment and demo documentation.

## Explicit exclusions

Custom LLM training; nationwide live scraping; guaranteed earnings or employment prediction; actual call-centre/CRM integration without an approved endpoint; covert sentiment or emotion detection; household-level surveillance; native mobile applications.

## Success criteria

- One complete family counselling journey works in English and Marathi.
- Outcome evidence can be filtered by trade/provider/region and includes its cohort/period/denominator/provenance.
- Data gaps are shown as unknown, not fabricated.
- NSQF/job-role progression is explainable with traceable source references.
- Users can submit a human-counsellor request and view status.
- Admin metrics are aggregated and small cohorts suppressed.
- Low-literacy design decisions are demonstrated and tested with representative feedback if available.
- Core security, data handling and application tests pass.

## Constraints

Solo developer, approximately four focused hours daily, 60 days, Python-first stack, small initial scope, SIH-provided dummy placement/earnings dataset pending.

## Governance

Recommendation weights and explainer content are guidance, not validated psychometrics. Human counsellors remain important for nuanced or high-impact decisions. Production use, especially with minors and household data, requires legal/privacy review and approved consent/retention processes.
