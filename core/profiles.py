"""Privacy-conscious learner and parent context records for counselling."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum


class EducationLevel(StrEnum):
    """Normalized education levels; equivalence must be source-reviewed."""

    BELOW_GRADE_8 = "below_grade_8"
    GRADE_8 = "grade_8"
    GRADE_10 = "grade_10"
    GRADE_12 = "grade_12"
    ITI_OR_VOCATIONAL = "iti_or_vocational"
    DIPLOMA = "diploma"
    GRADUATE = "graduate"
    OTHER = "other"
    UNKNOWN = "unknown"


class ConcernCategory(StrEnum):
    """Parent-reported concern categories; these are not inferred from text."""

    INCOME = "income"
    PLACEMENT_AND_JOB_SECURITY = "placement_and_job_security"
    WORKPLACE_SAFETY = "workplace_safety"
    SOCIAL_PERCEPTION = "social_perception"
    AFFORDABILITY = "affordability"
    PROGRESSION = "progression"
    OTHER = "other"


class PreferredLanguage(StrEnum):
    ENGLISH = "en"
    MARATHI = "mr"


_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,63}$")
_REGION_CODE_PATTERN = re.compile(r"^[A-Z][A-Z0-9_-]{0,15}$")
_BAND_CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_-]{0,31}$")


def _validate_identifier(value: str, field_name: str) -> None:
    if not _IDENTIFIER_PATTERN.fullmatch(value):
        raise ValueError(
            f"{field_name} must be an opaque reference (1-64 letters, digits, '_' or '-')."
        )


def _normalise_text_items(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if len(values) > 12:
        raise ValueError(f"{field_name} cannot contain more than 12 items.")
    cleaned = tuple(value.strip() for value in values)
    if any(not value for value in cleaned):
        raise ValueError(f"{field_name} cannot contain blank items.")
    if any(len(value) > 100 for value in cleaned):
        raise ValueError(f"{field_name} items cannot exceed 100 characters.")
    if len({value.casefold() for value in cleaned}) != len(cleaned):
        raise ValueError(f"{field_name} cannot contain duplicate items.")
    return cleaned


@dataclass(frozen=True, slots=True)
class LearnerProfile:
    """Minimal learner context; never store a name, exact address or exact income."""

    learner_ref: str
    education_level: EducationLevel = EducationLevel.UNKNOWN
    state_code: str | None = None
    district_code: str | None = None
    household_income_band_code: str | None = None
    interests: tuple[str, ...] = ()
    work_preferences: tuple[str, ...] = ()
    preferred_language: PreferredLanguage = PreferredLanguage.ENGLISH

    def __post_init__(self) -> None:
        _validate_identifier(self.learner_ref, "learner_ref")
        if not isinstance(self.education_level, EducationLevel):
            raise ValueError("education_level must use a normalized EducationLevel value.")
        if not isinstance(self.preferred_language, PreferredLanguage):
            raise ValueError("preferred_language must be English or Marathi.")
        if self.state_code is not None and not _REGION_CODE_PATTERN.fullmatch(self.state_code):
            raise ValueError("state_code must be a normalized broad-region code.")
        if self.district_code is not None and not _REGION_CODE_PATTERN.fullmatch(
            self.district_code
        ):
            raise ValueError("district_code must be a normalized broad-region code.")
        if self.household_income_band_code is not None and not _BAND_CODE_PATTERN.fullmatch(
            self.household_income_band_code
        ):
            raise ValueError(
                "Income must be stored as a configured broad band code, not an amount."
            )
        object.__setattr__(self, "interests", _normalise_text_items(self.interests, "interests"))
        object.__setattr__(
            self,
            "work_preferences",
            _normalise_text_items(self.work_preferences, "work_preferences"),
        )


@dataclass(frozen=True, slots=True)
class ParentContext:
    """Parent/guardian perspective, kept separate from learner preferences."""

    participant_ref: str
    concerns: tuple[ConcernCategory, ...] = ()
    priorities: tuple[str, ...] = ()
    preferred_language: PreferredLanguage = PreferredLanguage.ENGLISH

    def __post_init__(self) -> None:
        _validate_identifier(self.participant_ref, "participant_ref")
        if not isinstance(self.preferred_language, PreferredLanguage):
            raise ValueError("preferred_language must be English or Marathi.")
        if any(not isinstance(concern, ConcernCategory) for concern in self.concerns):
            raise ValueError("concerns must use supported parent-reported categories.")
        if len(set(self.concerns)) != len(self.concerns):
            raise ValueError("concerns cannot contain duplicates.")
        object.__setattr__(self, "priorities", _normalise_text_items(self.priorities, "priorities"))


@dataclass(frozen=True, slots=True)
class FamilyCounsellingContext:
    """A composition of distinct learner and parent records, not a merged profile."""

    learner: LearnerProfile
    parent: ParentContext

    def __post_init__(self) -> None:
        if self.learner.learner_ref == self.parent.participant_ref:
            raise ValueError("Learner and parent must have distinct participant references.")
