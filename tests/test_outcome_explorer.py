"""Tests for the bilingual, provenance-first outcome explorer."""

from __future__ import annotations

import json
from contextlib import nullcontext
from urllib.error import URLError
from urllib.parse import parse_qs, urlsplit

import pytest

from app.outcome_explorer import (
    OUTCOME_EXPLORER_COPY,
    OutcomeApiError,
    build_outcome_params,
    comparison_assessment,
    fetch_outcome_page,
    is_numeric_value_displayable,
    render_outcome_explorer,
)


def make_record(**overrides):
    record = {
        "evidence_id": "evidence-1",
        "metric_code": "trade_related_employment_rate",
        "metric_label": "Trade-related employment",
        "definition": "Share of respondents employed in the trained trade.",
        "metric_kind": "rate",
        "value": 62.0,
        "value_status": "verified",
        "value_withheld": False,
        "numeric_metadata_withheld": False,
        "source_verified": True,
        "geography_level": "state",
        "geography_name": "Maharashtra",
        "trade_or_job_role": "Electrician",
        "provider_id": None,
        "state": "Maharashtra",
        "district": None,
        "numerator": 62,
        "denominator": 100,
        "sample_size": 100,
        "cohort_period": "2023",
        "observation_period": "2024",
        "currency": None,
        "unit": "%",
        "statistic_type": "unknown",
        "follow_up_period": "12 months",
        "source_publisher": "Test publisher",
        "source_url": "https://example.org/evidence",
        "source_publication_date": "2025-01-01",
        "source_page_or_table": "Table 2",
        "methodology": "Test-only fixture; not a real outcome.",
        "last_verified_at": "2025-02-01",
        "verification_status": "verified",
        "displayable": True,
    }
    record.update(overrides)
    return record


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class FakeStreamlit:
    def __init__(self, *, selected=()):
        self.session_state = {}
        self.selected = list(selected)
        self.events = []

    def form(self, _key):
        return nullcontext()

    def expander(self, label, expanded=False):
        self.events.append(("expander", label, expanded))
        return nullcontext()

    def selectbox(self, _label, options, index=0, **_kwargs):
        return options[index]

    def text_input(self, _label, value="", **_kwargs):
        return value

    def form_submit_button(self, _label):
        return False

    def button(self, _label, **_kwargs):
        return False

    def multiselect(self, _label, options, default=None, **_kwargs):
        return [item for item in self.selected if item in options] or list(default or [])

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.events.append((name, *args))
        return record


def test_build_outcome_params_carries_exact_filters_and_pagination() -> None:
    params = build_outcome_params(
        {
            "metric_code": " trade_related_employment_rate ",
            "geography_level": "state",
            "geography_name": " Maharashtra ",
            "trade": "Electrician",
            "provider_id": "should-not-leak",
            "cohort_period": "2023",
            "observation_period": "2024",
            "verification_status": "verified",
        },
        limit=25,
        offset=50,
    )

    assert params == {
        "limit": "25",
        "offset": "50",
        "metric_code": "trade_related_employment_rate",
        "geography_name": "Maharashtra",
        "trade": "Electrician",
        "cohort_period": "2023",
        "observation_period": "2024",
        "verification_status": "verified",
        "geography_level": "state",
    }
    assert "provider_id" not in params


def test_provider_id_is_only_sent_for_provider_level_geography() -> None:
    params = build_outcome_params(
        {"geography_level": "provider", "provider_id": "provider-01"}
    )
    assert params["geography_level"] == "provider"
    assert params["provider_id"] == "provider-01"


def test_outcome_pagination_bounds_are_validated() -> None:
    with pytest.raises(ValueError):
        build_outcome_params({}, limit=101)
    with pytest.raises(ValueError):
        build_outcome_params({}, offset=-1)


def test_fetch_outcome_page_uses_bounded_query_and_returns_api_records(monkeypatch) -> None:
    requested = {}
    payload = [make_record()]

    def fake_urlopen(request, timeout):
        requested["url"] = request.full_url
        requested["timeout"] = timeout
        return FakeResponse(payload)

    monkeypatch.setattr("app.outcome_explorer.urlopen", fake_urlopen)
    records = fetch_outcome_page(
        {"geography_level": "state", "geography_name": "Maharashtra"},
        offset=50,
        api_base_url="https://api.example.org/path",
    )

    query = parse_qs(urlsplit(requested["url"]).query)
    assert records == payload
    assert urlsplit(requested["url"]).path == "/path/api/v1/outcomes"
    assert query["limit"] == ["50"]
    assert query["offset"] == ["50"]
    assert query["geography_level"] == ["state"]
    assert query["geography_name"] == ["Maharashtra"]
    assert requested["timeout"] > 0


def test_offline_api_raises_without_substituting_local_records(monkeypatch) -> None:
    def offline(*_args, **_kwargs):
        raise URLError("offline")

    monkeypatch.setattr("app.outcome_explorer.urlopen", offline)
    with pytest.raises(OutcomeApiError) as error:
        fetch_outcome_page({}, api_base_url="http://127.0.0.1:8000")

    assert error.value.kind == "offline"


def test_invalid_api_url_fails_before_network_request(monkeypatch) -> None:
    called = False

    def unexpected(*_args, **_kwargs):
        nonlocal called
        called = True
        raise AssertionError("Network must not be called.")

    monkeypatch.setattr("app.outcome_explorer.urlopen", unexpected)
    with pytest.raises(OutcomeApiError) as error:
        fetch_outcome_page({}, api_base_url="javascript:alert(1)")

    assert error.value.kind == "configuration"
    assert called is False


def test_numeric_value_requires_all_verified_api_flags() -> None:
    verified = make_record()
    assert is_numeric_value_displayable(verified) is True

    for field, value in (
        ("verification_status", "synthetic_demo"),
        ("value_status", "withheld"),
        ("source_verified", False),
        ("displayable", False),
        ("value", None),
    ):
        candidate = {**verified, field: value}
        assert is_numeric_value_displayable(candidate) is False


def test_comparison_allows_compatible_records_and_discloses_period_differences() -> None:
    first = make_record()
    second = make_record(
        evidence_id="evidence-2",
        geography_name="Gujarat",
        cohort_period="2022",
        observation_period="2023",
        follow_up_period="18 months",
    )

    assessment = comparison_assessment(first, second)

    assert assessment.compatible is True
    assert assessment.mismatches == ()
    assert any(item.startswith("geography:") for item in assessment.period_differences)
    assert any(item.startswith("cohort:") for item in assessment.period_differences)
    assert any(item.startswith("observation:") for item in assessment.period_differences)
    assert any(item.startswith("follow-up:") for item in assessment.period_differences)


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        ({"metric_code": "employment_rate"}, "metric"),
        ({"definition": "A different definition."}, "metric"),
        ({"metric_kind": "earnings"}, "kind"),
        ({"unit": "months"}, "unit"),
        ({"geography_level": "district"}, "geography"),
        ({"trade_or_job_role": "Fitter"}, "trade"),
    ],
)
def test_comparison_rejects_incompatible_observations(overrides, expected) -> None:
    assessment = comparison_assessment(make_record(), make_record(**overrides))
    assert assessment.compatible is False
    assert expected in assessment.mismatches


def test_provider_level_comparison_requires_provider_identity() -> None:
    first = make_record(geography_level="provider", provider_id=None)
    second = make_record(geography_level="provider", provider_id="provider-2")

    assessment = comparison_assessment(first, second)

    assert assessment.compatible is False
    assert "provider" in assessment.mismatches


def test_render_offline_state_in_english_and_marathi(monkeypatch) -> None:
    def offline(*_args, **_kwargs):
        raise URLError("offline")

    monkeypatch.setattr("app.outcome_explorer.urlopen", offline)
    for locale in ("English", "मराठी"):
        st = FakeStreamlit()
        render_outcome_explorer(st, locale, api_base_url="http://127.0.0.1:8000")
        messages = [str(event) for event in st.events]
        assert OUTCOME_EXPLORER_COPY[locale]["heading"] in messages[0]
        assert any(OUTCOME_EXPLORER_COPY[locale]["offline"] in message for message in messages)


def test_render_verified_result_shows_source_and_numeric_value(monkeypatch) -> None:
    payload = [make_record()]

    monkeypatch.setattr(
        "app.outcome_explorer.urlopen",
        lambda *_args, **_kwargs: FakeResponse(payload),
    )
    st = FakeStreamlit()
    render_outcome_explorer(st, "English", api_base_url="http://127.0.0.1:8000")

    rendered = "\n".join(str(event) for event in st.events)
    assert "62 %" in rendered
    assert "Test publisher" in rendered
    assert any(event[0] == "link_button" and event[2] == "https://example.org/evidence" for event in st.events)


def test_render_withheld_result_never_shows_unverified_numeric_value(monkeypatch) -> None:
    payload = [
        make_record(
            value=None,
            value_status="withheld",
            value_withheld=True,
            numeric_metadata_withheld=True,
            source_verified=False,
            displayable=False,
            verification_status="synthetic_demo",
            numerator=None,
            denominator=None,
            sample_size=None,
        )
    ]
    monkeypatch.setattr(
        "app.outcome_explorer.urlopen",
        lambda *_args, **_kwargs: FakeResponse(payload),
    )
    st = FakeStreamlit()
    render_outcome_explorer(st, "English", api_base_url="http://127.0.0.1:8000")

    rendered = "\n".join(str(event) for event in st.events)
    assert "withheld" in rendered
    assert "Synthetic demo" in rendered
    assert "62.0" not in rendered
