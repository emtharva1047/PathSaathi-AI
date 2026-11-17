"""Tests for provenance-gated qualification and NSQF explainer records."""

from dataclasses import replace
from datetime import date
from decimal import Decimal

import pytest

from core.domain import CourseRecord, normalize_nsqf_level
from core.qualification_explainers import (
    ExplainerStatus,
    QualificationFact,
    QualificationFactKind,
    QualificationRecordStatus,
    build_qualification_explainer,
)
from services.qualification_catalogue import load_official_qualification_examples


AS_OF = date(2026, 11, 17)


def test_curated_nqr_record_contains_source_backed_job_entry_and_progression_facts() -> None:
    record = load_official_qualification_examples()[0]
    view = build_qualification_explainer(record, as_of=AS_OF)

    assert view.status == ExplainerStatus.CURRENT
    assert record.course.title == "Assistant Baking Technician"
    assert record.course.nsqf_level == Decimal("3.0")
    assert record.valid_until == date(2027, 8, 26)
    assert any(fact.kind == QualificationFactKind.JOB_DESCRIPTION for fact in view.visible_facts)
    assert len([fact for fact in view.visible_facts if fact.kind == QualificationFactKind.ENTRY_ROUTE]) == 4
    progression = next(
        fact for fact in view.visible_facts if fact.kind == QualificationFactKind.PROGRESSION
    )
    assert progression.related_qualification_title == "Plant Biscuit Production Specialist"
    assert progression.related_nsqf_level == Decimal("4.0")
    assert record.marathi_translation_reviewed is False


def test_expired_qualification_suppresses_all_current_guidance() -> None:
    record = load_official_qualification_examples()[0]
    expired = replace(record, valid_until=date(2026, 11, 16))

    view = build_qualification_explainer(expired, as_of=AS_OF)

    assert view.status == ExplainerStatus.EXPIRED
    assert view.visible_facts == ()
    assert view.withheld_fact_count == len(record.facts)


def test_archived_and_unknown_records_do_not_expose_claims() -> None:
    record = load_official_qualification_examples()[0]

    archived = build_qualification_explainer(
        replace(record, record_status=QualificationRecordStatus.ARCHIVED),
        as_of=AS_OF,
    )
    unknown = build_qualification_explainer(
        replace(record, record_status=QualificationRecordStatus.UNKNOWN),
        as_of=AS_OF,
    )

    assert archived.status == ExplainerStatus.ARCHIVED
    assert archived.visible_facts == ()
    assert unknown.status == ExplainerStatus.UNKNOWN
    assert unknown.visible_facts == ()


def test_unverified_claim_is_withheld_without_hiding_verified_claims() -> None:
    record = load_official_qualification_examples()[0]
    unverified = replace(
        record.facts[0],
        fact_id="job-description-needs-review",
        verification_status="needs_review",
    )
    partial_record = replace(record, facts=(*record.facts, unverified))

    view = build_qualification_explainer(partial_record, as_of=AS_OF)

    assert view.status == ExplainerStatus.PARTIAL
    assert view.withheld_fact_count == 1
    assert len(view.visible_facts) == len(record.facts)


def test_future_dated_claim_is_withheld() -> None:
    record = load_official_qualification_examples()[0]
    future_fact = replace(
        record.facts[0],
        fact_id="future-job-description",
        last_verified_at=date(2026, 11, 18),
    )
    partial_record = replace(record, facts=(*record.facts, future_fact))

    view = build_qualification_explainer(partial_record, as_of=AS_OF)

    assert view.status == ExplainerStatus.PARTIAL
    assert view.withheld_fact_count == 1


def test_verified_fact_requires_complete_provenance() -> None:
    with pytest.raises(ValueError, match="Verified qualification facts"):
        QualificationFact(
            fact_id="missing-source",
            kind=QualificationFactKind.JOB_DESCRIPTION,
            text_en="A sourced claim.",
            text_mr="स्रोतासह माहिती.",
            verification_status="verified",
        )


def test_progression_fact_requires_a_target_qualification() -> None:
    with pytest.raises(ValueError, match="related qualification title"):
        QualificationFact(
            fact_id="missing-progression-target",
            kind=QualificationFactKind.PROGRESSION,
            text_en="Progression is described.",
            text_mr="प्रगतीचा मार्ग नमूद आहे.",
        )


def test_nsqf_levels_preserve_half_steps_and_reject_arbitrary_decimals() -> None:
    assert normalize_nsqf_level(Decimal("2.5")) == Decimal("2.5")
    assert normalize_nsqf_level(3) == Decimal("3.0")
    assert normalize_nsqf_level(None) is None
    with pytest.raises(ValueError, match="half-level"):
        normalize_nsqf_level(Decimal("2.3"))


def test_course_record_accepts_fractional_nsqf_levels() -> None:
    course = CourseRecord(
        course_id="fractional-level",
        title="Test qualification",
        trade="Test trade",
        nsqf_level=Decimal("2.5"),
        verification_status="synthetic_demo",
    )

    assert course.nsqf_level == Decimal("2.5")
