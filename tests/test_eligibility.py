"""Tests for source-backed, three-state qualification eligibility."""

from datetime import date

import pytest

from core.eligibility import (
    CriteriaVerificationStatus,
    EligibilityStatus,
    QualificationEntryCriteria,
    evaluate_eligibility,
)
from core.profiles import EducationLevel, LearnerProfile


def verified_criteria() -> QualificationEntryCriteria:
    return QualificationEntryCriteria(
        qualification_code="QF-TEST-01",
        accepted_education_levels=frozenset({EducationLevel.GRADE_10, EducationLevel.GRADE_12}),
        source_publisher="Synthetic test awarding body",
        source_url="https://example.org/qualification/QF-TEST-01",
        last_verified_at=date(2026, 11, 14),
        verification_status=CriteriaVerificationStatus.VERIFIED,
    )


def test_verified_matching_education_is_eligible_with_source_caveat() -> None:
    learner = LearnerProfile(learner_ref="learner_10", education_level=EducationLevel.GRADE_10)

    result = evaluate_eligibility(learner, verified_criteria())

    assert result.status == EligibilityStatus.ELIGIBLE
    assert result.qualification_code == "QF-TEST-01"
    assert result.source_url == "https://example.org/qualification/QF-TEST-01"
    assert result.admission_decision is False
    assert result.scope == "education_requirement_only"
    assert "Other entry conditions" in result.explanation


def test_verified_non_matching_education_is_ineligible_for_this_criterion() -> None:
    learner = LearnerProfile(learner_ref="learner_11", education_level=EducationLevel.GRADE_8)

    result = evaluate_eligibility(learner, verified_criteria())

    assert result.status == EligibilityStatus.INELIGIBLE
    assert result.reason_code == "published_education_requirement_not_met"
    assert "Confirm equivalence" in result.explanation


def test_unknown_learner_education_remains_unknown() -> None:
    learner = LearnerProfile(learner_ref="learner_12")

    result = evaluate_eligibility(learner, verified_criteria())

    assert result.status == EligibilityStatus.UNKNOWN
    assert result.reason_code == "learner_education_unknown"
    assert result.missing_information == ("learner's highest completed education level",)


def test_missing_qualification_criteria_remains_unknown() -> None:
    learner = LearnerProfile(learner_ref="learner_13", education_level=EducationLevel.GRADE_12)

    result = evaluate_eligibility(learner, None)

    assert result.status == EligibilityStatus.UNKNOWN
    assert result.reason_code == "criteria_not_available"


def test_unverified_criteria_cannot_produce_eligible_or_ineligible() -> None:
    learner = LearnerProfile(learner_ref="learner_14", education_level=EducationLevel.GRADE_10)
    criteria = QualificationEntryCriteria(
        qualification_code="QF-TEST-02",
        accepted_education_levels=frozenset({EducationLevel.GRADE_10}),
        verification_status=CriteriaVerificationStatus.NEEDS_REVIEW,
    )

    result = evaluate_eligibility(learner, criteria)

    assert result.status == EligibilityStatus.UNKNOWN
    assert result.reason_code == "criteria_not_verified"


def test_stale_criteria_cannot_be_used_for_eligibility() -> None:
    learner = LearnerProfile(learner_ref="learner_15", education_level=EducationLevel.GRADE_10)
    criteria = QualificationEntryCriteria(
        qualification_code="QF-TEST-03",
        accepted_education_levels=frozenset({EducationLevel.GRADE_10}),
        source_publisher="Synthetic test awarding body",
        source_url="https://example.org/qualification/QF-TEST-03",
        last_verified_at=date(2025, 1, 1),
        verification_status=CriteriaVerificationStatus.STALE,
    )

    assert evaluate_eligibility(learner, criteria).status == EligibilityStatus.UNKNOWN


def test_verified_criteria_requires_source_and_accepted_levels() -> None:
    with pytest.raises(ValueError, match="complete source provenance"):
        QualificationEntryCriteria(
            qualification_code="QF-TEST-04",
            accepted_education_levels=frozenset({EducationLevel.GRADE_10}),
            verification_status=CriteriaVerificationStatus.VERIFIED,
        )


def test_unknown_cannot_be_declared_as_an_accepted_education_level() -> None:
    with pytest.raises(ValueError, match="UNKNOWN cannot be an accepted"):
        QualificationEntryCriteria(
            qualification_code="QF-TEST-05",
            accepted_education_levels=frozenset({EducationLevel.UNKNOWN}),
        )


def test_invalid_source_url_is_rejected() -> None:
    with pytest.raises(ValueError, match=r"absolute HTTP\(S\) URL"):
        QualificationEntryCriteria(
            qualification_code="QF-TEST-06",
            accepted_education_levels=frozenset({EducationLevel.GRADE_10}),
            source_url="javascript:alert(1)",
        )
