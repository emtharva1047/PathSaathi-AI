"""Contract tests for storage-independent course and outcome repositories."""

from datetime import date

import pytest

from core.domain import CourseRecord, OutcomeEvidenceRecord
from services.in_memory import InMemoryCourseRepository, InMemoryOutcomeEvidenceRepository
from services.repositories import CourseQuery, OutcomeQuery


def make_course(
    course_id: str,
    *,
    trade: str = "Electrician",
    state: str = "Maharashtra",
    district: str = "Thane",
    nsqf_level: int | None = 4,
) -> CourseRecord:
    return CourseRecord(
        course_id=course_id,
        title=f"Course {course_id}",
        trade=trade,
        state=state,
        district=district,
        nsqf_level=nsqf_level,
        verification_status="synthetic_demo",
    )


def make_outcome(
    evidence_id: str,
    *,
    trade: str = "Electrician",
    state: str = "Maharashtra",
    value: float | None = 62.0,
    verification_status: str = "synthetic_demo",
) -> OutcomeEvidenceRecord:
    return OutcomeEvidenceRecord(
        evidence_id=evidence_id,
        metric_code="trade_related_employment_rate",
        metric_label="Trade-related employment",
        definition="Synthetic test-only share of respondents employed in the trained trade.",
        metric_kind="rate",
        value=value,
        geography_level="state",
        geography_name=state,
        state=state,
        trade_or_job_role=trade,
        verification_status=verification_status,  # type: ignore[arg-type]
    )


def test_course_repository_filters_case_insensitive_and_by_nsqf_range() -> None:
    repository = InMemoryCourseRepository(
        (
            make_course("a", nsqf_level=3),
            make_course("b", nsqf_level=5),
            make_course("c", trade="Fitter", nsqf_level=5),
            make_course("d", nsqf_level=None),
        )
    )

    results = repository.list_courses(
        CourseQuery(state="maharashtra", trade="ELECTRICIAN", min_nsqf_level=4)
    )

    assert [course.course_id for course in results] == ["b"]


def test_course_repository_returns_empty_tuple_for_no_match() -> None:
    repository = InMemoryCourseRepository((make_course("a"),))

    assert repository.list_courses(CourseQuery(district="Pune")) == ()


def test_course_repository_preserves_unknown_nsqf_level() -> None:
    unknown = make_course("unknown", nsqf_level=None)
    repository = InMemoryCourseRepository((unknown,))

    assert repository.get_course("unknown") == unknown
    assert repository.list_courses()[0].nsqf_level is None


def test_course_repository_rejects_duplicate_identifiers() -> None:
    course = make_course("duplicate")

    with pytest.raises(ValueError, match="identifiers must be unique"):
        InMemoryCourseRepository((course, course))


def test_course_query_rejects_inverted_nsqf_range() -> None:
    with pytest.raises(ValueError, match="cannot exceed"):
        CourseQuery(min_nsqf_level=6, max_nsqf_level=3)


def test_outcome_repository_filters_without_changing_geographic_scope() -> None:
    state_record = make_outcome("state")
    district_record = OutcomeEvidenceRecord(
        evidence_id="district",
        metric_code="trade_related_employment_rate",
        metric_label="Trade-related employment",
        definition="Synthetic district-only test evidence.",
        metric_kind="rate",
        value=58.0,
        geography_level="district",
        geography_name="Thane",
        state="Maharashtra",
        district="Thane",
        trade_or_job_role="Electrician",
        verification_status="synthetic_demo",
    )
    repository = InMemoryOutcomeEvidenceRepository((state_record, district_record))

    results = repository.list_outcomes(OutcomeQuery(state="Maharashtra", district="Thane"))

    assert [record.evidence_id for record in results] == ["district"]
    assert repository.get_outcome("state") == state_record
    assert repository.get_outcome("missing") is None


def test_unknown_outcome_is_preserved_but_not_displayable() -> None:
    unknown = make_outcome("unknown", value=None, verification_status="needs_review")
    repository = InMemoryOutcomeEvidenceRepository((unknown,))

    result = repository.list_outcomes()[0]

    assert result.value is None
    assert result.is_verified_displayable is False


def test_synthetic_outcome_is_never_marked_verified_displayable() -> None:
    synthetic = make_outcome("synthetic")

    assert synthetic.verification_status == "synthetic_demo"
    assert synthetic.is_verified_displayable is False


def test_verified_outcome_requires_complete_source_provenance() -> None:
    with pytest.raises(ValueError, match="source publisher"):
        make_outcome("unproven", verification_status="verified")


def test_verified_outcome_with_source_can_be_displayable() -> None:
    verified = OutcomeEvidenceRecord(
        evidence_id="verified",
        metric_code="trade_related_employment_rate",
        metric_label="Trade-related employment",
        definition="Source-reported share of the defined cohort employed in the trained trade.",
        metric_kind="rate",
        value=62.0,
        geography_level="state",
        geography_name="Maharashtra",
        state="Maharashtra",
        numerator=62,
        denominator=100,
        sample_size=100,
        source_publisher="Example official publisher",
        source_url="https://example.gov.in/report",
        source_publication_date=date(2025, 1, 1),
        last_verified_at=date(2026, 11, 2),
        verification_status="verified",
    )

    assert verified.is_verified_displayable is True


def test_rate_outside_percentage_range_is_rejected() -> None:
    with pytest.raises(ValueError, match="percentages from 0 to 100"):
        make_outcome("invalid-rate", value=101.0)


def test_rate_numerator_cannot_exceed_denominator() -> None:
    with pytest.raises(ValueError, match="cannot exceed"):
        OutcomeEvidenceRecord(
            evidence_id="invalid-counts",
            metric_code="placement_rate",
            metric_label="Placement rate",
            definition="Test rate definition.",
            metric_kind="rate",
            value=100.0,
            geography_level="state",
            geography_name="Maharashtra",
            numerator=11,
            denominator=10,
        )


def test_earnings_require_currency_unit_and_statistic_type() -> None:
    with pytest.raises(ValueError, match="currency and unit"):
        OutcomeEvidenceRecord(
            evidence_id="earnings",
            metric_code="median_monthly_earnings",
            metric_label="Median monthly earnings",
            definition="Test earnings definition.",
            metric_kind="earnings",
            value=18000.0,
            geography_level="state",
            geography_name="Maharashtra",
            statistic_type="median",
        )



def test_non_finite_outcome_values_are_rejected() -> None:
    with pytest.raises(ValueError, match="finite numbers"):
        make_outcome("not-finite", value=float("nan"))


def test_negative_earnings_are_rejected() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        OutcomeEvidenceRecord(
            evidence_id="negative-earnings",
            metric_code="median_monthly_earnings",
            metric_label="Median monthly earnings",
            definition="Test earnings definition.",
            metric_kind="earnings",
            value=-1.0,
            geography_level="state",
            geography_name="Maharashtra",
            currency="INR",
            unit="per month",
            statistic_type="median",
        )


def test_outcome_repository_rejects_duplicate_identifiers() -> None:
    outcome = make_outcome("duplicate")

    with pytest.raises(ValueError, match="identifiers must be unique"):
        InMemoryOutcomeEvidenceRepository((outcome, outcome))



def test_unknown_verification_status_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported outcome verification status"):
        make_outcome("invalid-status", verification_status="official")  # type: ignore[arg-type]


def test_unknown_metric_kind_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported outcome metric kind"):
        OutcomeEvidenceRecord(
            evidence_id="invalid-kind",
            metric_code="custom_metric",
            metric_label="Custom metric",
            definition="Test definition.",
            metric_kind="unknown",  # type: ignore[arg-type]
            value=None,
            geography_level="state",
            geography_name="Maharashtra",
        )


def test_unknown_verification_status_filter_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported outcome verification status filter"):
        OutcomeQuery(verification_status="official")  # type: ignore[arg-type]



def test_provider_filter_excludes_state_aggregate_even_if_provider_id_is_tagged() -> None:
    provider_record = make_outcome("provider", verification_status="synthetic_demo")
    state_record = OutcomeEvidenceRecord(
        evidence_id="state-tagged",
        metric_code="trade_related_employment_rate",
        metric_label="Trade-related employment",
        definition="Synthetic state aggregate; provider identifier is not a provider sample.",
        metric_kind="rate",
        value=60.0,
        geography_level="state",
        geography_name="Maharashtra",
        trade_or_job_role="Electrician",
        provider_id="provider-01",
        state="Maharashtra",
        numerator=60,
        denominator=100,
        sample_size=100,
        verification_status="synthetic_demo",
    )
    repository = InMemoryOutcomeEvidenceRepository((provider_record, state_record))

    results = repository.list_outcomes(OutcomeQuery(provider_id="provider-01"))

    assert [record.evidence_id for record in results] == ["provider"]
    assert results[0].geography_level == "provider"
