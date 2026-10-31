# Project Research — SIH Problem Statement 26241

## Official challenge metadata
- **Problem Statement ID:** 26241
- **Title:** AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education
- **Organisation / Department:** Ministry of Skill Development and Entrepreneurship (MSDE)
- **Category / Theme:** Software / Smart Education
- **Official listing:** https://www.sih.gov.in/sih2026PS
- **Dataset field:** NA — dummy placement/earnings datasets to be provided for hackathon evaluation.

The full problem statement is transcribed in docs/PROBLEM_STATEMENT_26241.md.

## Problem interpretation

The challenge is not satisfied by a generic chatbot, static course catalogue or learner-only career quiz. Its centre of gravity is:
1. joint learner-parent conversation;
2. credible and localised outcome evidence for trades and training providers;
3. plain-language explanation of trade-to-job-role and NSQF progression;
4. human escalation for unresolved concerns;
5. administrator visibility into engagement and where resistance is concentrated;
6. low-literacy and low-digital-familiarity design.

## MVP choices

- Streamlit + FastAPI + SQLAlchemy, Python-first.
- English + Marathi for the first demonstrator; locale-ready architecture for more languages.
- Broad location, academic background and optional household-income bracket for context.
- SIH dummy dataset when received; synthetic fixtures only before then.
- Sentiment shift through explicit pre/post self-report rather than hidden emotion inference.
- Callback request and status if live counsellor integration is unavailable; label it accurately.
- Admin views are aggregate with small-cohort suppression.

## Qualification and progression evidence

NCVET's National Qualification Register is an inventory of NSQF-aligned and approved qualifications. Qualification windows can contain qualification files, model curricula, industry validations and occupational maps. The NQR search interface exposes filters for academic education, experience, sector, notional hours, NSQF level, qualification type and awarding body.

- NCVET NQR overview: https://ncvet.gov.in/national-qualifications-register/
- NQR search: https://www.nqr.gov.in/qualifications-search
- Revised NSQF notification: https://ncvet.gov.in/national-skills-qualification-framework/nsqf-notification/

Use the specific qualification file for entry criteria and learning outcomes; do not infer eligibility from NSQF level alone.

## Employment and earnings evidence

The Directorate General of Training publishes ITI graduate tracer-study reports. One example is the Government of Uttarakhand's June 2023 tracer study:
- DGT report listing: https://dgt.gov.in/en/node/1998
- Report PDF: https://www.dgt.gov.in/sites/default/files/2024-02/Final_Tracer_Study_Report_Uttarakhand.pdf

The report describes a survey of 738 ITI graduates across 36 ITIs and focuses on candidates who passed the AITT in academic year 2019. It includes trade and ITI-type employment findings and earnings bands. It is historical and Uttarakhand-specific; it is not a current Maharashtra estimate and must not be presented as an outcome for an individual provider unless the underlying source supports that exact scope.

This demonstrates a possible official data-source type, not a substitute for the SIH dummy dataset or current provider-level records.

## Important data caveats

- The SIH dummy placement/earnings dataset and its data dictionary are not yet in the repository.
- Public outcome data may be state-, scheme-, trade- or cohort-level rather than provider-specific.
- Placement, post-training employment, trade-related employment, apprenticeship and self-employment are distinct measures.
- Salary averages, medians and salary bands are not interchangeable.
- Every displayed outcome must carry cohort, geography, sample/denominator, period and source.
- Missing provider-level evidence must be shown as unavailable, not imputed from a broader study.
- No real learner/parent personal data is required for the portfolio demo; use synthetic records.

## Validation dependencies

- Inspect organiser-provided dataset schema, definitions, licence and permitted use when received.
- Confirm whether Marathi is the preferred pilot language with the mentor/sponsor.
- Validate wording and accessibility with representative learners and parents where feasible.
- Confirm live counsellor escalation expectations and any approved endpoint/contact directory.
- Review privacy, consent and retention requirements before a real pilot.

## Phase 1 status

The requirements baseline is ready for Phase 2 implementation. The dataset, pilot-language and live-counsellor confirmations remain external dependencies tracked in GitHub Issues; they must not be represented as completed.