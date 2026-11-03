"""SQLAlchemy persistence models for sourced course and outcome records."""
from __future__ import annotations

from datetime import date

from sqlalchemy import CheckConstraint, Date, Float, Index, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.domain import CourseRecord, OutcomeEvidenceRecord
from database.base import Base


class CourseModel(Base):
    """A course or qualification catalogue record."""

    __tablename__ = "courses"
    __table_args__ = (
        CheckConstraint("nsqf_level IS NULL OR nsqf_level BETWEEN 1 AND 10", name="nsqf_range"),
        CheckConstraint(
            "verification_status IN ('verified', 'needs_review', 'stale', 'synthetic_demo')",
            name="verification_status",
        ),
        CheckConstraint(
            "verification_status != 'verified' OR "
            "(source_publisher IS NOT NULL AND source_url IS NOT NULL "
            "AND last_verified_at IS NOT NULL)",
            name="verified_source_provenance",
        ),
        Index("ix_courses_trade_state", "trade", "state"),
    )

    course_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    trade: Mapped[str] = mapped_column(String(200), nullable=False)
    qualification_code: Mapped[str | None] = mapped_column(String(100))
    awarding_body: Mapped[str | None] = mapped_column(String(200))
    nsqf_level: Mapped[int | None] = mapped_column(Integer)
    state: Mapped[str | None] = mapped_column(String(100))
    district: Mapped[str | None] = mapped_column(String(100))
    provider_id: Mapped[str | None] = mapped_column(String(100))
    job_roles: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    entry_requirements: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    source_publisher: Mapped[str | None] = mapped_column(String(250))
    source_url: Mapped[str | None] = mapped_column(Text)
    source_publication_date: Mapped[date | None] = mapped_column(Date)
    last_verified_at: Mapped[date | None] = mapped_column(Date)
    verification_status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="needs_review"
    )

    @classmethod
    def from_domain(cls, record: CourseRecord) -> CourseModel:
        """Create a persistence model without changing source status or unknowns."""
        return cls(
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
        )

    def to_domain(self) -> CourseRecord:
        """Return the storage-independent course record."""
        return CourseRecord(
            course_id=self.course_id,
            title=self.title,
            trade=self.trade,
            qualification_code=self.qualification_code,
            awarding_body=self.awarding_body,
            nsqf_level=self.nsqf_level,
            state=self.state,
            district=self.district,
            provider_id=self.provider_id,
            job_roles=tuple(self.job_roles or ()),
            entry_requirements=tuple(self.entry_requirements or ()),
            source_publisher=self.source_publisher,
            source_url=self.source_url,
            source_publication_date=self.source_publication_date,
            last_verified_at=self.last_verified_at,
            verification_status=self.verification_status,  # type: ignore[arg-type]
        )


class OutcomeEvidenceModel(Base):
    """One source-scoped outcome observation; missing values remain SQL NULL."""

    __tablename__ = "outcome_evidence"
    __table_args__ = (
        CheckConstraint(
            "metric_kind IN ('rate', 'earnings', 'count', 'other')",
            name="metric_kind",
        ),
        CheckConstraint(
            "geography_level IN ('national', 'state', 'district', 'provider')",
            name="geography_level",
        ),
        CheckConstraint(
            "statistic_type IN ('mean', 'median', 'band', 'unknown')",
            name="statistic_type",
        ),
        CheckConstraint(
            "verification_status IN ('verified', 'needs_review', 'stale', 'synthetic_demo')",
            name="verification_status",
        ),
        CheckConstraint(
            "value IS NULL OR metric_kind != 'rate' OR (value >= 0 AND value <= 100)",
            name="rate_percentage",
        ),
        CheckConstraint(
            "denominator IS NULL OR denominator > 0",
            name="positive_denominator",
        ),
        CheckConstraint(
            "numerator IS NULL OR numerator >= 0",
            name="nonnegative_numerator",
        ),
        CheckConstraint(
            "numerator IS NULL OR denominator IS NULL OR numerator <= denominator",
            name="numerator_not_above_denominator",
        ),
        CheckConstraint(
            "(numerator IS NULL AND denominator IS NULL) OR "
            "(numerator IS NOT NULL AND denominator IS NOT NULL)",
            name="paired_rate_counts",
        ),
        CheckConstraint(
            "sample_size IS NULL OR sample_size > 0",
            name="positive_sample_size",
        ),
        CheckConstraint(
            "value IS NULL OR metric_kind NOT IN ('earnings', 'count') OR value >= 0",
            name="nonnegative_earnings_and_counts",
        ),
        CheckConstraint(
            "verification_status != 'verified' OR "
            "(source_publisher IS NOT NULL AND source_url IS NOT NULL "
            "AND last_verified_at IS NOT NULL)",
            name="verified_source_provenance",
        ),
        Index("ix_outcomes_trade_provider_scope", "trade_or_job_role", "provider_id", "state"),
    )

    evidence_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    metric_code: Mapped[str] = mapped_column(String(120), nullable=False)
    metric_label: Mapped[str] = mapped_column(String(250), nullable=False)
    definition: Mapped[str] = mapped_column(Text, nullable=False)
    metric_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    value: Mapped[float | None] = mapped_column(Float)
    geography_level: Mapped[str] = mapped_column(String(32), nullable=False)
    geography_name: Mapped[str] = mapped_column(String(150), nullable=False)
    trade_or_job_role: Mapped[str | None] = mapped_column(String(200))
    provider_id: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    district: Mapped[str | None] = mapped_column(String(100))
    numerator: Mapped[int | None] = mapped_column(Integer)
    denominator: Mapped[int | None] = mapped_column(Integer)
    sample_size: Mapped[int | None] = mapped_column(Integer)
    cohort_period: Mapped[str | None] = mapped_column(String(120))
    observation_period: Mapped[str | None] = mapped_column(String(120))
    currency: Mapped[str | None] = mapped_column(String(12))
    unit: Mapped[str | None] = mapped_column(String(80))
    statistic_type: Mapped[str] = mapped_column(String(32), nullable=False, default="unknown")
    follow_up_period: Mapped[str | None] = mapped_column(String(120))
    source_publisher: Mapped[str | None] = mapped_column(String(250))
    source_url: Mapped[str | None] = mapped_column(Text)
    source_publication_date: Mapped[date | None] = mapped_column(Date)
    source_page_or_table: Mapped[str | None] = mapped_column(String(200))
    methodology: Mapped[str | None] = mapped_column(Text)
    last_verified_at: Mapped[date | None] = mapped_column(Date)
    verification_status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="needs_review"
    )

    @classmethod
    def from_domain(cls, record: OutcomeEvidenceRecord) -> OutcomeEvidenceModel:
        """Create a persistence model without inventing or aggregating values."""
        return cls(
            evidence_id=record.evidence_id,
            metric_code=record.metric_code,
            metric_label=record.metric_label,
            definition=record.definition,
            metric_kind=record.metric_kind,
            value=record.value,
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
        )

    def to_domain(self) -> OutcomeEvidenceRecord:
        """Return the storage-independent outcome record."""
        return OutcomeEvidenceRecord(
            evidence_id=self.evidence_id,
            metric_code=self.metric_code,
            metric_label=self.metric_label,
            definition=self.definition,
            metric_kind=self.metric_kind,  # type: ignore[arg-type]
            value=self.value,
            geography_level=self.geography_level,  # type: ignore[arg-type]
            geography_name=self.geography_name,
            trade_or_job_role=self.trade_or_job_role,
            provider_id=self.provider_id,
            state=self.state,
            district=self.district,
            numerator=self.numerator,
            denominator=self.denominator,
            sample_size=self.sample_size,
            cohort_period=self.cohort_period,
            observation_period=self.observation_period,
            currency=self.currency,
            unit=self.unit,
            statistic_type=self.statistic_type,  # type: ignore[arg-type]
            follow_up_period=self.follow_up_period,
            source_publisher=self.source_publisher,
            source_url=self.source_url,
            source_publication_date=self.source_publication_date,
            source_page_or_table=self.source_page_or_table,
            methodology=self.methodology,
            last_verified_at=self.last_verified_at,
            verification_status=self.verification_status,  # type: ignore[arg-type]
        )