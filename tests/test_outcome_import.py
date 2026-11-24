"""Tests for strict, provenance-aware outcome CSV validation."""

from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from hashlib import sha256

import pytest

import services.outcome_import as outcome_import
from services.outcome_import import parse_outcome_csv

HEADERS = [
    "evidence_id",
    "metric_code",
    "metric_label",
    "definition",
    "metric_kind",
    "value",
    "geography_level",
    "geography_name",
    "trade_or_job_role",
    "provider_id",
    "state",
    "district",
    "numerator",
    "denominator",
    "sample_size",
    "cohort_period",
    "observation_period",
    "currency",
    "unit",
    "statistic_type",
    "follow_up_period",
    "source_publisher",
    "source_url",
    "source_publication_date",
    "source_page_or_table",
    "methodology",
    "last_verified_at",
    "verification_status",
]


def base_row(**overrides: str) -> dict[str, str]:
    row = {
        "evidence_id": "synthetic-rate-01",
        "metric_code": "trade_related_employment_rate",
        "metric_label": "Trade-related employment",
        "definition": "Share of the defined cohort employed in the trained trade.",
        "metric_kind": "rate",
        "value": "60",
        "geography_level": "state",
        "geography_name": "Maharashtra",
        "trade_or_job_role": "Electrician",
        "provider_id": "",
        "state": "Maharashtra",
        "district": "",
        "numerator": "60",
        "denominator": "100",
        "sample_size": "80",
        "cohort_period": "2024 cohort",
        "observation_period": "2025 follow-up",
        "currency": "",
        "unit": "percent",
        "statistic_type": "unknown",
        "follow_up_period": "12 months",
        "source_publisher": "PathSaathi synthetic fixtures",
        "source_url": "",
        "source_publication_date": "",
        "source_page_or_table": "synthetic fixture; not real outcomes",
        "methodology": "Fixed synthetic test data only.",
        "last_verified_at": "",
        "verification_status": "synthetic_demo",
    }
    row.update(overrides)
    return row


def make_csv(rows: list[dict[str, str]], headers: list[str] | None = None) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=headers or HEADERS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def parse(
    payload: bytes,
    *,
    filename: str = "synthetic-outcomes.csv",
    imported_at: datetime | None = None,
):
    return parse_outcome_csv(
        payload,
        dataset_id="synthetic-test-dataset",
        dataset_version="v1",
        source_filename=filename,
        imported_at=imported_at or datetime(2026, 11, 24, 3, 30, tzinfo=timezone.utc),
    )


def test_valid_synthetic_rate_has_audit_metadata_and_is_not_verified() -> None:
    payload = make_csv([base_row()])

    report = parse(payload, filename="../fixtures/synthetic.csv")

    assert report.ready_to_import is True
    assert report.accepted_row_count == 1
    assert report.rejected_row_count == 0
    assert report.records[0].verification_status == "synthetic_demo"
    assert report.records[0].is_verified_displayable is False
    assert report.source_filename == "synthetic.csv"
    assert report.source_sha256 == sha256(payload).hexdigest()
    assert report.dataset_id == "synthetic-test-dataset"
    assert report.dataset_version == "v1"
    assert report.imported_at.tzinfo == timezone.utc


def test_rate_is_derived_only_from_explicit_counts_and_disclosed() -> None:
    row = base_row(value="", numerator="1", denominator="3")

    report = parse(make_csv([row]))

    assert report.ready_to_import is True
    assert report.records[0].value == pytest.approx(100 / 3)
    assert report.derived_rate_evidence_ids == ("synthetic-rate-01",)
    assert any(item.code == "rate_derived" for item in report.warnings)


def test_published_rate_must_reconcile_with_counts() -> None:
    report = parse(make_csv([base_row(value="20", numerator="60", denominator="100")]))

    assert report.ready_to_import is False
    assert report.errors[0].code == "rate_count_mismatch"
    assert report.records == ()


def test_source_reported_rate_without_counts_is_kept_with_warning() -> None:
    row = base_row(numerator="", denominator="", sample_size="")

    report = parse(make_csv([row]))

    assert report.ready_to_import is True
    assert report.records[0].numerator is None
    assert report.records[0].denominator is None
    assert report.records[0].sample_size is None
    assert any(item.code == "rate_counts_unavailable" for item in report.warnings)


def test_blank_outcome_and_context_values_remain_unknown() -> None:
    row = base_row(
        value="",
        numerator="",
        denominator="",
        sample_size="",
        cohort_period="",
        observation_period="",
        follow_up_period="",
    )

    report = parse(make_csv([row]))

    assert report.ready_to_import is True
    record = report.records[0]
    assert record.value is None
    assert record.numerator is None
    assert record.denominator is None
    assert record.sample_size is None
    assert record.cohort_period is None
    assert record.observation_period is None
    assert record.follow_up_period is None
    assert len(report.warnings) >= 4


def test_uploaded_file_cannot_mark_evidence_verified() -> None:
    report = parse(make_csv([base_row(verification_status="verified")]))

    assert report.ready_to_import is False
    assert report.errors[0].code == "manual_verification_required"


def test_only_documented_headers_are_accepted() -> None:
    headers = HEADERS + ["salary_guess"]
    row = base_row(salary_guess="18000")
    report = parse(make_csv([row], headers=headers))

    assert report.ready_to_import is False
    assert any(item.code == "unknown_header" for item in report.errors)


def test_duplicate_headers_are_rejected() -> None:
    headers = HEADERS + ["evidence_id"]
    report = parse(make_csv([base_row()], headers=headers))

    assert report.ready_to_import is False
    assert any(item.code == "duplicate_header" for item in report.errors)


def test_missing_required_header_is_rejected() -> None:
    headers = [item for item in HEADERS if item != "definition"]
    report = parse(make_csv([base_row()], headers=headers))

    assert report.ready_to_import is False
    assert any(
        item.code == "missing_required_header" and item.field_name == "definition"
        for item in report.errors
    )


def test_source_reference_is_required() -> None:
    report = parse(
        make_csv([base_row(source_page_or_table="", source_url="")])
    )

    assert report.ready_to_import is False
    assert report.errors[0].code == "source_reference_required"


def test_source_url_must_be_http_or_https_without_credentials() -> None:
    report = parse(
        make_csv(
            [base_row(source_url="file:///tmp/report.csv", source_page_or_table="")]
        )
    )

    assert report.ready_to_import is False
    assert report.errors[0].code == "invalid_source_url"


def test_provider_scope_requires_provider_id() -> None:
    report = parse(
        make_csv([base_row(geography_level="provider", provider_id="")])
    )

    assert report.ready_to_import is False
    assert report.errors[0].code == "provider_id_required"


def test_provider_id_cannot_be_attached_to_state_aggregate() -> None:
    report = parse(
        make_csv([base_row(geography_level="state", provider_id="provider-01")])
    )

    assert report.ready_to_import is False
    assert report.errors[0].code == "provider_scope_mismatch"


def test_rate_counts_must_be_complete_and_bounded() -> None:
    incomplete = parse(make_csv([base_row(numerator="60", denominator="")]))
    impossible = parse(make_csv([base_row(numerator="101", denominator="100")]))

    assert incomplete.errors[0].code == "incomplete_rate_counts"
    assert impossible.errors[0].code == "invalid_rate_counts"


def test_earnings_require_currency_unit_and_statistic_type() -> None:
    row = base_row(
        metric_code="median_monthly_earnings",
        metric_label="Median monthly earnings",
        metric_kind="earnings",
        value="18000",
        numerator="",
        denominator="",
        unit="",
        currency="",
        statistic_type="unknown",
    )

    report = parse(make_csv([row]))

    assert report.ready_to_import is False
    assert report.errors[0].code == "incomplete_earnings_semantics"


def test_earnings_with_explicit_semantics_are_accepted_as_synthetic() -> None:
    row = base_row(
        metric_code="median_monthly_earnings",
        metric_label="Median monthly earnings",
        metric_kind="earnings",
        value="18000",
        numerator="",
        denominator="",
        unit="per month",
        currency="INR",
        statistic_type="median",
    )

    report = parse(make_csv([row]))

    assert report.ready_to_import is True
    assert report.records[0].currency == "INR"
    assert report.records[0].statistic_type == "median"
    assert report.records[0].verification_status == "synthetic_demo"


def test_duplicate_evidence_ids_block_the_entire_file() -> None:
    report = parse(make_csv([base_row(), base_row()]))

    assert report.ready_to_import is False
    assert report.accepted_row_count == 1
    assert report.rejected_row_count == 1
    assert report.errors[0].code == "duplicate_evidence_id"
    with pytest.raises(ValueError, match="not ready"):
        report.require_importable_records()


def test_valid_preview_rows_cannot_be_staged_when_another_row_fails() -> None:
    invalid = base_row(evidence_id="bad-row", metric_kind="unsupported")
    report = parse(make_csv([base_row(), invalid]))

    assert report.accepted_row_count == 1
    assert report.ready_to_import is False
    with pytest.raises(ValueError, match="not ready"):
        report.require_importable_records()


def test_row_width_mismatch_is_rejected() -> None:
    payload = (
        ",".join(HEADERS)
        + "\n"
        + ",".join(base_row()[field] for field in HEADERS)
        + ",unexpected\n"
    ).encode()

    report = parse(payload)

    assert report.ready_to_import is False
    assert report.errors[0].code == "row_width_mismatch"


def test_invalid_date_is_reported_as_a_row_error() -> None:
    report = parse(make_csv([base_row(source_publication_date="24-11-2026")]))

    assert report.ready_to_import is False
    assert report.errors[0].code == "invalid_date"


def test_non_finite_values_are_rejected() -> None:
    report = parse(make_csv([base_row(value="NaN", numerator="", denominator="")]))

    assert report.ready_to_import is False
    assert report.errors[0].code == "non_finite_number"


def test_malformed_csv_and_invalid_utf8_are_rejected() -> None:
    malformed = parse(b'evidence_id,metric_code\n"unterminated,value\n')
    invalid_encoding = parse(b"evidence_id,metric_code\n\xff,rate\n")

    assert malformed.errors[0].code == "malformed_csv"
    assert invalid_encoding.errors[0].code == "invalid_encoding"


def test_file_size_limit_is_enforced(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(outcome_import, "MAX_IMPORT_BYTES", 4)

    report = parse(b"12345")

    assert report.ready_to_import is False
    assert report.errors[0].code == "file_too_large"


def test_row_limit_is_enforced_without_partial_import(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(outcome_import, "MAX_IMPORT_ROWS", 1)
    report = parse(make_csv([base_row(), base_row(evidence_id="synthetic-rate-02")]))

    assert report.ready_to_import is False
    assert report.errors[0].code == "row_limit_exceeded"
    with pytest.raises(ValueError, match="not ready"):
        report.require_importable_records()


def test_integer_fields_reject_malformed_signs() -> None:
    report = parse(make_csv([base_row(numerator="+-60")]))

    assert report.ready_to_import is False
    assert report.errors[0].code == "invalid_integer"


def test_dates_require_extended_iso_format() -> None:
    report = parse(make_csv([base_row(source_publication_date="20261124")]))

    assert report.ready_to_import is False
    assert report.errors[0].code == "invalid_date"


def test_import_metadata_requires_dataset_identity_and_timezone() -> None:
    with pytest.raises(ValueError, match="dataset_id and dataset_version"):
        parse_outcome_csv(
            make_csv([base_row()]),
            dataset_id=" ",
            dataset_version="v1",
            source_filename="demo.csv",
        )
    with pytest.raises(ValueError, match="timezone-aware"):
        parse_outcome_csv(
            make_csv([base_row()]),
            dataset_id="dataset",
            dataset_version="v1",
            source_filename="demo.csv",
            imported_at=datetime(2026, 11, 24),
        )
