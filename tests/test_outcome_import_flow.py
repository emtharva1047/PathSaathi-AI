"""Tests for the bilingual, preview-only outcome CSV Streamlit section."""

from __future__ import annotations

import csv
import io
import sys
from contextlib import nullcontext
from types import SimpleNamespace

import pytest

from app import outcome_import_flow, streamlit_app
from app.outcome_import_flow import OUTCOME_IMPORT_COPY, render_outcome_import


class FakeUpload:
    def __init__(
        self,
        payload: bytes,
        *,
        name: str = "outcomes.csv",
        mime: str = "text/csv",
    ) -> None:
        self.payload = payload
        self.name = name
        self.type = mime

    def getvalue(self) -> bytes:
        return self.payload


class FakeStreamlit:
    def __init__(
        self,
        *,
        upload: FakeUpload | None = None,
        inputs: dict[str, str] | None = None,
    ) -> None:
        self.upload = upload
        self.inputs = inputs or {}
        self.calls: list[tuple[str, tuple, dict]] = []

    def text_input(self, label: str, *, value: str, key: str) -> str:
        self.calls.append(("text_input", (label,), {"key": key}))
        return self.inputs.get(key, value)

    def file_uploader(self, label: str, **kwargs):
        self.calls.append(("file_uploader", (label,), kwargs))
        return self.upload

    def __getattr__(self, name: str):
        return lambda *args, **kwargs: self.calls.append((name, args, kwargs))


class FakeAppSidebar:
    def __init__(self, parent: FakeAppStreamlit) -> None:
        self.parent = parent

    def selectbox(self, _label: str, options: list[str]) -> str:
        return self.parent.locale if self.parent.locale in options else options[0]

    def radio(self, _label: str, options: tuple[str, ...], *, format_func, key: str) -> str:
        assert callable(format_func)
        assert options
        return self.parent.session_state[key]

    def __getattr__(self, _name: str):
        return lambda *_args, **_kwargs: None


class FakeAppStreamlit:
    def __init__(self, *, locale: str = "English") -> None:
        self.locale = locale
        self.session_state = {"page_navigation": "pathways"}
        self.sidebar = FakeAppSidebar(self)
        self.components = SimpleNamespace(v1=SimpleNamespace(html=lambda *_args, **_kwargs: None))

    def set_page_config(self, **_kwargs) -> None:
        return None

    def expander(self, _label: str, *, expanded: bool = False):
        return nullcontext()

    def __getattr__(self, _name: str):
        return lambda *_args, **_kwargs: None


def valid_csv(*, status: str = "synthetic_demo", include_bad_row: bool = False) -> bytes:
    headers = [
        "evidence_id",
        "metric_code",
        "metric_label",
        "definition",
        "metric_kind",
        "geography_level",
        "geography_name",
        "source_publisher",
        "verification_status",
        "source_page_or_table",
        "value",
        "unit",
        "cohort_period",
        "sample_size",
    ]
    rows = [
        {
            "evidence_id": "demo-01",
            "metric_code": "trade_related_employment_rate",
            "metric_label": "Trade-related employment",
            "definition": "Synthetic test fixture only.",
            "metric_kind": "rate",
            "geography_level": "state",
            "geography_name": "Maharashtra",
            "source_publisher": "PathSaathi synthetic fixtures",
            "verification_status": status,
            "source_page_or_table": "Synthetic fixture; not real outcomes",
            "value": "60",
            "unit": "percent",
            "cohort_period": "2024 synthetic cohort",
            "sample_size": "10",
        }
    ]
    if include_bad_row:
        bad = dict(rows[0])
        bad["evidence_id"] = "bad-02"
        bad["verification_status"] = "verified"
        rows.append(bad)
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=headers, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def configured_inputs() -> dict[str, str]:
    return {
        "outcome_dataset_id": "synthetic-test",
        "outcome_dataset_version": "v1",
    }


def messages(fake: FakeStreamlit, name: str) -> list[str]:
    return [
        str(args[0])
        for call_name, args, _kwargs in fake.calls
        if call_name == name and args
    ]


def test_translation_catalogues_have_matching_keys() -> None:
    assert set(OUTCOME_IMPORT_COPY["English"]) == set(OUTCOME_IMPORT_COPY["मराठी"])


def test_empty_state_is_bilingual_and_explains_no_upload() -> None:
    fake = FakeStreamlit()

    render_outcome_import(fake, "मराठी")

    rendered = " ".join(messages(fake, "subheader") + messages(fake, "write"))
    assert "CSV तपासा" in rendered
    assert any("CSV फाइल निवडा" in item for item in messages(fake, "caption"))
    uploader = next(call for call in fake.calls if call[0] == "file_uploader")
    assert uploader[2]["type"] == ["csv"]
    assert uploader[2]["accept_multiple_files"] is False


def test_valid_synthetic_csv_shows_audit_metadata_and_explicit_demo_status() -> None:
    fake = FakeStreamlit(
        upload=FakeUpload(valid_csv()),
        inputs=configured_inputs(),
    )

    render_outcome_import(fake, "English")

    rendered = " ".join(
        str(value)
        for _name, args, _kwargs in fake.calls
        for value in args
    )
    assert "synthetic-test · v1" in rendered
    assert "SHA-256" in rendered
    assert "SYNTHETIC DEMO — not real outcomes" in rendered
    assert "Every nonblank row passed canonical validation" in rendered
    assert any(name == "table" for name, _args, _kwargs in fake.calls)
    assert any(name == "info" and "No database" in args[0] for name, args, _ in fake.calls)


def test_failed_partial_file_never_renders_a_table_or_success_state() -> None:
    fake = FakeStreamlit(
        upload=FakeUpload(valid_csv(include_bad_row=True)),
        inputs=configured_inputs(),
    )

    render_outcome_import(fake, "English")

    assert not any(name == "table" for name, _args, _kwargs in fake.calls)
    assert any(
        name == "error" and "file is not ready" in args[0]
        for name, args, _ in fake.calls
    )
    assert any(
        name == "error" and "manual_verification_required" in args[0]
        for name, args, _ in fake.calls
    )


def test_non_csv_extension_is_rejected_before_parser(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = FakeStreamlit(
        upload=FakeUpload(
            b"not csv",
            name="outcomes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ),
        inputs=configured_inputs(),
    )
    monkeypatch.setattr(
        outcome_import_flow,
        "parse_outcome_csv",
        lambda *_args, **_kwargs: pytest.fail("parser must not run for a non-CSV file"),
    )

    render_outcome_import(fake, "English")

    assert messages(fake, "error") == [OUTCOME_IMPORT_COPY["English"]["extension_error"]]


def test_unsupported_mime_is_rejected_before_parser(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = FakeStreamlit(
        upload=FakeUpload(b"payload", mime="application/pdf"),
        inputs=configured_inputs(),
    )
    monkeypatch.setattr(
        outcome_import_flow,
        "parse_outcome_csv",
        lambda *_args, **_kwargs: pytest.fail("parser must not run for a non-CSV MIME type"),
    )

    render_outcome_import(fake, "English")

    assert messages(fake, "error") == [OUTCOME_IMPORT_COPY["English"]["mime_error"]]


def test_oversized_upload_is_rejected_before_parser(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = FakeStreamlit(
        upload=FakeUpload(b"123456"),
        inputs=configured_inputs(),
    )
    monkeypatch.setattr(outcome_import_flow, "MAX_IMPORT_BYTES", 5)
    monkeypatch.setattr(
        outcome_import_flow,
        "parse_outcome_csv",
        lambda *_args, **_kwargs: pytest.fail("parser must not run for an oversized file"),
    )

    render_outcome_import(fake, "English")

    assert messages(fake, "error") == [OUTCOME_IMPORT_COPY["English"]["size_error"]]


def test_missing_dataset_metadata_does_not_call_parser(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = FakeStreamlit(upload=FakeUpload(valid_csv()))
    monkeypatch.setattr(
        outcome_import_flow,
        "parse_outcome_csv",
        lambda *_args, **_kwargs: pytest.fail("parser must not run without dataset metadata"),
    )

    render_outcome_import(fake, "English")

    assert messages(fake, "error") == [OUTCOME_IMPORT_COPY["English"]["metadata_required"]]


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        ("needs_review", "Needs review — not verified"),
        ("stale", "Stale — not current evidence"),
    ],
)
def test_unverified_and_stale_rows_keep_nonverified_status_labels(
    status: str,
    expected: str,
) -> None:
    fake = FakeStreamlit(
        upload=FakeUpload(valid_csv(status=status)),
        inputs=configured_inputs(),
    )

    render_outcome_import(fake, "English")

    table_call = next(args[0] for name, args, _ in fake.calls if name == "table")
    assert table_call[0]["Evidence status"] == expected
    assert table_call[0]["Evidence status"] != "Verified"


def test_pathways_page_includes_the_outcome_preview_section(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = FakeAppStreamlit()
    called: list[str] = []
    monkeypatch.setitem(sys.modules, "streamlit", fake)
    monkeypatch.setattr(streamlit_app, "is_api_healthy", lambda: False)
    monkeypatch.setattr(streamlit_app, "render_pathway_explorer", lambda *_args: None)
    monkeypatch.setattr(streamlit_app, "render_qualification_explainers", lambda *_args: None)
    monkeypatch.setattr(streamlit_app, "render_multi_route_eligibility", lambda *_args: None)
    monkeypatch.setattr(streamlit_app, "render_read_aloud", lambda *_args: None)
    monkeypatch.setattr(
        streamlit_app,
        "render_outcome_import",
        lambda _st, locale: called.append(locale),
    )

    streamlit_app.main()

    assert called == ["English"]
