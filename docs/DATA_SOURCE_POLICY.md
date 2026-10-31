# Data Source and Provenance Policy

## Preferred source hierarchy

1. Official qualification and vocational education registries (NCVET/NQR).
2. Official ministry/directorate/state department reports and tracer studies.
3. Official training provider, ITI, polytechnic and institution course pages.
4. Official examination/admission notices and qualification documents.
5. Reputable secondary sources for context, clearly labelled as secondary.

## Core qualification sources

- NCVET: https://ncvet.gov.in/
- National Qualification Register overview: https://ncvet.gov.in/national-qualifications-register/
- NQR search: https://www.nqr.gov.in/qualifications-search
- Revised NSQF notification: https://ncvet.gov.in/national-skills-qualification-framework/nsqf-notification/
- Skill India Digital Hub: https://www.skillindiadigital.gov.in/

The NQR is an inventory of NSQF-aligned and approved qualifications and exposes qualification files, model curricula and other supporting material. Use the individual qualification file for entry criteria and learning outcomes; do not infer eligibility from an NSQF level alone.

## Employment and earnings outcome sources

Potential official sources include DGT/state-government tracer studies and authorised scheme/provider monitoring reports. Examples reviewed:
- DGT listing for Uttarakhand ITI graduate tracer study: https://dgt.gov.in/en/node/1998
- Uttarakhand tracer study PDF (June 2023): https://www.dgt.gov.in/sites/default/files/2024-02/Final_Tracer_Study_Report_Uttarakhand.pdf
- DGT listing for Himachal Pradesh tracer study: https://www.dgt.gov.in/en/node/2003

The Uttarakhand study is historical and specific to its state/cohort/sample. It is evidence of a possible data source type, not a proxy for Maharashtra or for a particular provider. The project must preserve its exact population, cohort, sample and definitions.

The official SIH26241 listing states that the public dataset link is NA and dummy placement/earnings datasets will be provided for hackathon evaluation. Obtain those files through the authorised channel and review their licence/terms before importing.

## Required metadata for course/qualification records

- record_id, title, provider/awarding body;
- qualification level/framework only when verified;
- entry criteria and source;
- duration/notional hours and source;
- fees only when publicly verified, with date and exact scope;
- source_url and source_publisher;
- last_verified_at (ISO date);
- confidence/status: verified, needs_review, stale, unknown;
- interpretation notes.

## Required metadata for outcome records

Follow docs/OUTCOME_DATA_MODEL.md: metric definition, numerator/denominator or sample size, trade, provider if specifically supported, geography, cohort and observation period, publication date, unit, source page/table, methodology, verification status and caveats.

## Rules

- Do not scrape or republish content contrary to terms or licence.
- Do not infer official recognition from provider marketing.
- Do not invent fees, salary, employment, placement or admission claims.
- Do not label post-training employment as placement unless the source defines it that way.
- Store null/unknown where a field cannot be verified.
- Record date checked and re-check before release.
- Do not derive provider-level outcomes from state-level or trade-level aggregates.
- Keep synthetic demo data visibly labelled as synthetic.
