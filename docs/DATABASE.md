# Database Configuration and Local Development

## Local default

PathSaathi AI uses SQLAlchemy 2.x with SQLite for local development:

~~~text
sqlite:///./data/pathsaathi.db
~~~

The URL is read from PATHSAATHI_DATABASE_URL. If it is not set, the local SQLite URL
is used. The engine helper creates the parent directory for a file-backed SQLite URL,
but it does not connect to the database until a session/query is used.

## Explicit schema setup

Schema creation is intentionally explicit:

~~~python
from database.session import create_database_engine, create_schema

engine = create_database_engine()
create_schema(engine)
~~~

Importing backend.main, database.models or database.session does not create tables.
The helper is intended for local development and tests, not as a production migration
strategy.

## Sessions and transactions

create_session_factory(engine) creates SQLAlchemy sessions. Repository add methods
stage records and flush them, but do not commit. The service or unit-of-work boundary
owns commit/rollback. Use get_session(factory) as a FastAPI dependency generator when
wiring database-backed routes.

## PostgreSQL compatibility

Set PATHSAATHI_DATABASE_URL to a PostgreSQL SQLAlchemy URL and install the optional
driver:

~~~bash
pip install -e ".[postgres]"
export PATHSAATHI_DATABASE_URL="postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME"
~~~

Never commit a connection string containing credentials. PostgreSQL URL support is
configuration readiness only; managed production database provisioning, migrations
and deployment are reserved for Phase 8.

## Test isolation

Automated database tests use sqlite+pysqlite:///:memory: with an isolated SQLAlchemy
engine and session factory. They do not read or write a developer's local database file.

## Runtime settings validation

The core settings object validates environment-backed values before the application serves
requests. Invalid configuration raises a concise `ValueError`; URL parsing does not open a
database connection.

- `APP_NAME`, `APP_ENV` and `API_HOST` must be non-blank; the host cannot contain whitespace.
- `API_PORT` must be an integer in the TCP port range 1–65535.
- `DATABASE_ECHO` accepts explicit true/false tokens: `true/false`, `1/0`, `yes/no`
  or `on/off`. Unknown tokens are rejected rather than silently interpreted as false.
- `PATHSAATHI_DATABASE_URL` must parse as a SQLite or PostgreSQL SQLAlchemy URL.
  PostgreSQL URLs must include a host. This is syntax/configuration validation only;
  it does not test credentials, open a connection or provision a database.
