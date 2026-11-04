"""Integration tests for the read-only FastAPI catalogue and evidence routes."""

from __future__ import annotations

from datetime import date
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from backend.dependencies import get_db_session
from backend.main import app
from core.domain import CourseRecord, OutcomeEvidenceRecord
from database.repositories import SqlAlchemyCourseRepository, SqlAlchemyOutcomeEvidenceRepository
from database.session import create_database_engine, create_schema, create_session_factory


@pytest.fixture
def api_client() -> Iterator[tuple[TestClient, sessionmaker[Session]]]:
    """Use an isolated in-memory database and explicitly prepare its schema."""
    engine = create_database_engine("sqlite+pysqlite:///:memory:")
    create_schema(engine)
    factory = create_session_factory(engine)

    def override_session() -> Iterator[Session]:
        with factory() as session:
            yield session

    app.dependency_overrides[get_db_session] = override_session
    try:
        with TestClient(app) as client:
            yield client, factory
    finally:
        app.dependency_overrides.pop(get_db_session, None)
        engine.dispose()


def make_course(
    course_id: str,
    *,
    trade: str = "Electrician",
    nsqf_level: int | None = 4,
) -> CourseRecord:
    return CourseRecord(
        course_id=course_id,
        title=f"Test course {course_id}",
        trade=trade,
        nsqf_level=nsqf_level,
        state="Maharashtra",
        district="Thane",
        provider_id="provider-01",
        job_roles=("Electrician",),
        entry_requirements=("Test-only requirement",),
        verification_status="synthetic_demo",
    )


def make_outcome(
    evidence_id: str,
    *,
    value: float | None = 62.0,
    verification_status: str = "synthetic_demo",
    geography_level: str = "state",
    provider_id: str | None = None,
) -> OutcomeEvidenceRecord:
    verified = verification_status == "verified"
    return OutcomeEvidenceRecord(
        evidence_id=evidence_id,
        metric_code="trade_related_employment_rate",
        metric_label="Trade-related employment",
        definition="Test-only share of respondents employed in the trained trade.",
        metric_kind="rate",
        value=value,
        geography_level=geography_level,
        geography_name=provider_id or "Maharashtra",
        trade_or_job_role="Electrician",
        provider_id=provider_id,
        state="Maharashtra",
        district="Thane" if geography_level == "district" else None,
        numerator=62 if value is not None else None,
        denominator=100 if value is not None else None,
        sample_size=100 if value is not None else None,
        cohort_period="test cohort",
        observation_period="test observation period",
        source_publisher="Test fixture publisher" if verified else None,
        source_url="https://example.org/test-evidence" if verified else None,
        last_verified_at=date(2026, 11, 4) if verified else None,
        verification_status=verification_status,  # type: ignore[arg-type]
    )


def seed_records(
    factory: sessionmaker[Session],
    *,
    courses: tuple[CourseRecord, ...] = (),
    outcomes: tuple[OutcomeEvidenceRecord, ...] = (),
) -> None:
    with factory() as session:
        course_repository = SqlAlchemyCourseRepository(session)
        outcome_repository = SqlAlchemyOutcomeEvidenceRepository(session)
        for record in courses:
            course_repository.add_course(record)
        for record in outcomes:
            outcome_repository.add_outcome(record)
        session.commit()


def test_empty_catalogue_and_outcomes_return_empty_lists(api_client) -> None:
    client, _ = api_client

    assert client.get("/api/v1/courses").status_code == 200
    assert client.get("/api/v1/courses").json() == []
    assert client.get("/api/v1/outcomes").status_code == 200
    assert client.get("/api/v1/outcomes").json() == []


def test_course_filters_are_exact_and_keep_unknown_nsqf_levels_unknown(api_client) -> None:
    client, factory = api_client
    seed_records(
        factory,
        courses=(
            make_course("electrician-4"),
            make_course("electrician-unknown", nsqf_level=None),
            make_course("fitter-4", trade="Fitter"),
        ),
    )

    response = client.get(
        "/api/v1/courses",
        params={"state": "Maharashtra", "trade": "electrician", "min_nsqf_level": 3},
    )

    assert response.status_code == 200
    records = response.json()
    assert [record["course_id"] for record in records] == ["electrician-4"]
    assert records[0]["verification_status"] == "synthetic_demo"
    assert records[0]["source_verified"] is False


def test_course_detail_returns_record_and_unknown_id_is_404(api_client) -> None:
    client, factory = api_client
    seed_records(factory, courses=(make_course("course-01"),))

    response = client.get("/api/v1/courses/course-01")

    assert response.status_code == 200
    assert response.json()["course_id"] == "course-01"
    assert client.get("/api/v1/courses/missing").status_code == 404


def test_invalid_nsqf_range_returns_422(api_client) -> None:
    client, _ = api_client

    response = client.get(
        "/api/v1/courses",
        params={"min_nsqf_level": 6, "max_nsqf_level": 3},
    )

    assert response.status_code == 422


def test_unverified_outcome_values_are_withheld_and_unknowns_stay_null(api_client) -> None:
    client, factory = api_client
    seed_records(
        factory,
        outcomes=(
            make_outcome("verified", value=62.0, verification_status="verified"),
            make_outcome("synthetic", value=71.0),
            make_outcome("unknown", value=None),
        ),
    )

    response = client.get("/api/v1/outcomes")

    assert response.status_code == 200
    records = {record["evidence_id"]: record for record in response.json()}
    assert records["verified"]["value"] == 62.0
    assert records["verified"]["value_status"] == "verified"
    assert records["verified"]["displayable"] is True
    assert records["synthetic"]["value"] is None
    assert records["synthetic"]["value_status"] == "withheld"
    assert records["synthetic"]["value_withheld"] is True
    assert records["unknown"]["value"] is None
    assert records["unknown"]["value_status"] == "unknown"
    assert records["unknown"]["value_withheld"] is False


def test_provider_filter_never_returns_state_aggregate_with_provider_tag(api_client) -> None:
    client, factory = api_client
    seed_records(
        factory,
        outcomes=(
            make_outcome(
                "provider-record",
                geography_level="provider",
                provider_id="provider-01",
            ),
            make_outcome(
                "state-record-with-provider-tag",
                geography_level="state",
                provider_id="provider-01",
            ),
        ),
    )

    response = client.get("/api/v1/outcomes", params={"provider_id": "provider-01"})

    assert response.status_code == 200
    records = response.json()
    assert [record["evidence_id"] for record in records] == ["provider-record"]
    assert records[0]["geography_level"] == "provider"


def test_outcome_detail_returns_provenance_and_missing_id_is_404(api_client) -> None:
    client, factory = api_client
    seed_records(
        factory,
        outcomes=(make_outcome("evidence-01", value=55.0, verification_status="verified"),),
    )

    response = client.get("/api/v1/outcomes/evidence-01")

    assert response.status_code == 200
    assert response.json()["source_publisher"] == "Test fixture publisher"
    assert response.json()["source_url"] == "https://example.org/test-evidence"
    assert client.get("/api/v1/outcomes/missing").status_code == 404


def test_health_endpoint_does_not_require_database_session(api_client) -> None:
    client, _ = api_client

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "pathsaathi-api"}
