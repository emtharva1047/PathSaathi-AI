# Read-only catalogue API

The FastAPI service exposes a small read-only interface over the existing SQLAlchemy course and outcome repositories.

## Local setup

Prepare the local SQLite schema explicitly before the first catalogue request:

```bash
python -c "from database.session import create_database_engine, create_schema; engine = create_database_engine(); create_schema(engine); engine.dispose()"
uvicorn backend.main:app --reload
```

The API does not create tables during import or application startup. The health route is independent of the database:

- `GET /health`

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/courses` | List courses; supports state, district, trade, provider_id and NSQF-level filters |
| GET | `/api/v1/courses/{course_id}` | Fetch one course |
| GET | `/api/v1/outcomes` | List outcome evidence; supports metric, trade/job role, provider, state, district and verification-status filters |
| GET | `/api/v1/outcomes/{evidence_id}` | Fetch one evidence record |

Both list endpoints accept `limit` (default 50, maximum 100) and `offset` (default 0). Results use stable identifier ordering (`course_id` or `evidence_id`) so adjacent pages do not depend on database row order. The API returns a plain list; clients can request the next page by adding the returned page length to `offset`. A total-count field is intentionally omitted until a concrete UI needs it.

All filters are exact matches. A provider filter is restricted to records whose `geography_level` is `provider`; a state or trade aggregate is never promoted to provider evidence.

## Outcome value display contract

Every outcome response includes its metric definition, geography, cohort/observation periods, sample and numerator/denominator fields where available, earnings units/statistic/follow-up fields, verification status and source provenance.

The API exposes a numeric `value` only when the record is marked `verified` and has complete source provenance (publisher, HTTP(S) source URL and verification date). Numerator, denominator and sample-size counts are also withheld unless that verification status and provenance are complete. Otherwise:

- `value` is `null`;
- `value_status` is `withheld` when an unverified numeric value exists, or `unknown` when the value is absent;
- `value_withheld` explains that an unverified outcome value was intentionally not returned;
- `numeric_metadata_withheld` explains that numerator, denominator or sample-size counts were withheld;
- `source_verified` reports whether the verification status and required source fields are present (it is not an independent audit claim).

A `verified` label is not a claim that the source has been independently audited by PathSaathi; it records the current data-review status and must be supported by the supplied provenance. Synthetic fixtures are used only in tests and are never inserted as official outcomes.

## Database lifecycle

The engine and session factory are created lazily on first database-backed request, reused across requests and disposed during application shutdown. Each request receives a short-lived SQLAlchemy session. The API routes are read-only and do not commit writes.

Schema creation remains an explicit local-development operation. Production migrations, managed PostgreSQL and deployment are Phase 8 work. The current list endpoints are intended for the MVP catalogue; pagination and production authorisation must be completed before importing large datasets or exposing non-public records.
