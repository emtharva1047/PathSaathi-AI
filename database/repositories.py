"""SQLAlchemy adapters implementing the storage-independent repository contracts."""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.domain import CourseRecord, OutcomeEvidenceRecord
from database.models import CourseModel, OutcomeEvidenceModel
from services.repositories import CourseQuery, OutcomeQuery


class SqlAlchemyCourseRepository:
    """Session-scoped course repository; callers own transaction boundaries."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add_course(self, record: CourseRecord) -> None:
        """Stage a new course record; the caller commits or rolls back."""
        self._session.add(CourseModel.from_domain(record))
        self._session.flush()

    def list_courses(self, query: CourseQuery | None = None) -> tuple[CourseRecord, ...]:
        statement = select(CourseModel)
        if query is not None:
            for field_name in ("state", "district", "trade", "provider_id"):
                expected = getattr(query, field_name)
                if expected is not None:
                    column = getattr(CourseModel, field_name)
                    statement = statement.where(func.lower(column) == expected.strip().lower())
            if query.min_nsqf_level is not None:
                statement = statement.where(CourseModel.nsqf_level >= query.min_nsqf_level)
            if query.max_nsqf_level is not None:
                statement = statement.where(CourseModel.nsqf_level <= query.max_nsqf_level)
        records = self._session.scalars(statement.order_by(CourseModel.course_id)).all()
        return tuple(record.to_domain() for record in records)

    def get_course(self, course_id: str) -> CourseRecord | None:
        record = self._session.get(CourseModel, course_id)
        return record.to_domain() if record is not None else None


class SqlAlchemyOutcomeEvidenceRepository:
    """Session-scoped outcome repository that never broadens evidence scope."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add_outcome(self, record: OutcomeEvidenceRecord) -> None:
        """Stage a new outcome record; the caller commits or rolls back."""
        self._session.add(OutcomeEvidenceModel.from_domain(record))
        self._session.flush()

    def list_outcomes(self, query: OutcomeQuery | None = None) -> tuple[OutcomeEvidenceRecord, ...]:
        statement = select(OutcomeEvidenceModel)
        if query is not None:
            for field_name in (
                "metric_code",
                "trade_or_job_role",
                "provider_id",
                "state",
                "district",
                "verification_status",
            ):
                expected = getattr(query, field_name)
                if expected is not None:
                    column = getattr(OutcomeEvidenceModel, field_name)
                    statement = statement.where(func.lower(column) == expected.strip().lower())
            if query.provider_id is not None:
                statement = statement.where(OutcomeEvidenceModel.geography_level == "provider")
        records = self._session.scalars(statement.order_by(OutcomeEvidenceModel.evidence_id)).all()
        return tuple(record.to_domain() for record in records)

    def get_outcome(self, evidence_id: str) -> OutcomeEvidenceRecord | None:
        record = self._session.get(OutcomeEvidenceModel, evidence_id)
        return record.to_domain() if record is not None else None