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

### Verify the local application connection

Run the network-level smoke check from the repository root after installing the project and development dependencies:

```bash
python scripts/smoke_test.py
```

The script starts the real Streamlit and Uvicorn applications on distinct ephemeral loopback ports. It verifies the Streamlit `/_stcore/health` and root HTTP endpoints while the configured API is offline, then exercises the same `is_api_healthy()` function used by the Streamlit sidebar through the sequence:

1. Streamlit serves its health endpoint and HTML shell while FastAPI is offline.
2. The configured API is detected as online after FastAPI `/health` responds.
3. The API is stopped and the health client reports it offline again.
4. Streamlit continues serving its health endpoint and HTML shell after API shutdown.

This is a real-process startup and availability check, not a browser/WebSocket interaction or an accessibility-conformance test. It uses only the database-independent health route; it does not create a SQLite file or schema, and it does not require a hosted database.

For a manual UI check, start the API in one terminal:

```bash
uvicorn backend.main:app --reload
```

Then start Streamlit in a second terminal:

```bash
streamlit run app/streamlit_app.py
```

The sidebar should show the API as connected. Stop Uvicorn and rerun the Streamlit page; the sidebar should show the offline message while the informational shell remains usable. The smoke script validates the network health client, while the existing Streamlit rendering tests validate the bilingual status and navigation copy.

### API base URL configuration

The Streamlit health client reads `PATHSAATHI_API_URL` when no explicit base URL is supplied. The default is `http://127.0.0.1:8000`. For example, if FastAPI is listening on another local port:

```bash
export PATHSAATHI_API_URL="http://127.0.0.1:8001"
```

Use an absolute HTTP or HTTPS base URL without embedded credentials, a query string or a fragment. A path prefix is allowed. A blank or malformed value is treated as offline without making a network request; the informational UI remains available. The explicit URL argument used by tests and smoke checks takes precedence over the environment variable.

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

Schema creation remains an explicit local-development operation. Production migrations, managed PostgreSQL and deployment are Phase 8 work. Bounded pagination is implemented for the current list endpoints. Production authorisation and importer-scale validation remain prerequisites before importing large datasets or exposing non-public records.
