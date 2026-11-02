"""Typed domain records for qualification and outcome evidence.

These records are storage-independent. They deliberately preserve unknown values and
source provenance instead of manufacturing estimates for missing evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal
from urllib.parse import urlsplit

VerificationStatus = Literal["verified", "needs_review", "stale", "synthetic_demo"]
GeographyLevel = Literal["national", "state", "district", "provider"]
MetricKind = Literal["rate", "earnings", "count", "other"]
StatisticType = Literal["mean", "median", "band", "unknown"]


def _validate_source(
    verification_status: VerificationStatus,
    source_publisher: str | None,
    source_url: str | None,
    last_verified_at: date | None,
) -> None:
    """Require auditable provenance before a record can be marked verified."""
    if verification_status != "verified":
        return
    if not source_publisher or not source_url or last_verified_at is None:
        raise ValueError(
            "Verified records require a source publisher, source URL and verification date."
        )
    parsed = urlsplit(source_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Verified source URLs must use HTTP or HTTPS.")


@dataclass(frozen=True, slots=True)
class CourseRecord:
    """A qualification or course catalogue entry with explicit source status."""

    course_id: str
    title: str
    trade: str
    qualification_code: str | None = None
    awarding_body: str | None = None
    nsqf_level: int | None = None
    state: str | None = None
    district: str | None = None
    provider_id: str | None = None
    job_roles: tuple[str, ...] = ()
    entry_requirements: tuple[str, ...] = ()
    source_publisher: str | None = None
    source_url: str | None = None
    source_publication_date: date | None = None
    last_verified_at: date | None = None
    verification_status: VerificationStatus = "needs_review"

    def __post_init__(self) -> None:
        if not self.course_id.strip():
            raise ValueError("course_id cannot be empty.")
        if not self.title.strip():
            raise ValueError("title cannot be empty.")
        if not self.trade.strip():
            raise ValueError("trade cannot be empty.")
        if self.nsqf_level is not None and not 1 <= self.nsqf_level <= 10:
            raise ValueError("nsqf_level must be between 1 and 10, or unknown.")
        _validate_source(
            self.verification_status,
            self.source_publisher,
            self.source_url,
            self.last_verified_at,
        )

    @property
    def has_verified_source(self) -> bool:
        """Whether this course has a complete, verified source trail."""
        return (
            self.verification_status == "verified"
            and bool(self.source_publisher)
            and bool(self.source_url)
            and self.last_verified_at is not None
        )


@dataclass(frozen=True, slots=True)
class OutcomeEvidenceRecord:
    """One source-scoped outcome observation; unknown values remain None."""

    evidence_id: str
    metric_code: str
    metric_label: str
    definition: str
    metric_kind: MetricKind
    value: float | None
    geography_level: GeographyLevel
    geography_name: str
    trade_or_job_role: str | None = None
    provider_id: str | None = None
    state: str | None = None
    district: str | None = None
    numerator: int | None = None
    denominator: int | None = None
    sample_size: int | None = None
    cohort_period: str | None = None
    observation_period: str | None = None
    currency: str | None = None
    unit: str | None = None
    statistic_type: StatisticType = "unknown"
    follow_up_period: str | None = None
    source_publisher: str | None = None
    source_url: str | None = None
    source_publication_date: date | None = None
    source_page_or_table: str | None = None
    methodology: str | None = None
    last_verified_at: date | None = None
    verification_status: VerificationStatus = "needs_review"

    def __post_init__(self) -> None:
        for field_name in ("evidence_id", "metric_code", "metric_label", "definition"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} cannot be empty.")
        if not self.geography_name.strip():
            raise ValueError("geography_name cannot be empty.")
        if self.value is not None and self.metric_kind == "rate":
            if not 0 <= self.value <= 100:
                raise ValueError("Rate values must be expressed as percentages from 0 to 100.")
        if (self.numerator is None) != (self.denominator is None):
            raise ValueError("numerator and denominator must both be present or both be unknown.")
        if self.numerator is not None and self.denominator is not None:
            if self.numerator < 0 or self.denominator <= 0:
                raise ValueError("Rate counts require a non-negative numerator and positive denominator.")
            if self.numerator > self.denominator:
                raise ValueError("numerator cannot exceed denominator.")
        if self.sample_size is not None and self.sample_size < 0:
            raise ValueError("sample_size cannot be negative.")
        if self.metric_kind == "earnings" and self.value is not None:
            if not self.currency or not self.unit:
                raise ValueError("Earnings values require an explicit currency and unit.")
            if self.statistic_type == "unknown":
                raise ValueError("Earnings values require a mean, median or band statistic type.")
        _validate_source(
            self.verification_status,
            self.source_publisher,
            self.source_url,
            self.last_verified_at,
        )

    @property
    def is_verified_displayable(self) -> bool:
        """True only when a numeric value and complete verified provenance exist."""
        return (
            self.value is not None
            and self.verification_status == "verified"
            and bool(self.source_publisher)
            and bool(self.source_url)
            and self.last_verified_at is not None
        )
