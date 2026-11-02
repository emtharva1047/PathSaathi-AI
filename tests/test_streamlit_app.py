"""Tests for the bilingual Streamlit shell and optional API health check."""

import json
from urllib.error import URLError
from unittest.mock import patch

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


def test_translation_catalogues_have_matching_keys() -> None:
    english = set(TRANSLATIONS["English"])
    marathi = set(TRANSLATIONS["मराठी"])

    assert english == marathi
    assert {"nav_home", "nav_profile", "nav_pathways", "api_online", "api_offline"} <= english


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
