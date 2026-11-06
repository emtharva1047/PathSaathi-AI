# Catalogue and Outcome Repository Contracts

## Purpose

Course catalogue and outcome-evidence services depend on Python protocols, not a specific
storage engine. This lets Phase 3 assessment and Phase 4 CSV ingestion use the same
contracts with deterministic in-memory fixtures or local SQLAlchemy persistence.

## Domain records

- CourseRecord stores a qualification/course, trade, optional NSQF level, broad
  geography, provider identifier, entry requirements, job roles and source status.
- OutcomeEvidenceRecord stores one metric observation with its definition, geography,
  trade/provider scope, cohort, observation period, denominator/sample size, earnings
  unit/statistic metadata and provenance.
- Unknown values remain None; an absent NSQF level is not treated as a level zero.
- A numeric outcome is displayable as verified only when its status is verified,
  publisher and HTTP(S) source URL are present, and a verification date is recorded.
- Synthetic test/demo records use verification_status=synthetic_demo and can never
  satisfy the verified-displayable predicate.

## Repository contracts

CourseRepository exposes list_courses(CourseQuery | None) and get_course(course_id).

OutcomeEvidenceRepository exposes list_outcomes(OutcomeQuery | None) and
get_outcome(evidence_id).

Each query applies all supplied exact-match filters. Text matching is case-insensitive,
but the adapter does not broaden a provider query into a state or trade average. A provider
filter also requires provider-level geography; a state aggregate remains excluded even if
it carries a provider identifier. NSQF range filters exclude records whose level is unknown.
Queries support a non-negative offset and an optional limit from 1 through 100. SQLAlchemy
applies these bounds in the database; in-memory adapters sort by stable identifier before
slicing so paginated results have deterministic ordering across adapters.

## In-memory adapters

InMemoryCourseRepository and InMemoryOutcomeEvidenceRepository accept iterables of
immutable domain records. They reject duplicate identifiers, sort paginated query results by stable identifier,
and return tuples. They are intended for tests and explicitly labelled synthetic demos.

## SQLAlchemy adapters

- CourseModel and OutcomeEvidenceModel map the domain fields to relational tables.
- JSON columns store course job-role and entry-requirement lists in both SQLite and
  PostgreSQL.
- SqlAlchemyCourseRepository and SqlAlchemyOutcomeEvidenceRepository implement the
  same exact-match read contracts and provide explicit add methods.
- Repository methods flush staged inserts but do not commit. The service/unit-of-work
  caller owns transaction commit or rollback.
- Unknown values remain SQL NULL; synthetic status is preserved on round trip.
- Database constraints reject invalid status/metric/geography/statistic values, invalid
  rate ranges, invalid count pairs and impossible NSQF levels.

## Outcome validation rules

- Rate values are percentages from 0 through 100.
- Numerator and denominator must be supplied together; denominator must be positive and
  numerator cannot exceed it.
- Earnings with a numeric value require currency, unit and explicit mean/median/band type.
- Verified records require a publisher, HTTP(S) source URL and last-verification date.
- Missing values remain unknown; no repository method calculates a replacement estimate.

## CSV ingestion boundary for Phase 4

The Phase 4 importer should parse and validate source rows into these same domain records,
then pass them to an implementation of the repository protocol. It must preserve the
original source file hash, import timestamp, exact metric definitions and cohort/geography
scope. The official SIH dummy dataset remains an external dependency; no synthetic fixture
in this repository is an official outcome.

## Database configuration

- Default local URL: sqlite:///./data/pathsaathi.db.
- Override with PATHSAATHI_DATABASE_URL.
- Install the optional PostgreSQL driver with pip install -e ".[postgres]".
- create_database_engine() constructs an engine but does not connect until used.
- create_schema(engine) explicitly creates development/test tables; it is not invoked
  automatically by importing the application.
- Production PostgreSQL provisioning, migrations and deployment are Phase 8 release work.