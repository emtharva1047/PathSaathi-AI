"""Cross-layer acceptance tests for the Phase 4 evidence journey."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import nullcontext
from decimal import Decimal
from urllib.parse import urlsplit

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from app.course_explorer import COURSE_EXPLORER_COPY, render_course_explorer
from app.outcome_explorer import OUTCOME_EXPLORER_COPY, render_outcome_explorer
from app.outcome_import_flow import OUTCOME_IMPORT_COPY, render_outcome_import
from backend.dependencies import get_db_session
from backend.main import app
from core.domain import CourseRecord, OutcomeEvidenceRecord
from database.repositories import (
    SqlAlchemyCourseRepository,
    SqlAlchemyOutcomeEvidenceRepository,
)
from database.session import create_database_engine, create_schema, create_session_factory


@pytest.fixture
def phase4_api_client() -> Iterator[tuple[TestClient, sessionmaker[Session]]]:
    """Run the real API routes against an isolated in-memory SQLite database."""
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


class ClientResponse:
    """Adapt a FastAPI TestClient response to the urllib response interface."""

    def __init__(self, response) -> None:
        self.response = response

    def __enter__(self) -> ClientResponse:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.response.content


class RecordingStreamlit:
    """Minimal Streamlit surface that records rendered text without a browser."""

    def __init__(self) -> None:
        self.session_state: dict[str, object] = {}
        self.events: list[tuple[str, tuple, dict]] = []

    def form(self, *_args, **_kwargs):
        return nullcontext()

    def form_submit_button(self, *_args, **_kwargs) -> bool:
        return False

    def text_input(self, _label: str, *, value: str = "", **_kwargs) -> str:
        return value

    def selectbox(self, _label: str, options, index: int = 0, **_kwargs):
        return options[index]

    def multiselect(self, _label: str, options, default=None, **_kwargs):
        return list(default or [])

    def expander(self, *_args, **_kwargs):
        return nullcontext()

    def button(self, *_args, **_kwargs) -> bool:
        return False

    def file_uploader(self, *_args, **_kwargs):
        return None

    def rendered_text(self) -> str:
        return " ".join(
            str(value)
            for _name, args, _kwargs in self.events
            for value in args
        )

    def __getattr__(self, name: str):
        def record(*args, **kwargs) -> None:
            self.events.append((name, args, kwargs))

        return record


def _seed_synthetic_phase4_records(factory: sessionmaker[Session]) -> None:
    """Seed clearly synthetic catalogue and outcome records for the integration test."""
    course = CourseRecord(
        course_id="demo-electrician-01",
        title="Synthetic Electrician Qualification",
        trade="Electrician",
        qualification_code="DEMO-ELEC-01",
        awarding_body="PathSaathi synthetic test fixtures",
        nsqf_level=Decimal("4.0"),
        state="Maharashtra",
        district="Thane",
        provider_id="demo-provider-01",
        job_roles=("Electrician",),
        entry_requirements=("Synthetic test fixture only",),
        source_publisher="PathSaathi synthetic test fixtures",
        verification_status="synthetic_demo",
    )
    outcome = OutcomeEvidenceRecord(
        evidence_id="demo-electrician-outcome-01",
        metric_code="trade_related_employment_rate",
        metric_label="Trade-related employment",
        definition="Synthetic fixture only; not a labour-market estimate.",
        metric_kind="rate",
        value=62.0,
        geography_level="state",
        geography_name="Maharashtra",
        trade_or_job_role="Electrician",
        state="Maharashtra",
        numerator=62,
        denominator=100,
        sample_size=100,
        cohort_period="synthetic cohort",
        observation_period="synthetic observation period",
        follow_up_period="12 months (synthetic fixture)",
        source_publisher="PathSaathi synthetic test fixtures",
        methodology="Synthetic fixture only; not real outcomes.",
        verification_status="synthetic_demo",
    )

    with factory() as session:
        SqlAlchemyCourseRepository(session).add_course(course)
        SqlAlchemyOutcomeEvidenceRepository(session).add_outcome(outcome)
        session.commit()


def _client_urlopen(client: TestClient, requested_paths: list[str]):
    """Route the Streamlit HTTP client through the real in-process FastAPI app."""

    def open_request(request, timeout: float):
        parsed = urlsplit(request.full_url)
        requested_paths.append(parsed.path)
        response = client.get(request.full_url)
        return ClientResponse(response)

    return open_request


@pytest.mark.parametrize("locale", ["English", "मराठी"])
def test_phase4_explorers_read_sqlite_api_and_withhold_synthetic_outcomes(
    phase4_api_client,
    monkeypatch: pytest.MonkeyPatch,
    locale: str,
) -> None:
    """Exercise course, CSV-preview and outcome screens across the real API boundary."""
    client, factory = phase4_api_client
    _seed_synthetic_phase4_records(factory)

    requested_paths: list[str] = []
    api_urlopen = _client_urlopen(client, requested_paths)
    monkeypatch.setattr("app.course_explorer.urlopen", api_urlopen)
    monkeypatch.setattr("app.outcome_explorer.urlopen", api_urlopen)

    st = RecordingStreamlit()
    render_course_explorer(st, locale, api_base_url="http://testserver")
    render_outcome_import(st, locale)
    render_outcome_explorer(st, locale, api_base_url="http://testserver")

    rendered = st.rendered_text()
    assert COURSE_EXPLORER_COPY[locale]["heading"] in rendered
    assert "Synthetic Electrician Qualification" in rendered
    assert COURSE_EXPLORER_COPY[locale]["synthetic_demo"] in rendered
    assert OUTCOME_IMPORT_COPY[locale]["heading"] in rendered
    assert OUTCOME_IMPORT_COPY[locale]["waiting"] in rendered
    assert OUTCOME_EXPLORER_COPY[locale]["heading"] in rendered
    assert OUTCOME_EXPLORER_COPY[locale]["status_synthetic_demo"] in rendered
    assert OUTCOME_EXPLORER_COPY[locale]["withheld"] in rendered
    assert OUTCOME_EXPLORER_COPY[locale]["numeric_metadata_withheld"] in rendered

    # The API withholds the synthetic value and counts; the UI must not reintroduce them.
    assert "62" not in rendered
    assert "62 / 100" not in rendered
    assert requested_paths == ["/api/v1/courses", "/api/v1/outcomes"]
