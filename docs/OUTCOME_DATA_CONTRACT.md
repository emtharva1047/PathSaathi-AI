# Outcome Dataset Contract — SIH PS 26241

## Purpose
Define an import/query contract for the dummy placement and earnings datasets referenced in the SIH brief. Official files and the data dictionary have not yet been supplied; map this provisional contract to the organiser's actual schema before displaying real metrics.

## Recommended logical fields

| Field | Meaning | Validation |
|---|---|---|
| dataset_id / version | Source dataset identity and revision | Required |
| trade_code / trade_name | Training trade | Required |
| provider_id / provider_name | Training provider | Required for provider-specific records |
| state / district / region_code | Locality | Preserve supplied codes |
| cohort_id / batch_year | Training cohort | Required when available |
| qualification_id / nsqf_level | Qualification and NSQF level | Preserve source definition |
| enrolled_count | Learners enrolled | Non-negative integer |
| completed_count | Learners completing | 0 <= completed <= enrolled when both exist |
| placed_count | Learners placed under source definition | 0 <= placed <= denominator |
| placement_denominator | Cohort used to calculate placement | Required to calculate rate |
| placement_rate | placed_count / denominator | Derive and reconcile |
| earnings_currency | Currency code | Required when earnings exist |
| earnings_period | Monthly, annual or source-defined period | Required when earnings exist |
| earnings_mean / median | Post-training earnings statistic | Preserve exact definition |
| earnings_min / max | Observed range | min <= max |
| earnings_sample_size | Number of earnings observations | Required for interpretation where available |
| follow_up_months | Months after training when measured | Preserve source definition |
| employment_definition | Source definition of placed/employed | Preserve or reference source dictionary |
| source_reference | Source file, report or URL | Required |
| published_at / last_verified_at | Source and verification dates | ISO dates when available |
| data_quality_status | verified, needs_review, incomplete, synthetic | Required |

## Calculation and display rules
- Calculate placement rate only when numerator and denominator describe the same cohort and time window.
- Store and display numerator, denominator and cohort size with the percentage.
- Do not compare earnings without currency and time basis.
- Label mean, median or range; include observation count and follow-up period where provided.
- Do not aggregate unlike providers, regions, cohorts or follow-up periods without labelling the aggregation.
- Missing values stay unknown; do not replace with zero.
- Preserve original input files and document transformations.
- Do not imply historical group outcomes guarantee an individual's future outcome.

## Synthetic fixtures
Synthetic data may test parsing, validation and UI states. Every record must carry `data_quality_status=synthetic`, and the interface must clearly label such results as illustrative. Synthetic figures must never be presented as actual Indian labour-market or provider outcomes.

## Validation tests
- Missing required identifiers.
- Duplicate source rows.
- Negative counts and impossible numerator/denominator relationships.
- Earnings without currency/period.
- Inconsistent dates.
- Rate mismatch against numerator/denominator.
- Failed provider/trade/region mapping.
- Missing dataset or row provenance.

## Open dependency
When the SIH files arrive, inspect the data dictionary, units, cohort definitions, suppression policy and permitted use. Create a versioned mapping before importing.
