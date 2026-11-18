"""Tests for source-backed OR/AND qualification eligibility routes."""

from dataclasses import replace
from datetime import date
from decimal import Decimal

import pytest

from core.eligibility import CriteriaVerificationStatus, EligibilityStatus
from core.multi_route_eligibility import (
    CriterionSource,
    LearnerEligibilityEvidence,
    PriorQualificationEvidence,
    PriorQualificationRelevance,
    RelevantExperienceEvidence,
    evaluate_multi_route_eligibility,
)
from core.profiles import EducationLevel
from services.eligibility_catalogue import load_assistant_baking_technician_entry_criteria


AS_OF = date(2026, 11, 18)


def verified_source(reference: str = "NQR record, entry criteria") -> CriterionSource:
    return CriterionSource(
        publisher="Synthetic test awarding body",
        url="https://example.org/qualification/entry",
        reference=reference,
        last_verified_at=AS_OF,
        verification_status=CriteriaVerificationStatus.VERIFIED,
    )


def prior_qualification(
    level: str = "2.5",
    *,
    relevance: PriorQualificationRelevance = PriorQualificationRelevance.VERIFIED_RELEVANT,
    verification: CriteriaVerificationStatus = CriteriaVerificationStatus.VERIFIED,
) -> PriorQualificationEvidence:
    return PriorQualificationEvidence(
        qualification_code="PRIOR-QF-01",
        qualification_version="V1",
        nsqf_level=Decimal(level),
        relevance_status=relevance,
        verification_status=verification,
        source=verified_source("Prior qualification NQR record, NSQF level"),
    )


def experience(
    months: int,
    *,
    verification: CriteriaVerificationStatus = CriteriaVerificationStatus.VERIFIED,
) -> RelevantExperienceEvidence:
    return RelevantExperienceEvidence(
        industry_code="food_industry",
        months=months,
        verification_status=verification,
        evidence_reference="experience-evidence-ref-01",
        last_verified_at=AS_OF if verification == CriteriaVerificationStatus.VERIFIED else None,
    )


@pytest.fixture()
def criteria():
    return load_assistant_baking_technician_entry_criteria()


def test_assistant_baking_technician_has_four_source_backed_or_routes(criteria) -> None:
    assert criteria.qualification_code == "QG-03-FI-02932-2024-V2-FICSI"
    assert criteria.qualification_version == "V4.0"
    assert criteria.valid_until == date(2027, 8, 26)
    assert [route.route_id for route in criteria.routes] == [
        "grade-10",
        "grade-8-plus-36-months",
        "prior-nsqf-2-5-plus-18-months",
        "prior-nsqf-2-plus-36-months",
    ]
    assert all(
        condition.source.is_current(AS_OF)
        for route in criteria.routes
        for condition in route.conditions
    )


def test_assistant_baking_technician_stays_unknown_without_learner_inputs(criteria) -> None:
    result = evaluate_multi_route_eligibility(LearnerEligibilityEvidence(), criteria, as_of=AS_OF)

    assert result.status == EligibilityStatus.UNKNOWN
    assert result.reason_code == "one_or_more_routes_need_more_information"
    assert "age in completed years" in result.missing_information
    assert any("education level" in item for item in result.missing_information)
    assert "जन्मतारीख गोळा केली जात नाही" in result.route_evaluations[0].conditions[1].explanation_mr
    assert result.admission_decision is False


def test_grade_10_route_is_eligible_when_both_and_conditions_are_met(criteria) -> None:
    evidence = LearnerEligibilityEvidence(
        education_level=EducationLevel.GRADE_10,
        age_in_completed_years=18,
    )

    result = evaluate_multi_route_eligibility(evidence, criteria, as_of=AS_OF)

    assert result.status == EligibilityStatus.ELIGIBLE
    assert result.route_evaluations[0].status == EligibilityStatus.ELIGIBLE
    assert all(
        condition.status == EligibilityStatus.ELIGIBLE
        for condition in result.route_evaluations[0].conditions
    )
    assert "not an admission decision" in result.explanation_en
    assert "अंतिम निर्णय नाही" in result.explanation_mr


def test_grade_8_route_requires_education_and_36_months_experience(criteria) -> None:
    incomplete = LearnerEligibilityEvidence(
        education_level=EducationLevel.GRADE_8,
        age_in_completed_years=18,
        relevant_experience=(experience(24),),
    )
    complete = replace(incomplete, relevant_experience=(experience(36),))

    incomplete_result = evaluate_multi_route_eligibility(incomplete, criteria, as_of=AS_OF)
    complete_result = evaluate_multi_route_eligibility(complete, criteria, as_of=AS_OF)

    assert incomplete_result.route_evaluations[1].status == EligibilityStatus.INELIGIBLE
    assert incomplete_result.route_evaluations[1].conditions[1].status == EligibilityStatus.INELIGIBLE
    assert complete_result.status == EligibilityStatus.ELIGIBLE
    assert complete_result.route_evaluations[1].status == EligibilityStatus.ELIGIBLE


def test_prior_nsqf_half_level_route_requires_relevance_and_18_months(criteria) -> None:
    evidence = LearnerEligibilityEvidence(
        age_in_completed_years=18,
        prior_qualifications=(prior_qualification("2.5"),),
        relevant_experience=(experience(18),),
    )

    result = evaluate_multi_route_eligibility(evidence, criteria, as_of=AS_OF)

    assert result.status == EligibilityStatus.ELIGIBLE
    assert result.route_evaluations[2].status == EligibilityStatus.ELIGIBLE
    assert result.route_evaluations[2].conditions[0].reason_code == "verified_relevant_prior_nsqf_met"


def test_prior_nsqf_level_2_route_requires_36_months(criteria) -> None:
    evidence = LearnerEligibilityEvidence(
        age_in_completed_years=18,
        prior_qualifications=(prior_qualification("2.0"),),
        relevant_experience=(experience(36),),
    )

    result = evaluate_multi_route_eligibility(evidence, criteria, as_of=AS_OF)

    assert result.status == EligibilityStatus.ELIGIBLE
    assert result.route_evaluations[3].status == EligibilityStatus.ELIGIBLE


def test_unverified_prior_qualification_or_unknown_relevance_stays_unknown(criteria) -> None:
    evidence = LearnerEligibilityEvidence(
        age_in_completed_years=18,
        prior_qualifications=(
            prior_qualification("2.5", relevance=PriorQualificationRelevance.UNKNOWN),
        ),
        relevant_experience=(experience(18),),
    )

    result = evaluate_multi_route_eligibility(evidence, criteria, as_of=AS_OF)

    assert result.status == EligibilityStatus.UNKNOWN
    assert result.route_evaluations[2].status == EligibilityStatus.UNKNOWN
    assert result.route_evaluations[2].conditions[0].reason_code == "prior_qualification_needs_verification"


def test_self_reported_experience_does_not_satisfy_verified_requirement(criteria) -> None:
    evidence = LearnerEligibilityEvidence(
        education_level=EducationLevel.GRADE_8,
        age_in_completed_years=18,
        relevant_experience=(
            experience(36, verification=CriteriaVerificationStatus.NEEDS_REVIEW),
        ),
    )

    result = evaluate_multi_route_eligibility(evidence, criteria, as_of=AS_OF)

    assert result.status == EligibilityStatus.UNKNOWN
    assert result.route_evaluations[1].status == EligibilityStatus.UNKNOWN
    assert result.route_evaluations[1].conditions[1].status == EligibilityStatus.UNKNOWN


def test_minimum_age_boundary_is_inclusive(criteria) -> None:
    age_16 = evaluate_multi_route_eligibility(
        LearnerEligibilityEvidence(
            education_level=EducationLevel.GRADE_10,
            age_in_completed_years=16,
        ),
        criteria,
        as_of=AS_OF,
    )
    age_15 = evaluate_multi_route_eligibility(
        LearnerEligibilityEvidence(
            education_level=EducationLevel.GRADE_10,
            age_in_completed_years=15,
        ),
        criteria,
        as_of=AS_OF,
    )

    assert age_16.status == EligibilityStatus.ELIGIBLE
    assert age_15.status == EligibilityStatus.UNKNOWN
    assert age_15.route_evaluations[0].conditions[1].status == EligibilityStatus.INELIGIBLE


def test_ineligible_requires_every_alternative_route_to_be_resolved(criteria) -> None:
    evidence = LearnerEligibilityEvidence(
        education_level=EducationLevel.GRADE_8,
        age_in_completed_years=18,
        prior_qualifications=(),
        relevant_experience=(experience(12),),
    )

    result = evaluate_multi_route_eligibility(evidence, criteria, as_of=AS_OF)

    assert result.status == EligibilityStatus.INELIGIBLE
    assert result.reason_code == "all_routes_fully_evaluated_and_not_met"
    assert all(route.status == EligibilityStatus.INELIGIBLE for route in result.route_evaluations)


def test_missing_age_keeps_otherwise_matching_route_unknown(criteria) -> None:
    result = evaluate_multi_route_eligibility(
        LearnerEligibilityEvidence(education_level=EducationLevel.GRADE_10),
        criteria,
        as_of=AS_OF,
    )

    assert result.status == EligibilityStatus.UNKNOWN
    assert result.route_evaluations[0].status == EligibilityStatus.UNKNOWN
    assert result.route_evaluations[0].conditions[0].status == EligibilityStatus.ELIGIBLE
    assert result.route_evaluations[0].conditions[1].status == EligibilityStatus.UNKNOWN


def test_stale_or_expired_criteria_suppress_route_results(criteria) -> None:
    stale = replace(
        criteria,
        source=replace(
            criteria.source,
            verification_status=CriteriaVerificationStatus.STALE,
        ),
    )
    expired = replace(criteria, valid_until=date(2026, 11, 17))
    evidence = LearnerEligibilityEvidence(
        education_level=EducationLevel.GRADE_10,
        age_in_completed_years=18,
    )

    stale_result = evaluate_multi_route_eligibility(evidence, stale, as_of=AS_OF)
    expired_result = evaluate_multi_route_eligibility(evidence, expired, as_of=AS_OF)

    assert stale_result.status == EligibilityStatus.UNKNOWN
    assert expired_result.status == EligibilityStatus.UNKNOWN
    assert all(route.status == EligibilityStatus.UNKNOWN for route in expired_result.route_evaluations)


def test_stale_condition_source_is_unknown_even_if_record_source_is_current(criteria) -> None:
    route = criteria.routes[0]
    condition = replace(
        route.conditions[0],
        source=replace(
            route.conditions[0].source,
            verification_status=CriteriaVerificationStatus.STALE,
        ),
    )
    changed_route = replace(route, conditions=(condition, *route.conditions[1:]))
    changed = replace(criteria, routes=(changed_route, *criteria.routes[1:]))

    result = evaluate_multi_route_eligibility(
        LearnerEligibilityEvidence(
            education_level=EducationLevel.GRADE_10,
            age_in_completed_years=18,
        ),
        changed,
        as_of=AS_OF,
    )

    assert result.status == EligibilityStatus.UNKNOWN
    assert result.route_evaluations[0].conditions[0].reason_code == "criterion_source_not_current"


def test_routes_must_have_unique_ids_and_nonempty_conditions(criteria) -> None:
    with pytest.raises(ValueError, match="unique"):
        replace(criteria, routes=(criteria.routes[0], criteria.routes[0]))
    with pytest.raises(ValueError, match="at least one condition"):
        replace(criteria.routes[0], conditions=())


def test_verified_prior_qualification_requires_verified_source() -> None:
    with pytest.raises(ValueError, match="verified source"):
        PriorQualificationEvidence(
            qualification_code="PRIOR-QF-02",
            qualification_version="V1",
            nsqf_level=Decimal("2.5"),
            verification_status=CriteriaVerificationStatus.VERIFIED,
        )


def test_inputs_use_completed_years_and_opaque_evidence_not_dob_or_employer_names() -> None:
    learner_fields = set(LearnerEligibilityEvidence.__dataclass_fields__)
    experience_fields = set(RelevantExperienceEvidence.__dataclass_fields__)

    assert "date_of_birth" not in learner_fields
    assert "employer_name" not in experience_fields
    assert "age_in_completed_years" in learner_fields
    assert "evidence_reference" in experience_fields
