"""Tests for the bilingual, read-only course catalogue explorer."""

from __future__ import annotations

import json
from contextlib import nullcontext
from urllib.error import URLError
from urllib.parse import parse_qs, urlsplit

import pytest

from app.course_explorer import (
    COURSE_EXPLORER_COPY,
    PAGE_SIZE,
    CourseApiError,
    build_course_params,
    fetch_course_page,
    render_course_explorer,
    safe_source_url,
)


class FakeResponse:
    def __init__(self, payload: object) -> None:
        self.payload = payload

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


class FakeStreamlit:
    def __init__(self, *, state: dict | None = None, submit: bool = False) -> None:
        self.session_state = state if state is not None else {}
        self.submit = submit
        self.events: list[tuple[str, tuple, dict]] = []

    def form(self, *_args, **_kwargs):
        return nullcontext()

    def form_submit_button(self, *_args, **_kwargs) -> bool:
        return self.submit

    def text_input(self, _label: str, *, value: str = "", **_kwargs) -> str:
        return value

    def expander(self, *_args, **_kwargs):
        return nullcontext()

    def button(self, *_args, **_kwargs) -> bool:
        return False

    def __getattr__(self, name: str):
        def record(*args, **kwargs):
            self.events.append((name, args, kwargs))
        return record


def rendered_text(st: FakeStreamlit) -> str:
    return "\n".join(str(value) for _, args, _ in st.events for value in args)


def make_course(**overrides) -> dict:
    record = {
        "course_id": "nqr-test-01",
        "title": "Assistant Baking Technician",
        "trade": "Food Processing",
        "qualification_code": "QG-TEST-01",
        "awarding_body": "Food Industry Capacity and Skill Initiative",
        "nsqf_level": 3.0,
        "state": "Maharashtra",
        "district": "Thane",
        "provider_id": "provider-01",
        "job_roles": ["Assistant Baking Technician"],
        "entry_requirements": ["Grade 10 or an approved alternative route"],
        "source_publisher": "National Qualifications Register",
        "source_url": "https://example.org/qualification",
        "source_publication_date": "2025-01-01",
        "last_verified_at": "2026-11-20",
        "verification_status": "verified",
        "source_verified": True,
    }
    record.update(overrides)
    return record


def test_course_params_use_exact_filters_and_preserve_half_step_levels() -> None:
    params = build_course_params(
        {
            "state": " Maharashtra ",
            "district": "Thane",
            "trade": "Electrician",
            "provider_id": "provider-01",
            "min_nsqf_level": "2.5",
            "max_nsqf_level": "4",
        },
        limit=50,
        offset=100,
    )

    assert params == {
        "limit": "50",
        "offset": "100",
        "state": "Maharashtra",
        "district": "Thane",
        "trade": "Electrician",
        "provider_id": "provider-01",
        "min_nsqf_level": "2.5",
        "max_nsqf_level": "4.0",
    }


@pytest.mark.parametrize("value", ["0.5", "2.3", "10.5", "abc", "NaN", "Infinity"])
def test_invalid_nsqf_filter_values_are_rejected(value: str) -> None:
    with pytest.raises(CourseApiError) as error:
        build_course_params({"min_nsqf_level": value})
    assert error.value.kind == "validation"


def test_minimum_nsqf_cannot_exceed_maximum() -> None:
    with pytest.raises(CourseApiError) as error:
        build_course_params({"min_nsqf_level": "4.5", "max_nsqf_level": "4"})
    assert error.value.kind == "validation"


@pytest.mark.parametrize("limit,offset", [(0, 0), (101, 0), (50, -1)])
def test_course_pagination_bounds_are_rejected(limit: int, offset: int) -> None:
    with pytest.raises(CourseApiError):
        build_course_params({}, limit=limit, offset=offset)


def test_fetch_course_page_uses_bounded_exact_api_query(monkeypatch) -> None:
    requested: dict[str, object] = {}

    def fake_urlopen(request, timeout):
        requested["url"] = request.full_url
        requested["timeout"] = timeout
        requested["method"] = request.get_method()
        return FakeResponse([make_course()])

    monkeypatch.setattr("app.course_explorer.urlopen", fake_urlopen)
    records = fetch_course_page(
        {
            "state": "Maharashtra",
            "district": "Thane",
            "trade": "Food Processing",
            "provider_id": "provider-01",
            "min_nsqf_level": "2.5",
            "max_nsqf_level": "3.0",
        },
        offset=50,
        api_base_url="https://api.example.org/path",
    )

    query = parse_qs(urlsplit(str(requested["url"])).query)
    assert records[0]["course_id"] == "nqr-test-01"
    assert urlsplit(str(requested["url"])).path == "/path/api/v1/courses"
    assert requested["method"] == "GET"
    assert requested["timeout"] == 3.0
    assert query == {
        "limit": ["50"],
        "offset": ["50"],
        "state": ["Maharashtra"],
        "district": ["Thane"],
        "trade": ["Food Processing"],
        "provider_id": ["provider-01"],
        "min_nsqf_level": ["2.5"],
        "max_nsqf_level": ["3.0"],
    }


def test_invalid_filters_fail_before_network_request(monkeypatch) -> None:
    def unexpected(*_args, **_kwargs):
        raise AssertionError("Invalid filters must not trigger a network request.")

    monkeypatch.setattr("app.course_explorer.urlopen", unexpected)
    with pytest.raises(CourseApiError) as error:
        fetch_course_page({"min_nsqf_level": "2.3"})
    assert error.value.kind == "validation"


def test_offline_api_raises_without_substituting_local_courses(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.course_explorer.urlopen",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(URLError("offline")),
    )
    with pytest.raises(CourseApiError) as error:
        fetch_course_page({}, api_base_url="http://127.0.0.1:8000")
    assert error.value.kind == "offline"


def test_invalid_api_url_fails_before_network_request(monkeypatch) -> None:
    def unexpected(*_args, **_kwargs):
        raise AssertionError("Invalid URL must not trigger a network request.")

    monkeypatch.setattr("app.course_explorer.urlopen", unexpected)
    with pytest.raises(CourseApiError) as error:
        fetch_course_page({}, api_base_url="javascript:alert(1)")
    assert error.value.kind == "configuration"


@pytest.mark.parametrize(
    "value",
    [
        "https://example.org/source",
        "http://example.org/source",
    ],
)
def test_safe_source_url_accepts_http_and_https(value: str) -> None:
    assert safe_source_url(value) == value


@pytest.mark.parametrize(
    "value",
    [
        "javascript:alert(1)",
        "ftp://example.org/source",
        "https://user:secret@example.org/source",
        "not-a-url",
        None,
    ],
)
def test_safe_source_url_rejects_unsafe_or_missing_urls(value: str | None) -> None:
    assert safe_source_url(value) is None


@pytest.mark.parametrize("locale", ["English", "मराठी"])
def test_render_offline_state_is_localised_and_has_no_fallback_records(monkeypatch, locale: str) -> None:
    monkeypatch.setattr(
        "app.course_explorer.urlopen",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(URLError("offline")),
    )
    st = FakeStreamlit()
    render_course_explorer(st, locale, api_base_url="http://127.0.0.1:8000")

    text = rendered_text(st)
    assert COURSE_EXPLORER_COPY[locale]["heading"] in text
    assert COURSE_EXPLORER_COPY[locale]["offline"] in text
    assert "Assistant Baking Technician" not in text


def test_render_empty_state_does_not_claim_catalogue_is_exhaustive(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.course_explorer.urlopen",
        lambda *_args, **_kwargs: FakeResponse([]),
    )
    st = FakeStreamlit()
    render_course_explorer(st, "English")

    assert COURSE_EXPLORER_COPY["English"]["empty"] in rendered_text(st)


def test_render_verified_course_displays_required_fields_and_safe_source(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.course_explorer.urlopen",
        lambda *_args, **_kwargs: FakeResponse([make_course()]),
    )
    st = FakeStreamlit()
    render_course_explorer(st, "English")

    text = rendered_text(st)
    assert "Assistant Baking Technician" in text
    assert "Food Processing" in text
    assert "QG-TEST-01" in text
    assert "Food Industry Capacity and Skill Initiative" in text
    assert "3.0" in text
    assert "Assistant Baking Technician" in text
    assert "Grade 10 or an approved alternative route" in text
    assert "Maharashtra" in text
    assert "Thane" in text
    assert "provider-01" in text
    assert "National Qualifications Register" in text
    assert "2025-01-01" in text
    assert "2026-11-20" in text
    assert COURSE_EXPLORER_COPY["English"]["verified"] in text
    assert any(
        name == "link_button" and args[1] == "https://example.org/qualification"
        for name, args, _ in st.events
    )


def test_render_synthetic_course_is_labelled_and_source_link_is_not_opened(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.course_explorer.urlopen",
        lambda *_args, **_kwargs: FakeResponse(
            [
                make_course(
                    verification_status="synthetic_demo",
                    source_verified=False,
                    source_url="javascript:alert(1)",
                )
            ]
        ),
    )
    st = FakeStreamlit()
    render_course_explorer(st, "English")

    text = rendered_text(st)
    assert COURSE_EXPLORER_COPY["English"]["synthetic_demo"] in text
    assert "link_button" not in [name for name, _, _ in st.events]
    assert COURSE_EXPLORER_COPY["English"]["invalid_source"] in text


def test_render_incomplete_verified_metadata_is_not_presented_as_verified(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.course_explorer.urlopen",
        lambda *_args, **_kwargs: FakeResponse(
            [make_course(verification_status="verified", source_verified=False)]
        ),
    )
    st = FakeStreamlit()
    render_course_explorer(st, "English")

    assert COURSE_EXPLORER_COPY["English"]["verified_incomplete"] in rendered_text(st)


def test_invalid_nsqf_range_renders_error_without_calling_api(monkeypatch) -> None:
    def unexpected(*_args, **_kwargs):
        raise AssertionError("Invalid range must not trigger a network request.")

    monkeypatch.setattr("app.course_explorer.urlopen", unexpected)
    st = FakeStreamlit(
        state={
            "course_explorer_filters": {
                "min_nsqf_level": "4.0",
                "max_nsqf_level": "2.5",
            }
        },
        submit=True,
    )
    render_course_explorer(st, "English")

    assert COURSE_EXPLORER_COPY["English"]["invalid_filter"] in rendered_text(st)


def test_course_page_uses_fixed_bounded_page_size() -> None:
    assert PAGE_SIZE == 50
    assert build_course_params({})["limit"] == "50"
