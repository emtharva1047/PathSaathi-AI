"""Deterministic, source-backed qualification eligibility evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from urllib.parse import urlsplit

from core.profiles import EducationLevel, LearnerProfile


class EligibilityStatus(StrEnum):
    ELIGIBLE = "eligible"
    INELIGIBLE = "ineligible"
    UNKNOWN = "unknown"


class CriteriaVerificationStatus(StrEnum):
    VERIFIED = "verified"
    NEEDS_REVIEW = "needs_review"
    STALE = "stale"


@dataclass(frozen=True, slots=True)
class QualificationEntryCriteria:
    """Normalized accepted education levels copied from a cited qualification source."""

    qualification_code: str
    accepted_education_levels: frozenset[EducationLevel] | None = None
    source_publisher: str | None = None
    source_url: str | None = None
    last_verified_at: date | None = None
    verification_status: CriteriaVerificationStatus = CriteriaVerificationStatus.NEEDS_REVIEW

    def __post_init__(self) -> None:
        qualification_code = self.qualification_code.strip()
        if not qualification_code:
            raise ValueError("qualification_code cannot be empty.")
        object.__setattr__(self, "qualification_code", qualification_code)
        if self.accepted_education_levels is not None:
            levels = frozenset(self.accepted_education_levels)
            if not levels:
                raise ValueError("accepted_education_levels cannot be empty when specified.")
            if any(not isinstance(level, EducationLevel) for level in levels):
                raise ValueError("accepted_education_levels must use normalized education values.")
            if EducationLevel.UNKNOWN in levels:
                raise ValueError("UNKNOWN cannot be an accepted qualification entry level.")
            object.__setattr__(self, "accepted_education_levels", levels)
        if self.source_url is not None:
            parsed = urlsplit(self.source_url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError("source_url must be an absolute HTTP(S) URL.")
        if self.verification_status == CriteriaVerificationStatus.VERIFIED:
            if (
                self.accepted_education_levels is None
                or not self.source_publisher
                or not self.source_url
                or self.last_verified_at is None
            ):
                raise ValueError(
                    "Verified entry criteria require accepted levels and complete "
                    "source provenance."
                )

    @property
    def has_verified_criteria(self) -> bool:
        return (
            self.verification_status == CriteriaVerificationStatus.VERIFIED
            and self.accepted_education_levels is not None
            and bool(self.source_publisher)
            and bool(self.source_url)
            and self.last_verified_at is not None
        )


@dataclass(frozen=True, slots=True)
class EligibilityResult:
    """An explainable result scoped only to the published education requirement."""

    status: EligibilityStatus
    reason_code: str
    explanation: str
    qualification_code: str | None = None
    missing_information: tuple[str, ...] = ()
    source_publisher: str | None = None
    source_url: str | None = None
    last_verified_at: date | None = None
    scope: str = "education_requirement_only"
    admission_decision: bool = False


def evaluate_eligibility(
    learner: LearnerProfile,
    criteria: QualificationEntryCriteria | None,
) -> EligibilityResult:
    """Evaluate one explicitly sourced education criterion without guessing missing facts."""
    if criteria is None:
        return EligibilityResult(
            status=EligibilityStatus.UNKNOWN,
            reason_code="criteria_not_available",
            explanation="Published entry criteria are not available for this qualification.",
            missing_information=("official qualification entry criteria",),
        )

    if not criteria.has_verified_criteria:
        return EligibilityResult(
            status=EligibilityStatus.UNKNOWN,
            reason_code="criteria_not_verified",
            qualification_code=criteria.qualification_code,
            explanation="Entry criteria are not sufficiently verified to assess eligibility.",
            missing_information=("verified qualification source",),
            source_publisher=criteria.source_publisher,
            source_url=criteria.source_url,
            last_verified_at=criteria.last_verified_at,
        )

    if learner.education_level == EducationLevel.UNKNOWN:
        return EligibilityResult(
            status=EligibilityStatus.UNKNOWN,
            reason_code="learner_education_unknown",
            qualification_code=criteria.qualification_code,
            explanation="The learner's highest completed education level has not been recorded.",
            missing_information=("learner's highest completed education level",),
            source_publisher=criteria.source_publisher,
            source_url=criteria.source_url,
            last_verified_at=criteria.last_verified_at,
        )

    if learner.education_level in criteria.accepted_education_levels:
        return EligibilityResult(
            status=EligibilityStatus.ELIGIBLE,
            reason_code="published_education_requirement_met",
            qualification_code=criteria.qualification_code,
            explanation=(
                "The recorded education level matches the published education requirement. "
                "Other entry conditions and the provider's admission decision may still apply."
            ),
            source_publisher=criteria.source_publisher,
            source_url=criteria.source_url,
            last_verified_at=criteria.last_verified_at,
        )

    return EligibilityResult(
        status=EligibilityStatus.INELIGIBLE,
        reason_code="published_education_requirement_not_met",
        qualification_code=criteria.qualification_code,
        explanation=(
            "The recorded education level is not in the published accepted list. "
            "Confirm equivalence with the awarding body or provider before ruling out this pathway."
        ),
        source_publisher=criteria.source_publisher,
        source_url=criteria.source_url,
        last_verified_at=criteria.last_verified_at,
    )
