"""Deterministic in-memory repository adapters for tests and labelled demos."""

from __future__ import annotations

from collections.abc import Iterable

from core.domain import CourseRecord, OutcomeEvidenceRecord
from services.repositories import (
    CourseQuery,
    CourseRepository,
    OutcomeEvidenceRepository,
    OutcomeQuery,
)


def _normalise(value: str) -> str:
    return value.strip().casefold()


def _matches(actual: str | None, expected: str | None) -> bool:
    if expected is None:
        return True
    return actual is not None and _normalise(actual) == _normalise(expected)


class InMemoryCourseRepository(CourseRepository):
    """Immutable fixture-backed course repository; never persists user data."""

    def __init__(self, courses: Iterable[CourseRecord] = ()) -> None:
        records = tuple(courses)
        identifiers = [record.course_id for record in records]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("Course identifiers must be unique.")
        self._courses = records
        self._by_id = {record.course_id: record for record in records}

    def list_courses(self, query: CourseQuery | None = None) -> tuple[CourseRecord, ...]:
        if query is None:
            return self._courses

        matches: list[CourseRecord] = []
        for course in self._courses:
            if not all(
                (
                    _matches(course.state, query.state),
                    _matches(course.district, query.district),
                    _matches(course.trade, query.trade),
                    _matches(course.provider_id, query.provider_id),
                )
            ):
                continue
            if query.min_nsqf_level is not None:
                if course.nsqf_level is None or course.nsqf_level < query.min_nsqf_level:
                    continue
            if query.max_nsqf_level is not None:
                if course.nsqf_level is None or course.nsqf_level > query.max_nsqf_level:
                    continue
            matches.append(course)
        return tuple(matches)

    def get_course(self, course_id: str) -> CourseRecord | None:
        return self._by_id.get(course_id)


class InMemoryOutcomeEvidenceRepository(OutcomeEvidenceRepository):
    """Immutable outcome fixture adapter that preserves unknown and synthetic records."""

    def __init__(self, outcomes: Iterable[OutcomeEvidenceRecord] = ()) -> None:
        records = tuple(outcomes)
        identifiers = [record.evidence_id for record in records]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("Outcome evidence identifiers must be unique.")
        self._outcomes = records
        self._by_id = {record.evidence_id: record for record in records}

    def list_outcomes(self, query: OutcomeQuery | None = None) -> tuple[OutcomeEvidenceRecord, ...]:
        if query is None:
            return self._outcomes

        return tuple(
            outcome
            for outcome in self._outcomes
            if all(
                (
                    _matches(outcome.metric_code, query.metric_code),
                    _matches(outcome.trade_or_job_role, query.trade_or_job_role),
                    _matches(outcome.provider_id, query.provider_id),
                    _matches(outcome.state, query.state),
                    _matches(outcome.district, query.district),
                    _matches(outcome.verification_status, query.verification_status),
                )
            )
        )

    def get_outcome(self, evidence_id: str) -> OutcomeEvidenceRecord | None:
        return self._by_id.get(evidence_id)
