# Data Source and Provenance Policy

## Official SIH dataset note

The SIH Problem Statement 26241 entry states: **"NA - dummy placement/earnings datasets to be provided for hackathon evaluation."** The files have not yet been added to this repository. Treat them as the intended evaluation dataset when the organisers provide them.

Until then:
- use synthetic records only for unit tests and local demos;
- label every synthetic dataset and UI view prominently as illustrative;
- do not report synthetic figures as Indian labour-market facts;
- do not infer missing earnings or placements.

## Preferred source hierarchy
1. SIH-supplied evaluation dataset and its accompanying documentation.
2. Official qualification and vocational education registries.
3. Official training provider, ITI, polytechnic and institution records.
4. Official government scheme outcome reports and published evaluation documents.
5. Reputable secondary sources for context only, clearly labelled.

Potential reference sources:
- NCVET: https://ncvet.gov.in/
- National Qualification Register: https://www.nqr.gov.in/
- Skill India Digital Hub: https://www.skillindiadigital.gov.in/

## Required provenance metadata
Each dataset and record should preserve, as available:
- dataset_id and dataset_version
- source_file/source_url and publisher
- import_timestamp and importer/version
- trade_code and provider_id
- state/district or region code
- cohort/batch year and qualification/NSQF level
- reporting period and post-training follow-up interval
- completion denominator and placement numerator definitions
- earnings currency, time basis, statistic type, observation count
- source publication date and last_verified_at
- data-quality status and notes

## Rules
- Preserve the original supplied evaluation files and document transformations.
- Do not republish external data contrary to licence or terms.
- Do not combine incompatible denominators or cohort periods.
- Show cohort size, sample size and reporting period alongside metrics.
- Distinguish mean, median and range; never compare monthly and annual figures without normalisation and clear labels.
- Do not imply historical aggregate outcomes guarantee an individual's earnings or placement.
- Use null/unknown for missing data, not guesses.
- Do not invent fees, placement rates, salary bands or provider rankings.
