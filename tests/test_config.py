"""Runtime configuration validation tests."""

import pytest

from core.config import DEFAULT_DATABASE_URL, Settings


def test_local_sqlite_remains_the_default() -> None:
    settings = Settings()
    assert settings.database_url == DEFAULT_DATABASE_URL
    assert settings.api_host == "127.0.0.1"
    assert settings.api_port == 8000
    assert settings.database_echo is False


def test_environment_values_are_trimmed_and_parsed(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "  PathSaathi Test  ")
    monkeypatch.setenv("APP_ENV", "  test  ")
    monkeypatch.setenv("API_HOST", " 127.0.0.1 ")
    monkeypatch.setenv("API_PORT", " 8123 ")
    monkeypatch.setenv("PATHSAATHI_DATABASE_URL", " sqlite+pysqlite:///:memory: ")
    monkeypatch.setenv("DATABASE_ECHO", " YES ")

    settings = Settings()

    assert settings.app_name == "PathSaathi Test"
    assert settings.app_env == "test"
    assert settings.api_host == "127.0.0.1"
    assert settings.api_port == 8123
    assert settings.database_url == "sqlite+pysqlite:///:memory:"
    assert settings.database_echo is True


def test_postgresql_url_is_validated_without_opening_a_connection() -> None:
    settings = Settings(database_url="postgresql+psycopg://user:secret@localhost/pathsaathi")
    assert settings.database_url.startswith("postgresql+psycopg://")


@pytest.mark.parametrize("value", ["abc", "0", "-1", "65536", ""])
def test_invalid_api_port_environment_value_fails_fast(monkeypatch, value) -> None:
    monkeypatch.setenv("API_PORT", value)
    with pytest.raises(ValueError, match="API_PORT"):
        Settings()


@pytest.mark.parametrize("port", [0, -1, 65536, True])
def test_invalid_direct_api_port_fails_fast(port) -> None:
    with pytest.raises(ValueError, match="API_PORT"):
        Settings(api_port=port)


@pytest.mark.parametrize("value", ["", "   ", "maybe", "enabled"])
def test_invalid_database_echo_environment_value_fails_fast(monkeypatch, value) -> None:
    monkeypatch.setenv("DATABASE_ECHO", value)
    with pytest.raises(ValueError, match="DATABASE_ECHO"):
        Settings()


@pytest.mark.parametrize(
    "database_url",
    [
        "",
        "   ",
        "not-a-url",
        "mysql://user:secret@localhost/pathsaathi",
        "postgresql+psycopg:///pathsaathi",
    ],
)
def test_invalid_database_url_fails_fast(database_url) -> None:
    with pytest.raises(ValueError, match="PATHSAATHI_DATABASE_URL"):
        Settings(database_url=database_url)


@pytest.mark.parametrize(
    ("field", "value"),
    [("app_name", " "), ("app_env", ""), ("api_host", " "), ("api_host", "local host")],
)
def test_invalid_required_text_settings_fail_fast(field, value) -> None:
    with pytest.raises(ValueError):
        Settings(**{field: value})


@pytest.mark.parametrize("value", ["false", "0", "no", "off", "FALSE"])
def test_false_boolean_tokens_are_supported(monkeypatch, value) -> None:
    monkeypatch.setenv("DATABASE_ECHO", value)
    assert Settings().database_echo is False


@pytest.mark.parametrize("value", ["true", "1", "yes", "on", "TRUE"])
def test_true_boolean_tokens_are_supported(monkeypatch, value) -> None:
    monkeypatch.setenv("DATABASE_ECHO", value)
    assert Settings().database_echo is True


def test_direct_database_url_is_normalized() -> None:
    settings = Settings(database_url=" sqlite+pysqlite:///:memory: ")
    assert settings.database_url == "sqlite+pysqlite:///:memory:"
