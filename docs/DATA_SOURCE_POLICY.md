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
