# Outcome Evidence Data Model

## Purpose

Represent employment and earnings evidence without flattening different studies into misleading universal "placement" or "salary" numbers.

## Required fields

| Field | Meaning |
|---|---|
| evidence_id | Stable record identifier |
| metric_code | e.g. trade_related_employment_rate, apprenticeship_share, median_monthly_earnings |
| metric_label | Human-readable metric |
| definition | Exact source definition; never silently reinterpret |
| numerator | Count meeting the metric, when available |
| denominator | Eligible population used for the rate, when available |
| sample_size | Survey/respondent sample size |
| trade_or_job_role | Trade/job role represented |
| provider_id | Exact training provider/ITI, only if the source identifies it |
| provider_type | Government, private, project ITI, etc., if source-defined |
| geography_level | National, state, district, provider |
| geography_code/name | Geographic scope |
| cohort_period | Training/completion cohort |
| observation_period | When outcome was measured |
| publication_date | Date report/source was published |
| value | Numeric value only when source reports it |
| lower_value / upper_value | For a reported range, if applicable |
| salary_band | Original source salary band, where applicable |
| currency / unit | e.g. INR per month |
| source_url | Direct official source/report URL |
| source_publisher | Issuing department/agency |
| source_page_or_table | Page, section or table reference |
| methodology | Survey/administrative-data method and relevant limitations |
| last_verified_at | Last date source was checked |
| verification_status | verified, needs_review, stale, synthetic_demo |
| notes | Caveats and interpretation notes |

## Metric semantics

Do not conflate:
- formal placement by a training provider;
- employment after training;
- employment in the trained trade;
- unrelated employment;
- apprenticeship;
- self-employment;
- current employment at the time of a tracer survey.

For each rate, preserve the source denominator. If the source reports percentages but not counts, store the published percentage and note that numerator/denominator were not published.

For earnings:
- show the source's salary band if it reports bands;
- label mean and median explicitly;
- distinguish earnings among employed respondents from earnings among all graduates;
- preserve monthly/annual unit and survey period;
- do not convert or extrapolate without a documented method.

## Granularity and display rules

1. Provider-level evidence requires a provider-specific source sample. Do not derive it from state averages.
2. Trade-level evidence must identify the trade and cohort.
3. State-level evidence is labelled state-level, not local district evidence.
4. Historical data displays its cohort and publication date prominently.
5. Suppress or warn on small samples; do not expose identifiable respondent-level records.
6. If filters requested by the user are narrower than source coverage, explain the mismatch and offer the broader evidence with an explicit label.
7. If evidence is absent, show "No verified data available for this exact scope" rather than a guessed value.

## Import policy

- Support CSV/JSON import for the SIH-provided dummy evaluation dataset once obtained.
- Validate schema, metric definitions, denominator/sample size, cohort, geography, units and provenance before accepting records.
- Store the original source file hash and import timestamp for reproducibility.
- Synthetic fixtures must use verification_status=synthetic_demo and must never be displayed as real outcomes.
