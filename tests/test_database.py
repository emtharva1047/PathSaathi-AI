"""SQLite persistence tests for the SQLAlchemy repository adapters."""
import pytest
from sqlalchemy.exc import IntegrityError

from core.config import DEFAULT_DATABASE_URL, Settings
from core.domain import CourseRecord, OutcomeEvidenceRecord
from database.models import CourseModel, OutcomeEvidenceModel
from database.repositories import (
    SqlAlchemyCourseRepository,
    SqlAlchemyOutcomeEvidenceRepository,
)
from database.session import create_database_engine, create_schema, create_session_factory
from services.repositories import CourseQuery, OutcomeQuery


@pytest.fixture
def db_session():
    engine = create_database_engine("sqlite+pysqlite:///:memory:")
    create_schema(engine)
    factory = create_session_factory(engine)
    with factory() as session:
        yield session
    engine.dispose()


def make_course(
    course_id: str,
    *,
    trade: str = "Electrician",
    nsqf_level: int | None = 4,
) -> CourseRecord:
    return CourseRecord(
        course_id=course_id,
        title=f"Course {course_id}",
        trade=trade,
        state="Maharashtra",
        district="Thane",
        provider_id="provider-01",
        nsqf_level=nsqf_level,
        job_roles=("Electrician", "Wireman"),
        entry_requirements=("Class 10",),
        verification_status="synthetic_demo",
    )


def make_outcome(
    evidence_id: str,
    *,
    value: float | None = 62.0,
    provider_id: str | None = None,
) -> OutcomeEvidenceRecord:
    return OutcomeEvidenceRecord(
        evidence_id=evidence_id,
        metric_code="trade_related_employment_rate",
        metric_label="Trade-related employment",
        definition="Synthetic test-only share of respondents employed in the trained trade.",
        metric_kind="rate",
        value=value,
        geography_level="provider" if provider_id else "state",
        geography_name=provider_id or "Maharashtra",
        trade_or_job_role="Electrician",
        provider_id=provider_id,
        state="Maharashtra",
        numerator=62 if value is not None else None,
        denominator=100 if value is not None else None,
        sample_size=100 if value is not None else None,
        verification_status="synthetic_demo",
    )


def test_default_database_configuration_is_local_sqlite() -> None:
    assert DEFAULT_DATABASE_URL.startswith("sqlite:///")
    assert Settings().database_url.startswith("sqlite:///")


def test_postgresql_url_can_be_configured_without_opening_a_connection() -> None:
    configured = Settings(database_url="postgresql+psycopg://user:pass@localhost/pathsaathi")
    assert configured.database_url.startswith("postgresql+psycopg://")


def test_course_repository_round_trips_domain_record(db_session) -> None:
    repository = SqlAlchemyCourseRepository(db_session)
    course = make_course("course-01")

    repository.add_course(course)
    db_session.commit()

    assert repository.get_course("course-01") == course
    assert repository.list_courses() == (course,)


def test_course_repository_applies_exact_filters_and_excludes_unknown_level(db_session) -> None:
    repository = SqlAlchemyCourseRepository(db_session)
    repository.add_course(make_course("level-4"))
    repository.add_course(make_course("unknown-level", nsqf_level=None))
    repository.add_course(make_course("fitter", trade="Fitter"))
    db_session.commit()

    results = repository.list_courses(
        CourseQuery(state="maharashtra", trade="ELECTRICIAN", min_nsqf_level=3)
    )

    assert [course.course_id for course in results] == ["level-4"]


def test_outcome_repository_preserves_unknown_values_and_synthetic_status(db_session) -> None:
    repository = SqlAlchemyOutcomeEvidenceRepository(db_session)
    unknown = make_outcome("unknown", value=None)
    repository.add_outcome(unknown)
    db_session.commit()

    restored = repository.get_outcome("unknown")

    assert restored == unknown
    assert restored is not None
    assert restored.value is None
    assert restored.is_verified_displayable is False


def test_outcome_repository_does_not_broaden_provider_scope(db_session) -> None:
    repository = SqlAlchemyOutcomeEvidenceRepository(db_session)
    state_record = make_outcome("state")
    provider_record = make_outcome("provider", provider_id="provider-01")
    repository.add_outcome(state_record)
    repository.add_outcome(provider_record)
    db_session.commit()

    results = repository.list_outcomes(OutcomeQuery(provider_id="provider-01"))

    assert [record.evidence_id for record in results] == ["provider"]
    assert results[0].geography_level == "provider"


def test_course_primary_key_rejects_duplicate_records(db_session) -> None:
    repository = SqlAlchemyCourseRepository(db_session)
    repository.add_course(make_course("duplicate"))
    db_session.commit()

    with pytest.raises(IntegrityError):
        repository.add_course(make_course("duplicate"))


def test_database_check_constraint_rejects_invalid_verification_status(db_session) -> None:
    db_session.add(
        CourseModel(
            course_id="bad-status",
            title="Bad status",
            trade="Electrician",
            job_roles=[],
            entry_requirements=[],
            verification_status="official",
        )
    )

    with pytest.raises(IntegrityError):
        db_session.flush()


def test_database_check_constraint_rejects_invalid_rate_value(db_session) -> None:
    db_session.add(
        OutcomeEvidenceModel(
            evidence_id="invalid-rate",
            metric_code="placement_rate",
            metric_label="Placement rate",
            definition="Invalid test-only percentage.",
            metric_kind="rate",
            value=101.0,
            geography_level="state",
            geography_name="Maharashtra",
            statistic_type="unknown",
            verification_status="synthetic_demo",
        )
    )

    with pytest.raises(IntegrityError):
        db_session.flush()