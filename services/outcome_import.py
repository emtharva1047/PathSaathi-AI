"""Strict, provenance-aware CSV validation for outcome evidence imports.

The importer previews canonical records only. It never persists data and never trusts an
uploaded file to mark evidence as verified.
"""

from __future__ import annotations

import csv
import hashlib
import io
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Literal, cast
from urllib.parse import urlsplit

from core.domain import (
    GeographyLevel,
    MetricKind,
    OutcomeEvidenceRecord,
    StatisticType,
    VerificationStatus,
)

MAX_IMPORT_BYTES = 10 * 1024 * 1024
MAX_IMPORT_ROWS = 50_000
RATE_RECONCILIATION_TOLERANCE = Decimal("0.51")

_REQUIRED_COLUMNS = frozenset(
    {
        "evidence_id",
        "metric_code",
        "metric_label",
        "definition",
        "metric_kind",
        "geography_level",
        "geography_name",
        "source_publisher",
        "verification_status",
    }
)
_ALLOWED_COLUMNS = _REQUIRED_COLUMNS | frozenset(
    {
        "trade_or_job_role",
        "provider_id",
        "state",
        "district",
        "value",
        "numerator",
        "denominator",
        "sample_size",
        "cohort_period",
        "observation_period",
        "currency",
        "unit",
        "statistic_type",
        "follow_up_period",
        "source_url",
        "source_publication_date",
        "source_page_or_table",
        "methodology",
        "last_verified_at",
    }
)
_METRIC_KINDS = frozenset({"rate", "earnings", "count", "other"})
_GEOGRAPHY_LEVELS = frozenset({"national", "state", "district", "provider"})
_STATISTIC_TYPES = frozenset({"mean", "median", "band", "unknown"})
_IMPORTABLE_STATUSES = frozenset({"needs_review", "stale", "synthetic_demo"})


@dataclass(frozen=True, slots=True)
class ImportFinding:
    """One row- or file-level validation finding."""

    row_number: int
    severity: Literal["error", "warning"]
    code: str
    message: str
    field_name: str | None = None


@dataclass(frozen=True, slots=True)
class OutcomeImportReport:
    """Immutable preview and audit metadata for one CSV import attempt."""

    dataset_id: str
    dataset_version: str
    source_filename: str
    source_sha256: str
    imported_at: datetime
    row_count: int
    records: tuple[OutcomeEvidenceRecord, ...]
    findings: tuple[ImportFinding, ...]
    derived_rate_evidence_ids: tuple[str, ...]

    @property
    def errors(self) -> tuple[ImportFinding, ...]:
        """Return blocking validation findings."""
        return tuple(item for item in self.findings if item.severity == "error")

    @property
    def warnings(self) -> tuple[ImportFinding, ...]:
        """Return non-blocking interpretation caveats."""
        return tuple(item for item in self.findings if item.severity == "warning")

    @property
    def accepted_row_count(self) -> int:
        """Number of rows that passed domain validation."""
        return len(self.records)

    @property
    def rejected_row_count(self) -> int:
        """Number of data rows containing at least one blocking error."""
        return len({item.row_number for item in self.errors if item.row_number > 1})

    @property
    def ready_to_import(self) -> bool:
        """Whether every nonblank data row passed and the file is nonempty."""
        return self.row_count > 0 and not self.errors and len(self.records) == self.row_count

    def require_importable_records(self) -> tuple[OutcomeEvidenceRecord, ...]:
        """Return all records only when the entire file is safe to stage."""
        if not self.ready_to_import:
            raise ValueError(
                "Outcome import is not ready: resolve all row errors and submit a nonempty file."
            )
        return self.records


class _RowValidationError(ValueError):
    def __init__(self, field_name: str, code: str, message: str) -> None:
        super().__init__(message)
        self.field_name = field_name
        self.code = code


def _safe_filename(value: str) -> str:
    return value.replace("\\", "/").rsplit("/", 1)[-1].strip() or "upload.csv"


def _normalise_imported_at(value: datetime | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("imported_at must be timezone-aware.")
    return value.astimezone(timezone.utc)


def _text(row: Mapping[str, str], field_name: str) -> str | None:
    value = row.get(field_name, "").strip()
    return value or None


def _required_text(row: Mapping[str, str], field_name: str) -> str:
    value = _text(row, field_name)
    if value is None:
        raise _RowValidationError(field_name, "required", f"{field_name} is required.")
    return value


def _optional_decimal(row: Mapping[str, str], field_name: str) -> Decimal | None:
    raw = _text(row, field_name)
    if raw is None:
        return None
    try:
        value = Decimal(raw)
    except InvalidOperation as exc:
        raise _RowValidationError(
            field_name, "invalid_number", f"{field_name} must be a decimal number."
        ) from exc
    if not value.is_finite():
        raise _RowValidationError(
            field_name, "non_finite_number", f"{field_name} must be finite."
        )
    return value


def _optional_integer(row: Mapping[str, str], field_name: str) -> int | None:
    raw = _text(row, field_name)
    if raw is None:
        return None
    digits = raw[1:] if raw[:1] in {"+", "-"} else raw
    if not digits or not digits.isascii() or not digits.isdigit():
        raise _RowValidationError(
            field_name, "invalid_integer", f"{field_name} must be a whole number."
        )
    return int(raw, 10)


def _optional_date(row: Mapping[str, str], field_name: str) -> date | None:
    raw = _text(row, field_name)
    if raw is None:
        return None
    if re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", raw) is None:
        raise _RowValidationError(
            field_name, "invalid_date", f"{field_name} must use an ISO date (YYYY-MM-DD)."
        )
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise _RowValidationError(
            field_name, "invalid_date", f"{field_name} must use an ISO date (YYYY-MM-DD)."
        ) from exc


def _build_record(
    row: Mapping[str, str],
) -> tuple[OutcomeEvidenceRecord, bool, tuple[tuple[str, str], ...]]:
    evidence_id = _required_text(row, "evidence_id")
    metric_code = _required_text(row, "metric_code")
    metric_label = _required_text(row, "metric_label")
    definition = _required_text(row, "definition")
    metric_kind_text = _required_text(row, "metric_kind")
    geography_level_text = _required_text(row, "geography_level")
    geography_name = _required_text(row, "geography_name")
    source_publisher = _required_text(row, "source_publisher")
    status_text = _required_text(row, "verification_status")

    if metric_kind_text not in _METRIC_KINDS:
        raise _RowValidationError(
            "metric_kind", "unsupported_metric_kind", "Unsupported metric_kind."
        )
    if geography_level_text not in _GEOGRAPHY_LEVELS:
        raise _RowValidationError(
            "geography_level", "unsupported_geography", "Unsupported geography_level."
        )
    if status_text == "verified":
        raise _RowValidationError(
            "verification_status",
            "manual_verification_required",
            "Uploaded files cannot mark evidence verified; use needs_review until a separate review.",
        )
    if status_text not in _IMPORTABLE_STATUSES:
        raise _RowValidationError(
            "verification_status",
            "unsupported_verification_status",
            "Imported evidence must be needs_review, stale or synthetic_demo.",
        )

    metric_kind = cast(MetricKind, metric_kind_text)
    geography_level = cast(GeographyLevel, geography_level_text)
    verification_status = cast(VerificationStatus, status_text)

    provider_id = _text(row, "provider_id")
    if geography_level == "provider" and provider_id is None:
        raise _RowValidationError(
            "provider_id", "provider_id_required", "Provider-level evidence requires provider_id."
        )
    if geography_level != "provider" and provider_id is not None:
        raise _RowValidationError(
            "provider_id",
            "provider_scope_mismatch",
            "provider_id is allowed only when geography_level is provider.",
        )

    source_url = _text(row, "source_url")
    source_page_or_table = _text(row, "source_page_or_table")
    if source_url is None and source_page_or_table is None:
        raise _RowValidationError(
            "source_url",
            "source_reference_required",
            "Provide source_url or source_page_or_table for provenance.",
        )
    if source_url is not None:
        try:
            parsed_url = urlsplit(source_url)
        except ValueError as exc:
            raise _RowValidationError(
                "source_url", "invalid_source_url", "source_url is malformed."
            ) from exc
        if (
            parsed_url.scheme not in {"http", "https"}
            or not parsed_url.netloc
            or parsed_url.username is not None
            or parsed_url.password is not None
        ):
            raise _RowValidationError(
                "source_url",
                "invalid_source_url",
                "source_url must be an HTTP(S) URL without embedded credentials.",
            )

    value_decimal = _optional_decimal(row, "value")
    numerator = _optional_integer(row, "numerator")
    denominator = _optional_integer(row, "denominator")
    sample_size = _optional_integer(row, "sample_size")
    unit = _text(row, "unit")
    derived_rate = False
    source_rate_without_counts = False

    if metric_kind == "rate":
        if unit is not None and unit.casefold() not in {"percent", "%"}:
            raise _RowValidationError(
                "unit", "rate_unit_mismatch", "Rate values must use percent or % as the unit."
            )
        if (numerator is None) != (denominator is None):
            raise _RowValidationError(
                "denominator",
                "incomplete_rate_counts",
                "numerator and denominator must both be supplied or both remain unknown.",
            )
        if numerator is not None and denominator is not None:
            if numerator < 0 or denominator <= 0 or numerator > denominator:
                raise _RowValidationError(
                    "numerator",
                    "invalid_rate_counts",
                    "Rate counts require 0 <= numerator <= denominator and denominator > 0.",
                )
            calculated = Decimal(numerator) * Decimal("100") / Decimal(denominator)
            if value_decimal is None:
                value_decimal = calculated
                unit = unit or "percent"
                derived_rate = True
            elif abs(value_decimal - calculated) > RATE_RECONCILIATION_TOLERANCE:
                raise _RowValidationError(
                    "value",
                    "rate_count_mismatch",
                    "Published rate differs from numerator/denominator by more than "
                    f"{RATE_RECONCILIATION_TOLERANCE} percentage points.",
                )
        elif value_decimal is not None:
            source_rate_without_counts = True
        if value_decimal is not None and unit is None:
            unit = "percent"
    elif numerator is not None or denominator is not None:
        raise _RowValidationError(
            "numerator",
            "counts_only_for_rates",
            "numerator and denominator are reserved for rate metrics.",
        )

    statistic_text = _text(row, "statistic_type") or "unknown"
    if statistic_text not in _STATISTIC_TYPES:
        raise _RowValidationError(
            "statistic_type", "unsupported_statistic", "Unsupported statistic_type."
        )
    statistic_type = cast(StatisticType, statistic_text)

    currency = _text(row, "currency")
    source_publication_date = _optional_date(row, "source_publication_date")
    last_verified_at = _optional_date(row, "last_verified_at")
    if metric_kind == "earnings" and value_decimal is not None:
        if not currency or not unit or statistic_type == "unknown":
            raise _RowValidationError(
                "currency",
                "incomplete_earnings_semantics",
                "Numeric earnings require currency, unit and mean/median/band statistic_type.",
            )

    try:
        record = OutcomeEvidenceRecord(
            evidence_id=evidence_id,
            metric_code=metric_code,
            metric_label=metric_label,
            definition=definition,
            metric_kind=metric_kind,
            value=None if value_decimal is None else float(value_decimal),
            geography_level=geography_level,
            geography_name=geography_name,
            trade_or_job_role=_text(row, "trade_or_job_role"),
            provider_id=provider_id,
            state=_text(row, "state"),
            district=_text(row, "district"),
            numerator=numerator,
            denominator=denominator,
            sample_size=sample_size,
            cohort_period=_text(row, "cohort_period"),
            observation_period=_text(row, "observation_period"),
            currency=currency,
            unit=unit,
            statistic_type=statistic_type,
            follow_up_period=_text(row, "follow_up_period"),
            source_publisher=source_publisher,
            source_url=source_url,
            source_publication_date=source_publication_date,
            source_page_or_table=source_page_or_table,
            methodology=_text(row, "methodology"),
            last_verified_at=last_verified_at,
            verification_status=verification_status,
        )
    except ValueError as exc:
        raise _RowValidationError("record", "domain_validation", str(exc)) from exc

    warnings: list[tuple[str, str]] = []
    if record.value is None:
        warnings.append(("value", "Metric value is not supplied and remains unknown."))
    if record.cohort_period is None:
        warnings.append(("cohort_period", "Cohort period is not supplied; keep cohort scope unknown."))
    if record.observation_period is None:
        warnings.append(
            ("observation_period", "Observation period is not supplied; do not infer recency.")
        )
    if record.sample_size is None:
        warnings.append(("sample_size", "Sample size is not supplied."))
    if record.follow_up_period is None:
        warnings.append(("follow_up_period", "Follow-up period is not supplied."))
    if source_rate_without_counts:
        warnings.append(
            ("numerator", "Only a source-reported percentage is available; counts are unknown.")
        )
    if derived_rate:
        warnings.append(
            ("value", "Percentage derived from the supplied numerator and denominator.")
        )

    return record, derived_rate, tuple(warnings)


def parse_outcome_csv(
    file_bytes: bytes,
    *,
    dataset_id: str,
    dataset_version: str,
    source_filename: str,
    imported_at: datetime | None = None,
) -> OutcomeImportReport:
    """Validate one canonical UTF-8 CSV without writing to any repository or database.

    The CSV schema is deliberately strict. The organiser's eventual SIH schema must be
    mapped explicitly after its data dictionary is received; this parser does not guess
    column names or silently discard unknown columns.
    """
    if not dataset_id.strip() or not dataset_version.strip():
        raise ValueError("dataset_id and dataset_version must be nonblank.")
    if not isinstance(file_bytes, bytes):
        raise TypeError("file_bytes must be bytes.")
    timestamp = _normalise_imported_at(imported_at)
    filename = _safe_filename(source_filename)
    digest = hashlib.sha256(file_bytes).hexdigest()
    findings: list[ImportFinding] = []
    records: list[OutcomeEvidenceRecord] = []
    derived_ids: list[str] = []
    row_count = 0

    def report() -> OutcomeImportReport:
        return OutcomeImportReport(
            dataset_id=dataset_id.strip(),
            dataset_version=dataset_version.strip(),
            source_filename=filename,
            source_sha256=digest,
            imported_at=timestamp,
            row_count=row_count,
            records=tuple(records),
            findings=tuple(findings),
            derived_rate_evidence_ids=tuple(derived_ids),
        )

    if len(file_bytes) > MAX_IMPORT_BYTES:
        findings.append(
            ImportFinding(
                1, "error", "file_too_large",
                f"CSV exceeds the {MAX_IMPORT_BYTES}-byte import limit.",
            )
        )
        return report()
    if not file_bytes:
        findings.append(ImportFinding(1, "error", "empty_file", "CSV file is empty."))
        return report()

    try:
        decoded = file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        findings.append(
            ImportFinding(1, "error", "invalid_encoding", "CSV must be valid UTF-8.")
        )
        return report()

    reader = csv.reader(io.StringIO(decoded, newline=""), strict=True)
    try:
        raw_header = next(reader, None)
        if raw_header is None:
            findings.append(ImportFinding(1, "error", "missing_header", "CSV header is missing."))
            return report()
        header = [column.strip() for column in raw_header]
        if any(not column for column in header):
            findings.append(
                ImportFinding(1, "error", "blank_header", "CSV headers cannot be blank.")
            )
        if len(header) != len(set(header)):
            findings.append(
                ImportFinding(1, "error", "duplicate_header", "CSV headers must be unique.")
            )
        missing = sorted(_REQUIRED_COLUMNS - set(header))
        unknown = sorted(set(header) - _ALLOWED_COLUMNS)
        for column in missing:
            findings.append(
                ImportFinding(
                    1, "error", "missing_required_header",
                    f"Required CSV column {column} is missing.", column,
                )
            )
        for column in unknown:
            findings.append(
                ImportFinding(
                    1, "error", "unknown_header",
                    f"Unknown CSV column {column}; add an explicit mapping before importing.",
                    column,
                )
            )
        if not ({"source_url", "source_page_or_table"} & set(header)):
            findings.append(
                ImportFinding(
                    1, "error", "source_reference_header_missing",
                    "Include source_url or source_page_or_table in the canonical CSV header.",
                )
            )
        if findings:
            return report()

        seen_ids: set[str] = set()
        for cells in reader:
            row_number = reader.line_num
            if not cells or all(not cell.strip() for cell in cells):
                continue
            row_count += 1
            if row_count > MAX_IMPORT_ROWS:
                findings.append(
                    ImportFinding(
                        row_number, "error", "row_limit_exceeded",
                        f"CSV exceeds the {MAX_IMPORT_ROWS}-row import limit.",
                    )
                )
                break
            if len(cells) != len(header):
                findings.append(
                    ImportFinding(
                        row_number, "error", "row_width_mismatch",
                        f"Expected {len(header)} cells but received {len(cells)}.",
                    )
                )
                continue
            row = dict(zip(header, cells, strict=True))
            raw_evidence_id = row.get("evidence_id", "").strip()
            if raw_evidence_id and raw_evidence_id in seen_ids:
                findings.append(
                    ImportFinding(
                        row_number, "error", "duplicate_evidence_id",
                        f"Duplicate evidence_id {raw_evidence_id}.", "evidence_id",
                    )
                )
                continue
            if raw_evidence_id:
                seen_ids.add(raw_evidence_id)
            try:
                record, derived, row_warnings = _build_record(row)
            except _RowValidationError as exc:
                findings.append(
                    ImportFinding(
                        row_number, "error", exc.code, str(exc), exc.field_name
                    )
                )
                continue
            records.append(record)
            if derived:
                derived_ids.append(record.evidence_id)
            for field_name, message in row_warnings:
                if field_name == "value" and derived:
                    code = "rate_derived"
                elif field_name == "numerator":
                    code = "rate_counts_unavailable"
                else:
                    code = "missing_context"
                findings.append(
                    ImportFinding(row_number, "warning", code, message, field_name)
                )
    except csv.Error as exc:
        findings.append(
            ImportFinding(
                max(reader.line_num, 1), "error", "malformed_csv",
                f"CSV parsing failed: {exc}",
            )
        )

    return report()
