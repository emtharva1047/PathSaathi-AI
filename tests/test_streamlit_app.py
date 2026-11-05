"""Tests for the bilingual Streamlit shell and optional API health check."""

import json
import sys
from contextlib import nullcontext
from urllib.error import URLError
from unittest.mock import patch

from app import streamlit_app
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


def test_home_renders_progress_help_and_continue_control(monkeypatch) -> None:
    fake_streamlit = FakeStreamlit(locale="English", page="home")
    monkeypatch.setitem(sys.modules, "streamlit", fake_streamlit)
    monkeypatch.setattr(streamlit_app, "is_api_healthy", lambda: True)

    streamlit_app.main()

    assert fake_streamlit.progress_calls == [(1 / 3, "Step 1 of 3")]
    assert fake_streamlit.expanders == ["Need help?"]
    assert fake_streamlit.buttons == ["Continue"]
    assert fake_streamlit.radio_options == ("home", "profile", "pathways")


def test_marathi_profile_renders_localised_progress_and_back_next_controls(monkeypatch) -> None:
    fake_streamlit = FakeStreamlit(locale="मराठी", page="profile")
    monkeypatch.setitem(sys.modules, "streamlit", fake_streamlit)
    monkeypatch.setattr(streamlit_app, "is_api_healthy", lambda: True)

    streamlit_app.main()

    assert fake_streamlit.progress_calls == [(2 / 3, "टप्पा 2 / 3")]
    assert fake_streamlit.expanders == ["मदत हवी आहे?"]
    assert fake_streamlit.buttons == ["मागील टप्पा", "पुढील टप्पा"]
