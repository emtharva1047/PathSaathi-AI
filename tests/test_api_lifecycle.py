"""End-to-end smoke coverage for FastAPI's lazy SQLite dependency lifecycle."""

from __future__ import annotations

from fastapi.testclient import TestClient

from backend import dependencies
from backend.main import app
from core.domain import CourseRecord
from database.repositories import SqlAlchemyCourseRepository
from database.session import create_database_engine, create_schema, create_session_factory


def test_health_is_database_independent_and_lazy_database_dependency_is_reused_and_disposed(
    monkeypatch,
) -> None:
    """Exercise the real FastAPI dependency rather than replacing it with a test override."""
    dependencies._get_session_factory.cache_clear()
    dependencies._get_engine.cache_clear()

    engine = create_database_engine("sqlite+pysqlite:///:memory:")
    create_schema(engine)
    factory = create_session_factory(engine)
    expected = CourseRecord(
        course_id="smoke-course",
        title="Synthetic smoke-test course",
        trade="Electrician",
        state="Maharashtra",
        district="Thane",
        job_roles=("Electrician",),
        entry_requirements=("Synthetic test fixture only",),
        verification_status="synthetic_demo",
    )
    with factory() as session:
        SqlAlchemyCourseRepository(session).add_course(expected)
        session.commit()

    engine_factory_calls = 0

    def reuse_test_engine():
        nonlocal engine_factory_calls
        engine_factory_calls += 1
        return engine

    monkeypatch.setattr(dependencies, "create_database_engine", reuse_test_engine)

    try:
        with TestClient(app) as client:
            # App startup and the process-health route must not open a database.
            assert dependencies._get_engine.cache_info().currsize == 0
            health = client.get("/health")
            assert health.status_code == 200
            assert health.json() == {"status": "ok", "service": "pathsaathi-api"}
            assert engine_factory_calls == 0

            # The first catalogue request creates the lazy engine/session factory.
            detail = client.get("/api/v1/courses/smoke-course")
            assert detail.status_code == 200
            assert detail.json()["course_id"] == expected.course_id
            assert detail.json()["verification_status"] == "synthetic_demo"
            assert detail.json()["source_verified"] is False
            assert engine_factory_calls == 1
            assert dependencies._get_session_factory.cache_info().currsize == 1

            # Later requests reuse the engine while obtaining their own short-lived session.
            listing = client.get("/api/v1/courses", params={"state": "Maharashtra"})
            assert listing.status_code == 200
            assert [record["course_id"] for record in listing.json()] == [expected.course_id]
            assert engine_factory_calls == 1

        # Application shutdown must release the cached factory and engine.
        assert dependencies._get_session_factory.cache_info().currsize == 0
        assert dependencies._get_engine.cache_info().currsize == 0
    finally:
        dependencies.dispose_database()
        engine.dispose()


def test_database_dependency_creates_and_closes_a_distinct_session_per_request(monkeypatch) -> None:
    """Each dependency invocation owns and closes its own short-lived session."""
    engine = create_database_engine("sqlite+pysqlite:///:memory:")

    from sqlalchemy.orm import Session, sessionmaker

    class TrackingSession(Session):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.close_calls = 0

        def close(self) -> None:
            self.close_calls += 1
            super().close()

    factory = sessionmaker(bind=engine, class_=TrackingSession)
    monkeypatch.setattr(dependencies, "_get_session_factory", lambda: factory)

    first_request = dependencies.get_db_session()
    second_request = dependencies.get_db_session()
    first_session = next(first_request)
    second_session = next(second_request)

    try:
        assert first_session is not second_session
        assert first_session.close_calls == 0
        assert second_session.close_calls == 0
    finally:
        first_request.close()
        second_request.close()
        engine.dispose()

    assert first_session.close_calls == 1
    assert second_session.close_calls == 1
