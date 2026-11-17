"""Provenance-gated, deterministic qualification and NSQF explainers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum
from urllib.parse import urlsplit

from core.domain import CourseRecord, VerificationStatus, normalize_nsqf_level


class QualificationRecordStatus(StrEnum):
    CURRENT = "current"
    EXPIRED = "expired"
    ARCHIVED = "archived"
    UNKNOWN = "unknown"


class ExplainerStatus(StrEnum):
    CURRENT = "current"
    PARTIAL = "partial"
    EXPIRED = "expired"
    ARCHIVED = "archived"
    UNKNOWN = "unknown"


class QualificationFactKind(StrEnum):
    JOB_DESCRIPTION = "job_description"
    ENTRY_ROUTE = "entry_route"
    MINIMUM_AGE = "minimum_age"
    TRAINING_DURATION = "training_duration"
    LEARNING_MODULE = "learning_module"
    PROGRESSION = "progression"


@dataclass(frozen=True, slots=True)
class QualificationFact:
    """One bilingual claim tied to a specific section of an official source."""

    fact_id: str
    kind: QualificationFactKind
    text_en: str
    text_mr: str
    source_publisher: str | None = None
    source_url: str | None = None
    source_reference: str | None = None
    source_publication_date: date | None = None
    last_verified_at: date | None = None
    verification_status: VerificationStatus = "needs_review"
    related_qualification_title: str | None = None
    related_nsqf_level: Decimal | None = None

    def __post_init__(self) -> None:
        for field_name in ("fact_id", "text_en", "text_mr"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} cannot be empty.")
            object.__setattr__(self, field_name, value.strip())

        if self.verification_status not in {
            "verified",
            "needs_review",
            "stale",
            "synthetic_demo",
        }:
            raise ValueError("Unsupported qualification fact verification status.")

        for field_name in ("source_publisher", "source_reference", "source_url"):
            value = getattr(self, field_name)
            if value is not None:
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"{field_name} cannot be blank when supplied.")
                object.__setattr__(self, field_name, value.strip())

        if self.source_url is not None:
            parsed = urlsplit(self.source_url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError("Qualification fact source URLs must use HTTP or HTTPS.")

        if self.verification_status == "verified" and not all(
            (self.source_publisher, self.source_url, self.source_reference, self.last_verified_at)
        ):
            raise ValueError(
                "Verified qualification facts require publisher, URL, source section and verification date."
            )

        if self.kind == QualificationFactKind.PROGRESSION:
            if not self.related_qualification_title or not self.related_qualification_title.strip():
                raise ValueError("Progression facts require a related qualification title.")
            object.__setattr__(
                self, "related_qualification_title", self.related_qualification_title.strip()
            )
            object.__setattr__(
                self, "related_nsqf_level", normalize_nsqf_level(self.related_nsqf_level)
            )
        elif self.related_qualification_title is not None or self.related_nsqf_level is not None:
            raise ValueError("Related qualification fields are only valid for progression facts.")


@dataclass(frozen=True, slots=True)
class QualificationExplainerRecord:
    """A curated qualification record with explicit NQR state and claim-level provenance."""

    course: CourseRecord
    record_status: QualificationRecordStatus
    valid_until: date | None
    facts: tuple[QualificationFact, ...]
    nqr_record_url: str | None = None
    record_source_publisher: str | None = None
    record_last_verified_at: date | None = None
    marathi_translation_reviewed: bool = False

    def __post_init__(self) -> None:
        if not self.course.qualification_code or not self.course.qualification_code.strip():
            raise ValueError("Qualification explainers require an exact qualification code.")
        status = QualificationRecordStatus(self.record_status)
        object.__setattr__(self, "record_status", status)
        facts = tuple(self.facts)
        identifiers = [fact.fact_id for fact in facts]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("Qualification fact identifiers must be unique.")
        object.__setattr__(self, "facts", facts)
        if self.nqr_record_url is not None:
            parsed = urlsplit(self.nqr_record_url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError("NQR record URLs must use HTTP or HTTPS.")
        if status == QualificationRecordStatus.CURRENT and not all(
            (self.nqr_record_url, self.record_source_publisher, self.record_last_verified_at)
        ):
            raise ValueError(
                "Current NQR records require a record URL, publisher and verification date."
            )


@dataclass(frozen=True, slots=True)
class QualificationExplainerView:
    """Only source-verified claims from a current record are exposed to the UI."""

    record: QualificationExplainerRecord
    status: ExplainerStatus
    visible_facts: tuple[QualificationFact, ...]
    withheld_fact_count: int

    @property
    def course(self) -> CourseRecord:
        return self.record.course


def build_qualification_explainer(
    record: QualificationExplainerRecord,
    *,
    as_of: date | None = None,
) -> QualificationExplainerView:
    """Withhold claims from unknown, expired, archived or unverified records."""
    today = as_of or date.today()

    if record.record_status == QualificationRecordStatus.ARCHIVED:
        status = ExplainerStatus.ARCHIVED
        visible_facts: tuple[QualificationFact, ...] = ()
    elif (
        record.record_status == QualificationRecordStatus.EXPIRED
        or (record.valid_until is not None and record.valid_until < today)
    ):
        status = ExplainerStatus.EXPIRED
        visible_facts = ()
    elif (
        record.record_status != QualificationRecordStatus.CURRENT
        or not record.course.has_verified_source
        or record.course.last_verified_at is None
        or record.course.last_verified_at > today
        or not record.nqr_record_url
        or not record.record_source_publisher
        or record.record_last_verified_at is None
        or record.record_last_verified_at > today
    ):
        status = ExplainerStatus.UNKNOWN
        visible_facts = ()
    else:
        visible_facts = tuple(
            fact
            for fact in record.facts
            if fact.verification_status == "verified"
            and fact.source_publisher
            and fact.source_url
            and fact.source_reference
            and fact.last_verified_at is not None
            and fact.last_verified_at <= today
        )
        if not visible_facts:
            status = ExplainerStatus.UNKNOWN
        elif len(visible_facts) < len(record.facts):
            status = ExplainerStatus.PARTIAL
        else:
            status = ExplainerStatus.CURRENT

    return QualificationExplainerView(
        record=record,
        status=status,
        visible_facts=visible_facts,
        withheld_fact_count=len(record.facts) - len(visible_facts),
    )
