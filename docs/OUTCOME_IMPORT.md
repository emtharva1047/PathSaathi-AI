# Outcome CSV Import and Validation

**Phase:** 4 — Course/outcome explorer  
**Status:** Canonical importer foundation; organiser-specific SIH mapping is pending.

## Current dependency

The SIH26241 brief says dummy placement/earnings data will be supplied for evaluation. The authorised files and data dictionary are not yet in this repository. Issue [#5](https://github.com/emtharva1047/PathSaathi-AI/issues/5) remains open.

The importer therefore accepts only a documented **canonical PathSaathi CSV contract** and synthetic test fixtures. It does not claim that the organiser's eventual file has this schema. When the file arrives, inspect its data dictionary, licence, units, cohort definitions and provenance, then implement and test an explicit versioned mapping. Do not guess columns or silently discard fields.

## Canonical CSV fields

Required columns:

- `evidence_id`, `metric_code`, `metric_label`, `definition`
- `metric_kind`, `geography_level`, `geography_name`
- `source_publisher`, `verification_status`
- At least one source-reference column: `source_url` or `source_page_or_table`

Optional columns are defined by `services/outcome_import.py`: trade/job role, provider ID, state, district, value, numerator, denominator, sample size, cohort and observation periods, currency, unit, statistic type, follow-up period, source publication date, methodology and last verification date.

Headers are exact lower snake_case. Duplicate, unknown, blank and missing required headers are rejected. Extra/missing row cells are rejected. UTF-8 (with an optional BOM) is required. The parser has a 10 MiB file limit and a 50,000 nonblank-row limit.

The upload caller supplies dataset ID, dataset version and source filename as metadata. The report records a SHA-256 hash and timezone-aware UTC import timestamp for reproducibility.

## Validation and safety

- Blank numeric/date/context fields remain `None`; blank is never converted to zero.
- Metric kind, geography level and verification status are allow-listed.
- Provider-level evidence requires a provider ID. A provider ID on a state/district/national aggregate is rejected rather than used to imply provider-level evidence.
- Rate numerator and denominator must be supplied together and satisfy `0 <= numerator <= denominator` with a positive denominator.
- If a rate and counts are both supplied, the percentage must reconcile within 0.51 percentage points (the allowance is for source percentages rounded to a whole percentage point).
- If a rate is absent but both valid counts are supplied, the parser derives the percentage and emits an explicit warning. It never derives from incomplete counts.
- Numeric earnings require currency, unit and mean/median/band statistic type.
- Source publisher and a URL or page/table reference are required. URLs must be HTTP(S) and cannot embed credentials.
- An uploaded file **cannot set verification_status=verified**. Imports may be `needs_review`, `stale` or `synthetic_demo`. A separate curator/review workflow must establish verification.
- Cohort, observation, sample-size and follow-up gaps produce warnings and remain unknown.
- The parser creates an immutable preview report only. It performs no database writes, API calls or automatic commits.

The report exposes row-level errors and warnings, accepted/rejected row counts, derived-rate identifiers, dataset identity, filename, SHA-256 and import timestamp. `ready_to_import` is true only when the file is nonempty and **every** nonblank row passes. `require_importable_records()` raises unless the entire file is ready, preventing partial staging when one row fails.

## Why the initial parser uses the Python CSV standard library

This first ingestion boundary is row-oriented and strict: it needs exact headers, per-row provenance, precise blank-value handling and deterministic rejection semantics. The standard library CSV parser provides those controls without introducing a dataframe dependency. Pandas remains appropriate for later analysis/comparison work if measured dataset size and operations justify it; it is not required for this validation boundary.

## What this does not do

- It does not import the missing official SIH dataset or invent outcome values.
- It does not write accepted records to SQLite/PostgreSQL.
- It does not certify source authenticity or promote evidence to verified.
- It does not aggregate unlike cohorts, geographies, providers or outcome definitions.
- It does not convert placement, employment, trade-related employment, apprenticeship and self-employment into one metric.

The bilingual Streamlit review preview is implemented in `app/outcome_import_flow.py` and is rendered below the pathway and qualification sections. It rejects non-CSV filenames/MIME types and oversized payloads before parsing, requires dataset ID/version, displays the SHA-256 and UTC timestamp, and renders every finding. A failed or partial file never receives a row table. A fully valid preview labels `synthetic_demo`, `needs_review` and `stale` rows explicitly; it does not promote them to verified evidence. The screen has no authenticated steward role and performs no persistence or external calls. Marathi copy remains a draft pending fluent human review.

The read-only outcome filters and comparison view were implemented in [PR #51](https://github.com/emtharva1047/PathSaathi-AI/pull/51), merged to main on 26 November 2026. The bilingual explorer preserves exact geography, cohort, observation, follow-up and provenance fields; provider queries remain provider-geography-only, and numeric values are shown only when the API's complete verified-value contract permits them. Comparisons disclose scope differences and never pool or average observations.

Next Phase 4 increment: add a bilingual course catalogue search over the existing read-only `GET /api/v1/courses` endpoint (issue [#52](https://github.com/emtharva1047/PathSaathi-AI/issues/52)). Keep qualification provenance and verification status visible; do not infer provider availability, fees, seats, admissions or outcomes. Do not add persistence or a write action without an authenticated data-steward boundary and source-reviewed import contract.
