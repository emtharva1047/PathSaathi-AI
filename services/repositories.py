"""Storage-independent repository contracts and query filters."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from core.domain import CourseRecord, OutcomeEvidenceRecord, VerificationStatus


@dataclass(frozen=True, slots=True)
class CourseQuery:
    """Exact, explainable filters for a course catalogue search."""

    state: str | None = None
    district: str | None = None
    trade: str | None = None
    provider_id: str | None = None
    min_nsqf_level: int | None = None
    max_nsqf_level: int | None = None
    limit: int | None = None
    offset: int = 0

    def __post_init__(self) -> None:
        if self.min_nsqf_level is not None and not 1 <= self.min_nsqf_level <= 10:
            raise ValueError("min_nsqf_level must be between 1 and 10.")
        if self.max_nsqf_level is not None and not 1 <= self.max_nsqf_level <= 10:
            raise ValueError("max_nsqf_level must be between 1 and 10.")
        if (
            self.min_nsqf_level is not None
            and self.max_nsqf_level is not None
            and self.min_nsqf_level > self.max_nsqf_level
        ):
            raise ValueError("min_nsqf_level cannot exceed max_nsqf_level.")
        if self.limit is not None and not 1 <= self.limit <= 100:
            raise ValueError("limit must be between 1 and 100.")
        if self.offset < 0:
            raise ValueError("offset cannot be negative.")


@dataclass(frozen=True, slots=True)
class OutcomeQuery:
    """Exact filters that preserve the source's geography and cohort granularity."""

    metric_code: str | None = None
    trade_or_job_role: str | None = None
    provider_id: str | None = None
    state: str | None = None
    district: str | None = None
    verification_status: VerificationStatus | None = None
    limit: int | None = None
    offset: int = 0

    def __post_init__(self) -> None:
        if self.verification_status is not None and self.verification_status not in {
            "verified",
            "needs_review",
            "stale",
            "synthetic_demo",
        }:
            raise ValueError("Unsupported outcome verification status filter.")
        if self.limit is not None and not 1 <= self.limit <= 100:
            raise ValueError("limit must be between 1 and 100.")
        if self.offset < 0:
            raise ValueError("offset cannot be negative.")


class CourseRepository(Protocol):
    """Read contract for qualification/course catalogue implementations."""

    def list_courses(self, query: CourseQuery | None = None) -> tuple[CourseRecord, ...]:
        """Return records matching all supplied filters."""
        ...

    def get_course(self, course_id: str) -> CourseRecord | None:
        """Return one course by stable identifier, or None when absent."""
        ...


class OutcomeEvidenceRepository(Protocol):
    """Read contract for provenance-aware outcome evidence implementations."""

    def list_outcomes(
        self,
        query: OutcomeQuery | None = None,
    ) -> tuple[OutcomeEvidenceRecord, ...]:
        """Return evidence matching all supplied filters."""
        ...

    def get_outcome(self, evidence_id: str) -> OutcomeEvidenceRecord | None:
        """Return one evidence record by stable identifier, or None when absent."""
        ...
