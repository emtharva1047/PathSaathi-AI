"""Tests for the bilingual Streamlit shell and optional API health check."""

from __future__ import annotations

import json
import sys
from contextlib import nullcontext
from types import SimpleNamespace
from urllib.error import URLError
from unittest.mock import patch

import pytest

from app import streamlit_app
from app.counselling_flow import COUNSELLING_COPY
from app.profile_flow import PROFILE_COPY
from app.streamlit_app import TRANSLATIONS, is_api_healthy


class StubResponse:
    """Minimal context-manager response for urllib health-check tests."""

    status = 200

    def __init__(self, payload: object) -> None:
        self.payload = payload

    def __enter__(self) -> "StubResponse":
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


class FakeSidebar:
    """Record sidebar controls without requiring a browser session."""

    def __init__(self, parent: FakeStreamlit) -> None:
        self.parent = parent

    def selectbox(self, _label: str, options: list[str]) -> str:
        return self.parent.locale if self.parent.locale in options else options[0]

    def radio(
        self,
        _label: str,
        options: tuple[str, ...],
        *,
        format_func,
        key: str,
    ) -> str:
        assert callable(format_func)
        self.parent.radio_options = options
        return self.parent.session_state.get(key, options[0])

    def __getattr__(self, name: str):
        return lambda *args, **kwargs: self.parent.calls.append((f"sidebar.{name}", args, kwargs))


class FakeStreamlit:
    """Small Streamlit surface used to assert accessible navigation affordances."""

    def __init__(self, *, locale: str = "English", page: str = "home") -> None:
        self.locale = locale
        self.session_state = {"page_navigation": page}
        self.sidebar = FakeSidebar(self)
        self.calls: list[tuple[str, tuple, dict]] = []
        self.buttons: list[str] = []
        self.expanders: list[str] = []
        self.progress_calls: list[tuple[float, str]] = []
        self.radio_options: tuple[str, ...] = ()
        self.components = SimpleNamespace(v1=SimpleNamespace(html=self._render_html))

    def _render_html(self, markup: str, *, height: int, scrolling: bool) -> None:
        self.calls.append(("components.v1.html", (markup,), {"height": height, "scrolling": scrolling}))

    def set_page_config(self, **kwargs) -> None:
        self.calls.append(("set_page_config", (), kwargs))

    def expander(self, label: str, *, expanded: bool = False):
        self.expanders.append(label)
        return nullcontext()

    def progress(self, value: float, *, text: str) -> None:
        self.progress_calls.append((value, text))

    def button(self, label: str, **kwargs) -> None:
        self.buttons.append(label)

    def __getattr__(self, name: str):
        return lambda *args, **kwargs: self.calls.append((name, args, kwargs))


def test_translation_catalogues_have_matching_keys() -> None:
    english = set(TRANSLATIONS["English"])
    marathi = set(TRANSLATIONS["मराठी"])

    assert english == marathi
    assert {
        "nav_home",
        "nav_profile",
        "nav_conversation",
        "nav_pathways",
        "progress",
        "help_title",
        "help_body",
        "back",
        "next",
        "api_online",
        "api_offline",
    } <= english


def test_api_health_check_accepts_expected_contract() -> None:
    response = StubResponse({"status": "ok", "service": "pathsaathi-api"})

    with patch("app.streamlit_app.urlopen", return_value=response) as mocked:
        assert is_api_healthy("http://localhost:8000/") is True

    request = mocked.call_args.args[0]
    assert request.full_url == "http://localhost:8000/health"
    assert mocked.call_args.kwargs["timeout"] == 2.0


def test_api_health_check_rejects_unexpected_payload() -> None:
    response = StubResponse({"status": "ok", "service": "different-service"})

    with patch("app.streamlit_app.urlopen", return_value=response):
        assert is_api_healthy("http://localhost:8000") is False


def test_api_health_check_fails_gracefully_when_api_is_unavailable() -> None:
    with patch("app.streamlit_app.urlopen", side_effect=URLError("connection refused")):
        assert is_api_healthy("http://localhost:8000") is False


def test_api_health_check_uses_environment_url_override(monkeypatch) -> None:
    monkeypatch.setenv("PATHSAATHI_API_URL", "https://api.example.test/path/")

    with patch(
        "app.streamlit_app.urlopen",
        return_value=StubResponse({"status": "ok", "service": "pathsaathi-api"}),
    ) as mocked:
        assert is_api_healthy() is True

    request = mocked.call_args.args[0]
    assert request.full_url == "https://api.example.test/path/health"


def test_explicit_api_base_url_takes_precedence_over_environment(monkeypatch) -> None:
    monkeypatch.setenv("PATHSAATHI_API_URL", "https://environment.example.test")

    with patch(
        "app.streamlit_app.urlopen",
        return_value=StubResponse({"status": "ok", "service": "pathsaathi-api"}),
    ) as mocked:
        assert is_api_healthy("http://explicit.example.test:9000/") is True

    request = mocked.call_args.args[0]
    assert request.full_url == "http://explicit.example.test:9000/health"


@pytest.mark.parametrize(
    "invalid_url",
    [
        "",
        "not-a-url",
        "ftp://api.example.test",
        "http://user:secret@api.example.test",
        "http://localhost:99999",
        "http://localhost:8000?debug=1",
        "http://localhost:8000#health",
    ],
)
def test_invalid_api_url_fails_closed_without_network_request(
    monkeypatch, invalid_url: str
) -> None:
    monkeypatch.setenv("PATHSAATHI_API_URL", invalid_url)

    with patch("app.streamlit_app.urlopen") as mocked:
        assert is_api_healthy() is False

    mocked.assert_not_called()


def test_home_renders_progress_help_and_continue_control(monkeypatch) -> None:
    fake_streamlit = FakeStreamlit(locale="English", page="home")
    monkeypatch.setitem(sys.modules, "streamlit", fake_streamlit)
    monkeypatch.setattr(streamlit_app, "is_api_healthy", lambda: True)

    streamlit_app.main()

    assert fake_streamlit.progress_calls == [(1 / 4, "Step 1 of 4")]
    assert fake_streamlit.expanders == ["Need help?"]
    assert fake_streamlit.buttons == ["Continue"]
    assert fake_streamlit.radio_options == ("home", "profile", "conversation", "pathways")
    read_aloud = [call for call in fake_streamlit.calls if call[0] == "components.v1.html"]
    assert len(read_aloud) == 1
    assert "Read page introduction aloud" in read_aloud[0][1][0]
    assert "Explore vocational pathways together." in read_aloud[0][1][0]


def test_marathi_profile_renders_localised_progress_and_back_next_controls(monkeypatch) -> None:
    fake_streamlit = FakeStreamlit(locale="मराठी", page="profile")
    monkeypatch.setitem(sys.modules, "streamlit", fake_streamlit)
    monkeypatch.setattr(streamlit_app, "is_api_healthy", lambda: True)

    streamlit_app.main()

    assert fake_streamlit.progress_calls == [
        (2 / 4, "टप्पा 2 / 4"),
        (1 / 7, "प्रश्न 1 / 7"),
    ]
    assert fake_streamlit.expanders == ["मदत हवी आहे?"]
    assert fake_streamlit.buttons == ["पुढील प्रश्न"]
    read_aloud = [call for call in fake_streamlit.calls if call[0] == "components.v1.html"]
    assert len(read_aloud) == 1
    assert "पानाची ओळख मोठ्याने वाचा" in read_aloud[0][1][0]
    assert "data-locale=\"mr-IN\"" in read_aloud[0][1][0]



@pytest.mark.parametrize(
    ("locale", "page"),
    [
        ("English", "home"),
        ("English", "profile"),
        ("English", "conversation"),
        ("English", "pathways"),
        ("मराठी", "home"),
        ("मराठी", "profile"),
        ("मराठी", "conversation"),
        ("मराठी", "pathways"),
    ],
)
def test_offline_ui_shows_localised_status_and_keeps_each_page_usable(
    monkeypatch, locale: str, page: str
) -> None:
    """Keep the bilingual informational journey available when the API is offline."""
    fake_streamlit = FakeStreamlit(locale=locale, page=page)
    monkeypatch.setitem(sys.modules, "streamlit", fake_streamlit)
    monkeypatch.setattr(streamlit_app, "is_api_healthy", lambda: False)

    streamlit_app.main()

    copy = TRANSLATIONS[locale]
    sidebar_warnings = [
        args[0] for name, args, _ in fake_streamlit.calls if name == "sidebar.warning"
    ]
    sidebar_captions = [
        args[0] for name, args, _ in fake_streamlit.calls if name == "sidebar.caption"
    ]
    rendered_text = [
        argument
        for _, args, _ in fake_streamlit.calls
        for argument in args
        if isinstance(argument, str)
    ]

    assert sidebar_warnings == [copy["api_offline"]]
    assert copy["api_label"] in sidebar_captions
    assert copy["api_fallback"] in sidebar_captions
    assert not any(name == "sidebar.success" for name, _, _ in fake_streamlit.calls)

    page_copy = {
        "home": (
            copy["title"],
            copy["tagline"],
            copy["notice"],
            copy["welcome"],
            copy["home_next"],
        ),
        "profile": (
            copy["profile_heading"],
            copy["profile_description"],
            copy["profile_placeholder"],
        ),
        "conversation": (
            copy["conversation_heading"],
            copy["conversation_description"],
            COUNSELLING_COPY[locale]["prompt_titles"]["learner_evidence_questions"],
        ),
        "pathways": (
            copy["pathways_heading"],
            copy["pathways_description"],
            copy["pathways_placeholder"],
        ),
    }
    assert all(
        any(expected in rendered for rendered in rendered_text)
        for expected in page_copy[page]
    )

    page_index = ("home", "profile", "conversation", "pathways").index(page)
    expected_progress = [
        (
            (page_index + 1) / 4,
            copy["progress"].format(step=page_index + 1, total=4),
        )
    ]
    if page == "profile":
        expected_progress.append(
            (
                1 / 7,
                PROFILE_COPY[locale]["progress"].format(step=1, total=7),
            )
        )
    elif page == "conversation":
        expected_progress.append(
            (
                1 / 7,
                COUNSELLING_COPY[locale]["progress"].format(step=1, total=6),
            )
        )
    assert fake_streamlit.progress_calls == expected_progress
    assert fake_streamlit.expanders == [copy["help_title"]]
    expected_buttons = {
        "home": [copy["next"]],
        "profile": [PROFILE_COPY[locale]["next"]],
        "conversation": [
            COUNSELLING_COPY[locale]["skip"],
            COUNSELLING_COPY[locale]["continue"],
        ],
        "pathways": [copy["back"]],
    }
    assert fake_streamlit.buttons == expected_buttons[page]


def test_pathways_page_renders_the_illustrative_shortlist_and_unknown_eligibility(
    monkeypatch,
) -> None:
    fake_streamlit = FakeStreamlit(locale="English", page="pathways")
    monkeypatch.setitem(sys.modules, "streamlit", fake_streamlit)
    monkeypatch.setattr(streamlit_app, "is_api_healthy", lambda: False)

    streamlit_app.main()

    rendered = [
        str(value)
        for _, args, _ in fake_streamlit.calls
        for value in args
    ]
    text = " ".join(rendered)
    assert "Illustrative demo catalogue only" in text
    assert "Illustrative technology-support theme" in text
    assert "Unknown — verified entry criteria or learner information are missing" in text
    assert "Assistant Baking Technician" in text
    assert "Plant Biscuit Production Specialist" in text
    assert "Qualification entry-route screening" in text
    assert "Route 1 — Grade 10" in text
    assert "Cannot determine yet" in text
