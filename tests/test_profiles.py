"""Tests for privacy-conscious learner and parent profile records."""

import pytest

from core.profiles import (
    ConcernCategory,
    EducationLevel,
    FamilyCounsellingContext,
    LearnerProfile,
    ParentContext,
    PreferredLanguage,
)


def test_family_context_preserves_learner_and_parent_preferences_separately() -> None:
    learner = LearnerProfile(
        learner_ref="learner_01",
        education_level=EducationLevel.GRADE_10,
        interests=("electronics", "repair work"),
        work_preferences=("hands-on",),
        preferred_language=PreferredLanguage.MARATHI,
    )
    parent = ParentContext(
        participant_ref="parent_01",
        concerns=(ConcernCategory.WORKPLACE_SAFETY, ConcernCategory.INCOME),
        priorities=("safe workplace", "stable income"),
    )

    context = FamilyCounsellingContext(learner=learner, parent=parent)

    assert context.learner.interests == ("electronics", "repair work")
    assert context.learner.work_preferences == ("hands-on",)
    assert context.parent.priorities == ("safe workplace", "stable income")
    assert context.parent.concerns == (ConcernCategory.WORKPLACE_SAFETY, ConcernCategory.INCOME)
    assert context.learner.preferred_language == PreferredLanguage.MARATHI


def test_profile_defaults_to_unknown_education_and_optional_location() -> None:
    profile = LearnerProfile(learner_ref="learner_02")

    assert profile.education_level == EducationLevel.UNKNOWN
    assert profile.state_code is None
    assert profile.district_code is None
    assert profile.household_income_band_code is None


def test_profile_rejects_exact_income_amount_in_band_field() -> None:
    with pytest.raises(ValueError, match="broad band code"):
        LearnerProfile(learner_ref="learner_03", household_income_band_code="25000")


def test_profile_rejects_contact_like_identifier() -> None:
    with pytest.raises(ValueError, match="opaque reference"):
        LearnerProfile(learner_ref="learner@example.com")


def test_profile_normalises_and_rejects_duplicate_preferences() -> None:
    profile = LearnerProfile(
        learner_ref="learner_04",
        interests=("  electronics  ",),
        work_preferences=("hands-on",),
    )

    assert profile.interests == ("electronics",)
    with pytest.raises(ValueError, match="duplicate"):
        LearnerProfile(learner_ref="learner_05", interests=("Repair", "repair"))


def test_family_context_rejects_same_participant_reference() -> None:
    learner = LearnerProfile(learner_ref="participant_01")
    parent = ParentContext(participant_ref="participant_01")

    with pytest.raises(ValueError, match="distinct participant references"):
        FamilyCounsellingContext(learner=learner, parent=parent)


def test_profile_accepts_region_codes_and_rejects_an_exact_address() -> None:
    profile = LearnerProfile(
        learner_ref="learner_06",
        state_code="MH",
        district_code="THANE",
    )
    assert profile.state_code == "MH"
    assert profile.district_code == "THANE"

    with pytest.raises(ValueError, match="normalized broad-region code"):
        LearnerProfile(learner_ref="learner_07", district_code="Flat 12, Road 4")
