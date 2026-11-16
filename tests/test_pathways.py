"""Tests for transparent, learner-led advisory pathway matching."""

from datetime import date

import pytest

from core.domain import CourseRecord
from core.eligibility import (
    CriteriaVerificationStatus,
    EligibilityStatus,
    QualificationEntryCriteria,
)
from core.pathways import (
    AdvisoryPathway,
    ShortlistState,
    build_pathway_shortlist,
)
from core.profiles import (
    ConcernCategory,
    EducationLevel,
    FamilyCounsellingContext,
    LearnerProfile,
    ParentContext,
)


def learner(
    *,
    interests: tuple[str, ...] = (),
    work_preferences: tuple[str, ...] = (),
    education_level: EducationLevel = EducationLevel.UNKNOWN,
) -> LearnerProfile:
    return LearnerProfile(
        learner_ref="learner_test",
        education_level=education_level,
        interests=interests,
        work_preferences=work_preferences,
    )


def pathway(
    course_id: str,
    *,
    interests: tuple[str, ...] = ("technology",),
    work_preferences: tuple[str, ...] = ("hands_on",),
    entry_criteria: QualificationEntryCriteria | None = None,
    verification_status: str = "synthetic_demo",
) -> AdvisoryPathway:
    course = CourseRecord(
        course_id=course_id,
        title=f"Illustrative {course_id}",
        trade="Illustrative trade",
        qualification_code=(
            entry_criteria.qualification_code if entry_criteria is not None else None
        ),
        source_publisher=(
            "Test fixture publisher" if verification_status == "verified" else None
        ),
        source_url=(
            "https://example.org/test-course" if verification_status == "verified" else None
        ),
        last_verified_at=date(2026, 1, 1) if verification_status == "verified" else None,
        verification_status=verification_status,
    )
    return AdvisoryPathway(
        course=course,
        display_title_mr=f"उदाहरण {course_id}",
        display_trade_mr="नमुना व्यवसाय",
        interest_tags=interests,
        work_preference_tags=work_preferences,
        entry_criteria=entry_criteria,
    )


def verified_criteria(
    accepted: frozenset[EducationLevel],
) -> QualificationEntryCriteria:
    return QualificationEntryCriteria(
        qualification_code="TEST-Q-001",
        accepted_education_levels=accepted,
        source_publisher="Test fixture publisher",
        source_url="https://example.org/test-qualification",
        last_verified_at=date(2026, 1, 1),
        verification_status=CriteriaVerificationStatus.VERIFIED,
    )


def test_matching_returns_exact_interest_and_work_reason_codes_in_both_languages() -> None:
    item = pathway(
        "demo-tech",
        entry_criteria=verified_criteria(frozenset({EducationLevel.GRADE_10})),
        verification_status="verified",
    )
    result = build_pathway_shortlist(
        learner(
            interests=("technology",),
            work_preferences=("hands_on",),
            education_level=EducationLevel.GRADE_10,
        ),
        (item,),
    )

    recommendation = result.shortlist[0]
    assert recommendation.reason_codes == (
        "interest:technology",
        "work_preference:hands_on",
    )
    assert recommendation.matched_interests == ("technology",)
    assert recommendation.matched_work_preferences == ("hands_on",)
    assert "interest: technology" in recommendation.explanation_en
    assert "आवड: तंत्रज्ञान" in recommendation.explanation_mr
    assert result.state == ShortlistState.MATCHES_AVAILABLE


def test_ties_use_stable_course_identifier_order_without_a_learner_score() -> None:
    items = (pathway("course-b"), pathway("course-a"))
    result = build_pathway_shortlist(
        learner(interests=("technology",)),
        items,
        max_shortlist=1,
    )

    assert result.needs_verification[0].pathway.course.course_id == "course-a"
    assert result.explore_all[0].pathway.course.course_id == "course-b"
    assert result.explore_all[0].matches_preferences is True
    assert len(result.all_options) == 2


def test_empty_profile_generates_no_shortlist_and_keeps_every_option_explorable() -> None:
    items = (pathway("course-a"), pathway("course-b"))
    result = build_pathway_shortlist(learner(), items)

    assert result.state == ShortlistState.NO_PREFERENCES
    assert result.shortlist == ()
    assert len(result.explore_all) == 2
    assert len(result.all_options) == 2
    assert all(item.eligibility.status == EligibilityStatus.UNKNOWN for item in result.all_options)
    assert all("No learner interests" in item.explanation_en for item in result.all_options)


def test_non_matching_preferences_do_not_hide_any_pathway() -> None:
    items = (pathway("course-a"), pathway("course-b", interests=("design_and_creativity",)))
    result = build_pathway_shortlist(
        learner(interests=("agriculture_and_nature",)),
        items,
    )

    assert result.state == ShortlistState.NO_MATCHES
    assert result.shortlist == ()
    assert len(result.explore_all) == 2
    assert all(not item.matches_preferences for item in result.all_options)


def test_synthetic_catalogue_items_never_claim_verified_eligibility_or_outcomes() -> None:
    result = build_pathway_shortlist(learner(interests=("technology",)), (pathway("demo"),))

    recommendation = result.needs_verification[0]
    assert recommendation.eligibility.status == EligibilityStatus.UNKNOWN
    assert recommendation.eligibility.reason_code == "criteria_not_available"
    assert recommendation.pathway.course.verification_status == "synthetic_demo"


def test_ineligible_education_result_does_not_override_preference_match() -> None:
    criteria = verified_criteria(frozenset({EducationLevel.GRADE_10}))
    item = pathway(
        "verified-course",
        entry_criteria=criteria,
        verification_status="verified",
    )
    result = build_pathway_shortlist(
        learner(
            interests=("technology",),
            education_level=EducationLevel.GRADE_8,
        ),
        (item,),
    )

    assert result.shortlist == ()
    assert result.explore_all[0].matches_preferences is True
    assert result.explore_all[0].eligibility.status == EligibilityStatus.INELIGIBLE
    assert result.explore_all[0].eligibility.admission_decision is False
    assert result.state == ShortlistState.MATCHES_NOT_ELIGIBLE


def test_unknown_education_remains_unknown_even_with_verified_entry_criteria() -> None:
    criteria = verified_criteria(frozenset({EducationLevel.GRADE_10}))
    item = pathway(
        "verified-course",
        entry_criteria=criteria,
        verification_status="verified",
    )
    result = build_pathway_shortlist(learner(interests=("technology",)), (item,))

    assert result.shortlist == ()
    assert result.needs_verification[0].eligibility.status == EligibilityStatus.UNKNOWN
    assert result.needs_verification[0].eligibility.reason_code == "learner_education_unknown"


def test_unverified_criteria_do_not_produce_eligibility() -> None:
    criteria = QualificationEntryCriteria(
        qualification_code="TEST-Q-001",
        accepted_education_levels=frozenset({EducationLevel.GRADE_10}),
        source_publisher="Test fixture publisher",
        source_url="https://example.org/test-qualification",
        last_verified_at=date(2026, 1, 1),
        verification_status=CriteriaVerificationStatus.NEEDS_REVIEW,
    )
    item = pathway(
        "verified-course",
        entry_criteria=criteria,
        verification_status="verified",
    )
    result = build_pathway_shortlist(
        learner(interests=("technology",), education_level=EducationLevel.GRADE_12),
        (item,),
    )

    assert result.needs_verification[0].eligibility.status == EligibilityStatus.UNKNOWN
    assert result.needs_verification[0].eligibility.reason_code == "criteria_not_verified"


def test_parent_context_is_not_used_as_a_shortlisting_signal() -> None:
    context = FamilyCounsellingContext(
        learner=learner(interests=("technology",)),
        parent=ParentContext(
            participant_ref="parent_test",
            concerns=(ConcernCategory.WORKPLACE_SAFETY,),
            priorities=("workplace_safety",),
        ),
    )
    result = build_pathway_shortlist(
        context.learner,
        (
            pathway("technology", interests=("technology",), work_preferences=()),
            pathway("safety", interests=("design_and_creativity",), work_preferences=()),
        ),
    )

    assert result.shortlist == ()
    assert [item.pathway.course.course_id for item in result.needs_verification] == ["technology"]
    assert [item.pathway.course.course_id for item in result.explore_all] == ["safety"]


def test_duplicate_catalogue_identifiers_are_rejected() -> None:
    with pytest.raises(ValueError, match="identifiers must be unique"):
        build_pathway_shortlist(
            learner(interests=("technology",)),
            (pathway("same"), pathway("same")),
        )


def test_invalid_shortlist_limit_is_rejected() -> None:
    with pytest.raises(ValueError, match="between 1 and 20"):
        build_pathway_shortlist(learner(), (pathway("course-a"),), max_shortlist=0)


def test_non_integer_shortlist_limit_is_rejected() -> None:
    with pytest.raises(ValueError, match="must be an integer"):
        build_pathway_shortlist(learner(), (pathway("course-a"),), max_shortlist=True)


def test_catalogue_rejects_unsupported_preference_tags() -> None:
    with pytest.raises(ValueError, match="unsupported tags"):
        pathway("bad", interests=("personality_score",), work_preferences=())


def test_qualification_criteria_must_match_a_verified_course_code() -> None:
    criteria = verified_criteria(frozenset({EducationLevel.GRADE_10}))
    course = CourseRecord(
        course_id="wrong-course",
        title="Wrong course",
        trade="Illustrative trade",
        qualification_code="OTHER-CODE",
        source_publisher="Test fixture publisher",
        source_url="https://example.org/test-course",
        last_verified_at=date(2026, 1, 1),
        verification_status="verified",
    )

    with pytest.raises(ValueError, match="codes must match"):
        AdvisoryPathway(
            course=course,
            display_title_mr="चाचणी",
            display_trade_mr="चाचणी",
            interest_tags=("technology",),
            entry_criteria=criteria,
        )


def test_empty_catalogue_is_reported_without_inventing_options() -> None:
    result = build_pathway_shortlist(learner(interests=("technology",)), ())

    assert result.state == ShortlistState.NO_CATALOGUE
    assert result.shortlist == ()
    assert result.needs_verification == ()
    assert result.explore_all == ()
    assert result.all_options == ()
