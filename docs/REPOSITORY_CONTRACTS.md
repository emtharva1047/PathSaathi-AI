# Catalogue and Outcome Repository Contracts

## Purpose

The course catalogue and outcome-evidence services depend on Python protocols, not a
database engine. This keeps the Phase 3 assessment and Phase 4 CSV importer independent
of storage technology. The current in-memory adapters are suitable for tests and
explicitly labelled demonstrations only.

## Domain records

- `CourseRecord` stores a qualification/course, trade, optional NSQF level, broad
  geography, provider identifier, entry requirements, job roles and source status.
- `OutcomeEvidenceRecord` stores one metric observation with its definition, geography,
  trade/provider scope, cohort, observation period, denominator/sample size, earnings
  unit/statistic metadata and provenance.
- Unknown values remain `None`; an absent NSQF level is not treated as a level zero.
- A numeric outcome is displayable as verified only when its status is `verified`,
  its publisher and HTTP(S) source URL are present, and a verification date is recorded.
- Synthetic test/demo records use `verification_status="synthetic_demo"` and can never
  satisfy the verified-displayable predicate.

## Repository contracts

`CourseRepository` exposes:

- `list_courses(CourseQuery | None)`
- `get_course(course_id)`

`OutcomeEvidenceRepository` exposes:

- `list_outcomes(OutcomeQuery | None)`
- `get_outcome(evidence_id)`

Each query applies all supplied exact-match filters. Text matching is case-insensitive,
but the adapter does not broaden a provider query into a state or trade average. NSQF
range filters exclude records whose level is unknown instead of guessing.

## In-memory adapters

`InMemoryCourseRepository` and `InMemoryOutcomeEvidenceRepository` accept iterables of
immutable domain records. They reject duplicate identifiers, preserve insertion order,
and return tuples. They do not write files, connect to a database or retain learner data.

## Outcome validation rules

- Rate values are percentages from 0 through 100.
- Numerator and denominator must be supplied together; denominator must be positive and
  numerator cannot exceed it.
- Earnings with a numeric value require a currency, unit and explicit mean/median/band
  statistic type.
- Verified records require a publisher, HTTP(S) source URL and last-verification date.
- Missing values remain unknown; no repository method calculates a replacement estimate.

## CSV ingestion boundary for Phase 4

The Phase 4 importer should parse and validate source rows into these same domain records,
then pass them to an implementation of the repository protocol. It must preserve the
original source file hash, import timestamp, exact metric definitions and cohort/geography
scope. The official SIH dummy dataset is still an external dependency; no synthetic fixture
in this repository is an official outcome.

## Future persistence boundary

After Phase 4 exit criteria are met, a PostgreSQL/SQLAlchemy implementation may satisfy the
same protocols. The domain records, query objects and contract tests should remain
storage-independent. No SQLAlchemy engine, SQLite connection, Alembic migration or hosted
database is part of this increment.
