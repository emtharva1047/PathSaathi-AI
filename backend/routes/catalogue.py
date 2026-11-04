"""Read-only catalogue and outcome-evidence API routes."""

from __future__ import annotations

from datetime import date
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.dependencies import get_db_session
from core.domain import CourseRecord, OutcomeEvidenceRecord, VerificationStatus
from database.repositories import SqlAlchemyCourseRepository, SqlAlchemyOutcomeEvidenceRepository
from services.repositories import CourseQuery, OutcomeQuery

router = APIRouter(prefix="/api/v1", tags=["catalogue"])


class CourseResponse(BaseModel):
    """Course data with an explicit source-verification indicator."""

    course_id: str
    title: str
    trade: str
    qualification_code: str | None
    awarding_body: str | None
    nsqf_level: int | None
    state: str | None
    district: str | None
    provider_id: str | None
    job_roles: list[str]
    entry_requirements: list[str]
    source_publisher: str | None
    source_url: str | None
    source_publication_date: date | None
    last_verified_at: date | None
    verification_status: VerificationStatus
    source_verified: bool


class OutcomeEvidenceResponse(BaseModel):
    """Outcome metadata; numeric values are exposed only with verified provenance."""

    evidence_id: str
    metric_code: str
    metric_label: str
    definition: str
    metric_kind: str
    value: float | None
    value_status: Literal["verified", "withheld", "unknown"]
    value_withheld: bool
    geography_level: str
    geography_name: str
    trade_or_job_role: str | None
    provider_id: str | None
    state: str | None
    district: str | None
    numerator: int | None
    denominator: int | None
    sample_size: int | None
    cohort_period: str | None
    observation_period: str | None
    currency: str | None
    unit: str | None
    statistic_type: str
    follow_up_period: str | None
    source_publisher: str | None
    source_url: str | None
    source_publication_date: date | None
    source_page_or_table: str | None
    methodology: str | None
    last_verified_at: date | None
    verification_status: VerificationStatus
    displayable: bool


def _course_response(record: CourseRecord) -> CourseResponse:
    return CourseResponse(
        course_id=record.course_id,
        title=record.title,
        trade=record.trade,
        qualification_code=record.qualification_code,
        awarding_body=record.awarding_body,
        nsqf_level=record.nsqf_level,
        state=record.state,
        district=record.district,
        provider_id=record.provider_id,
        job_roles=list(record.job_roles),
        entry_requirements=list(record.entry_requirements),
        source_publisher=record.source_publisher,
        source_url=record.source_url,
        source_publication_date=record.source_publication_date,
        last_verified_at=record.last_verified_at,
        verification_status=record.verification_status,
        source_verified=record.has_verified_source,
    )


def _outcome_response(record: OutcomeEvidenceRecord) -> OutcomeEvidenceResponse:
    displayable = record.is_verified_displayable
    value_status: Literal["verified", "withheld", "unknown"]
    if displayable:
        value_status = "verified"
    elif record.value is not None:
        value_status = "withheld"
    else:
        value_status = "unknown"

    return OutcomeEvidenceResponse(
        evidence_id=record.evidence_id,
        metric_code=record.metric_code,
        metric_label=record.metric_label,
        definition=record.definition,
        metric_kind=record.metric_kind,
        value=record.value if displayable else None,
        value_status=value_status,
        value_withheld=record.value is not None and not displayable,
        geography_level=record.geography_level,
        geography_name=record.geography_name,
        trade_or_job_role=record.trade_or_job_role,
        provider_id=record.provider_id,
        state=record.state,
        district=record.district,
        numerator=record.numerator,
        denominator=record.denominator,
        sample_size=record.sample_size,
        cohort_period=record.cohort_period,
        observation_period=record.observation_period,
        currency=record.currency,
        unit=record.unit,
        statistic_type=record.statistic_type,
        follow_up_period=record.follow_up_period,
        source_publisher=record.source_publisher,
        source_url=record.source_url,
        source_publication_date=record.source_publication_date,
        source_page_or_table=record.source_page_or_table,
        methodology=record.methodology,
        last_verified_at=record.last_verified_at,
        verification_status=record.verification_status,
        displayable=displayable,
    )


@router.get("/courses", response_model=list[CourseResponse])
def list_courses(
    state: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    district: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    trade: Annotated[str | None, Query(min_length=1, max_length=200)] = None,
    provider_id: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    min_nsqf_level: Annotated[int | None, Query(ge=1, le=10)] = None,
    max_nsqf_level: Annotated[int | None, Query(ge=1, le=10)] = None,
    session: Session = Depends(get_db_session),
) -> list[CourseResponse]:
    """List courses using exact filters; unknown NSQF levels remain unknown."""
    if (
        min_nsqf_level is not None
        and max_nsqf_level is not None
        and min_nsqf_level > max_nsqf_level
    ):
        raise HTTPException(
            status_code=422,
            detail="min_nsqf_level cannot exceed max_nsqf_level.",
        )
    query = CourseQuery(
        state=state,
        district=district,
        trade=trade,
        provider_id=provider_id,
        min_nsqf_level=min_nsqf_level,
        max_nsqf_level=max_nsqf_level,
    )
    records = SqlAlchemyCourseRepository(session).list_courses(query)
    return [_course_response(record) for record in records]


@router.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: Annotated[str, Path(min_length=1, max_length=100)],
    session: Session = Depends(get_db_session),
) -> CourseResponse:
    """Fetch one course by its stable identifier."""
    record = SqlAlchemyCourseRepository(session).get_course(course_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Course not found.")
    return _course_response(record)


@router.get("/outcomes", response_model=list[OutcomeEvidenceResponse])
def list_outcomes(
    metric_code: Annotated[str | None, Query(min_length=1, max_length=120)] = None,
    trade: Annotated[str | None, Query(min_length=1, max_length=200)] = None,
    provider_id: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    state: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    district: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    verification_status: VerificationStatus | None = None,
    session: Session = Depends(get_db_session),
) -> list[OutcomeEvidenceResponse]:
    """List source-scoped outcomes without exposing unverified numeric values."""
    query = OutcomeQuery(
        metric_code=metric_code,
        trade_or_job_role=trade,
        provider_id=provider_id,
        state=state,
        district=district,
        verification_status=verification_status,
    )
    records = SqlAlchemyOutcomeEvidenceRepository(session).list_outcomes(query)
    return [_outcome_response(record) for record in records]


@router.get("/outcomes/{evidence_id}", response_model=OutcomeEvidenceResponse)
def get_outcome(
    evidence_id: Annotated[str, Path(min_length=1, max_length=100)],
    session: Session = Depends(get_db_session),
) -> OutcomeEvidenceResponse:
    """Fetch one evidence record with provenance and value-display safeguards."""
    record = SqlAlchemyOutcomeEvidenceRepository(session).get_outcome(evidence_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Outcome evidence not found.")
    return _outcome_response(record)
