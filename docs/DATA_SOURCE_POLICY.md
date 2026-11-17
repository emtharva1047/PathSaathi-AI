# Data Source and Provenance Policy

## Official SIH dataset note

The SIH Problem Statement 26241 entry states: "NA - dummy placement/earnings datasets to be provided for hackathon evaluation." The files and data dictionary are not yet in this repository. Treat them as the intended evaluation dataset when organisers provide them.

Until then:
- use synthetic records only for unit tests and local demos;
- label every synthetic dataset and UI view prominently as illustrative;
- do not report synthetic figures as Indian labour-market facts;
- do not infer missing earnings or placements.

## Preferred source hierarchy

1. SIH-supplied evaluation dataset and its accompanying documentation.
2. Official qualification and vocational education registries.
3. Official ministry/directorate/state department reports and tracer studies.
4. Official training provider, ITI, polytechnic and institution records.
5. Reputable secondary sources for context only, clearly labelled.

## Qualification and progression sources

- NCVET: https://ncvet.gov.in/
- National Qualification Register: https://www.nqr.gov.in/
- NCVET NQR overview: https://ncvet.gov.in/national-qualifications-register/
- Revised NSQF notification: https://ncvet.gov.in/national-skills-qualification-framework/nsqf-notification/
- Skill India Digital Hub: https://www.skillindiadigital.gov.in/

The NQR is an inventory of NSQF-aligned and approved qualifications. Qualification records may include qualification files, model curricula, industry validations and occupational maps. Use the specific qualification file for entry criteria and learning outcomes; do not infer eligibility from NSQF level alone.

## Employment and earnings sources

Potential official sources include DGT and state-government tracer studies and authorised scheme/provider monitoring reports. Examples reviewed:
- DGT listing for Uttarakhand ITI graduate tracer study: https://dgt.gov.in/en/node/1998
- Uttarakhand tracer study PDF (June 2023): https://www.dgt.gov.in/sites/default/files/2024-02/Final_Tracer_Study_Report_Uttarakhand.pdf
- DGT listing for Himachal Pradesh tracer study: https://dgt.gov.in/en/node/2003

The Uttarakhand report describes a survey of 738 ITI graduates across 36 ITIs and focuses on candidates who passed the AITT in academic year 2019. It contains trade/ITI-type employment findings and earnings bands. It is historical and state-specific; it is not a current Maharashtra estimate or a proxy for an individual provider. Preserve its exact population, cohort, sample and definitions if used for a clearly labelled research example.

## Required provenance metadata

For each dataset and record, preserve as available:
- dataset_id and version;
- source file/URL and publisher;
- import timestamp and importer/version;
- trade code/name and provider ID/name;
- state/district/region code;
- cohort/batch year and qualification/NSQF level;
- reporting period and post-training follow-up interval;
- completion denominator and placement numerator definitions;
- earnings currency, time basis, statistic type and observation count;
- source publication date and last verification date;
- data-quality status and notes.

The detailed import schema and validation rules are in docs/OUTCOME_DATA_CONTRACT.md. The conceptual metric model is in docs/OUTCOME_DATA_MODEL.md.

## Rules

- Preserve original supplied evaluation files and document transformations.
- Do not republish external data contrary to licence or terms.
- Do not combine incompatible denominators or cohort periods.
- Show cohort size, sample size and reporting period alongside metrics.
- Distinguish mean, median and range; never compare monthly and annual figures without clear normalisation.
- Do not imply historical group outcomes guarantee an individual's future outcome.
- Missing values stay unknown; do not replace with zero.
- Do not invent fees, placement rates, salary bands or provider rankings.


## Curated NQR explainer example — 17 November 2026

The prototype includes one curated public qualification record for **Assistant Baking Technician**, NQR record 12209, qualification code/version QG-03-FI-02932-2024-V2-FICSI, V4.0. The NQR page lists it at NSQF Level 3 and shows validity through 26 August 2027. The linked qualification file was approved in the 39th NSQC meeting on 27 August 2024 and contains the job description, four alternative entry routes, minimum age, module summary, total training duration and progression pathway.

Sources:
- NQR qualification record: https://www.nqr.gov.in/qualifications/12209
- Exact qualification file (PDF): https://www.nqr.gov.in/qualification/file/English%20Q-file%20Baking%20Tech..pdf
- NQR overview and its official-register role: https://nqr.gov.in/aboutus
- NQR Qualification File purpose and structure: https://nqr.gov.in/qualificationfile
- NCVET office order on selecting valid NQR qualifications (8 October 2025): https://ncvet.gov.in/wp-content/uploads/2025/10/Office_Order-_Qualifications_from_NQR_and_Issuance_of_Certificates_docx1.pdf

The example is a national qualification record, not a local training-provider offer. It does not establish district availability, seats, fees, admission or employment outcomes. Its entry rules include multiple education/experience alternatives and a minimum-age condition; the current education-only evaluator must not issue an eligibility result for it. Marathi text is a draft translation pending fluent human review. The NQR record state is attributed to the National Qualifications Register (NCVET) and was last checked on 17 November 2026; the qualification file facts are attributed to FICSI. The current-record contract requires record URL, publisher and record verification date in addition to claim-level provenance. Validity and archive state must be checked again before future use.
