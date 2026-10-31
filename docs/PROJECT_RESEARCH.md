# Project Research — SIH26241

**Reviewed:** 1 November 2026  
**Official problem statement:** SIH26241 — AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education  
**Ministry:** Ministry of Skill Development and Entrepreneurship (MSDE)  
**Category/theme:** Software / Smart Education

## 1. Official problem framing

The official SIH 2026 problem-statement listing describes vocational enrolment and retention as being influenced by family perception as well as learner interest. It highlights that existing career-guidance tools are largely learner-facing and do not adequately address parental concerns, particularly in rural and semi-urban households.

The brief calls for a platform that:
- engages learners and parents jointly through a conversational interface in regional languages;
- responds to parental concerns about income potential, job security and social perception with credible local data;
- presents verified outcome data for specific trades and training providers, including post-training earnings, placement rates and progression pathways;
- explains qualifications, job roles and career growth in low-jargon language tailored to location, household-income bracket and academic background;
- provides a human-counsellor escalation route;
- tracks engagement and sentiment shifts for scheme administrators.

Expected outcomes include a working learner-parent conversational tool in at least one regional language plus English, a verified outcome-data backend, an administrator dashboard, low-literacy/low-digital-familiarity design and human escalation.

**Official source:** https://www.sih.gov.in/sih2026PS  
The official listing identifies the problem as SIH26241 and shows the dataset link as unavailable publicly, with dummy placement/earnings datasets to be provided for hackathon evaluation. The team must obtain and use the official evaluation dataset if/when supplied; it is not assumed to be publicly downloadable.

## 2. Product interpretation

The key differentiator is not a generic career chatbot. It is a joint family counselling workflow supported by credible, appropriately scoped vocational outcome evidence.

The system should answer questions such as:
- What does this qualification prepare a learner to do?
- What are the entry requirements and progression options?
- What evidence exists for employment outcomes for this trade and region?
- Does the evidence describe this exact provider, or only a wider state/cohort?
- What concerns does the parent have about cost, safety, income or job security?
- When should a human counsellor take over?

The platform must display uncertainty when data is absent or not comparable.

## 3. Initial MVP scope decision

For a solo 60-day portfolio build, use a **Maharashtra pilot** with **English and Marathi** as the initial language pair. This is a development-scope assumption, not a requirement imposed by SIH. The data model and locale system should support additional regions/languages later.

Initial learner cohort: students considering vocational pathways after Class 10 or Class 12, plus their parent/guardian. The product model should remain extensible to existing vocational learners and non-degree learners.

### Must-have prototype capabilities
1. Shared learner-parent conversational session with separate participant roles.
2. Transparent eligibility-aware pathway matching.
3. Qualification/course explorer using NQR/official provider references.
4. Outcome-evidence store with explicit metric definitions, cohort, geography, sample size and provenance.
5. English/Marathi core interface and simple-language flow.
6. Counsellor escalation request queue (clearly marked as a prototype unless connected to a real counsellor service).
7. Administrator dashboard with privacy-safe aggregate engagement and self-reported concern/confidence feedback.
8. Report export with evidence and limitations.

### Stretch / integration-dependent capabilities
- Live connection to an operational counsellor network.
- Provider-level outcome data where no public/authorised source is available.
- Voice input/output and offline sync.
- Nationwide real-time provider/course feeds.
- Advanced automated sentiment analysis. The MVP will prefer explicit, optional self-report rather than covert emotion inference.

## 4. Evidence and data availability

### Qualifications and progression
NCVET states that the National Qualification Register (NQR) is an inventory of NSQF-aligned and approved qualifications. Its records can include qualification files, model curricula, industry validation and occupational maps. The NQR search interface exposes filters such as academic education, experience, sector, notional hours, NSQF level, qualification type and awarding body.

- NCVET NQR overview: https://ncvet.gov.in/national-qualifications-register/
- NQR search: https://www.nqr.gov.in/qualifications-search
- NCVET NSQF notification: https://ncvet.gov.in/national-skills-qualification-framework/nsqf-notification/

The revised NSQF is outcome/competency-based and describes learning outcomes across knowledge, skills, aptitude and responsibility. It supports progression and mobility across vocational, general and technical education. Use the official qualification file for each specific entry criterion; do not infer eligibility from NSQF level alone.

### Employment and earnings outcomes
The Directorate General of Training (DGT) publishes tracer-study reports. For example, the Government of Uttarakhand's June 2023 tracer study of ITI graduates reports trade and ITI-type employment findings, income bands and methodology. It covers 738 surveyed graduates from 36 ITIs and focuses on candidates who passed the AITT in academic year 2019.

This is useful evidence that official/departmental tracer studies can contain trade-level outcome data, but it is historical and Uttarakhand-specific. It must not be presented as a current Maharashtra estimate or a result for an individual provider unless the source supports that exact granularity.

- DGT listing: https://dgt.gov.in/en/node/1998
- Report PDF: https://www.dgt.gov.in/sites/default/files/2024-02/Final_Tracer_Study_Report_Uttarakhand.pdf

### Skill India Digital Hub
The official Skill India Digital Hub describes course discovery, jobs, apprenticeships and multilingual access. Treat it as a discovery/reference channel; verify individual course and provider claims at the official source before storing them.

- https://www.skillindiadigital.gov.in/

## 5. Data gaps and safeguards

- SIH's listing says dummy placement/earnings datasets are to be provided for evaluation; request/obtain the official files from the authorised SIH channel rather than inventing them.
- Public outcome data may be state-, scheme-, trade- or cohort-level rather than provider-specific.
- "Placement rate", "employment status", "trade-related employment" and "apprenticeship" are different measures. Preserve source definitions.
- Salary averages, medians and salary bands are not interchangeable.
- Every displayed outcome must carry cohort, geography, sample/denominator, publication date and source.
- Missing provider-level evidence must be shown as unavailable, not imputed from a broader study.
- No real learner/parent personal data is required for the portfolio demo; use synthetic records.

## 6. Research questions still open

- Confirm the official evaluation dataset delivery channel, schema and licence/usage terms.
- Confirm whether the team has access to a counsellor partner for a real escalation workflow.
- Validate the Maharashtra/Marathi pilot assumption with the project mentor/team.
- Identify current, authorised Maharashtra outcome data with provider-level granularity, if any.
- Review the complete SIH evaluation rubric and any additional sponsor instructions.
