"""Load curated public qualification records with strict typed validation."""

from __future__ import annotations

import json
from datetime import date
from decimal import Decimal
from importlib.resources import files

from core.domain import CourseRecord
from core.qualification_explainers import (
    QualificationExplainerRecord,
    QualificationFact,
    QualificationFactKind,
    QualificationRecordStatus,
)


def _parse_date(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def load_official_qualification_examples() -> tuple[QualificationExplainerRecord, ...]:
    """Load the small, source-backed NQR example catalogue shipped with the app."""
    resource = files("data.qualifications").joinpath("assistant_baking_technician.json")
    payload = json.loads(resource.read_text(encoding="utf-8"))
    course_data = payload["course"]

    course = CourseRecord(
        course_id=course_data["course_id"],
        title=course_data["title"],
        trade=course_data["trade"],
        qualification_code=course_data["qualification_code"],
        awarding_body=course_data.get("awarding_body"),
        nsqf_level=Decimal(str(course_data["nsqf_level"]))
        if course_data.get("nsqf_level") is not None
        else None,
        job_roles=tuple(course_data.get("job_roles", ())),
        entry_requirements=tuple(course_data.get("entry_requirements", ())),
        source_publisher=course_data.get("source_publisher"),
        source_url=course_data.get("source_url"),
        source_publication_date=_parse_date(course_data.get("source_publication_date")),
        last_verified_at=_parse_date(course_data.get("last_verified_at")),
        verification_status=course_data["verification_status"],
    )

    facts = tuple(
        QualificationFact(
            fact_id=item["fact_id"],
            kind=QualificationFactKind(item["kind"]),
            text_en=item["text_en"],
            text_mr=item["text_mr"],
            source_publisher=item.get("source_publisher"),
            source_url=item.get("source_url"),
            source_reference=item.get("source_reference"),
            source_publication_date=_parse_date(item.get("source_publication_date")),
            last_verified_at=_parse_date(item.get("last_verified_at")),
            verification_status=item.get("verification_status", "needs_review"),
            related_qualification_title=item.get("related_qualification_title"),
            related_nsqf_level=Decimal(str(item["related_nsqf_level"]))
            if item.get("related_nsqf_level") is not None
            else None,
        )
        for item in payload["facts"]
    )

    return (
        QualificationExplainerRecord(
            course=course,
            record_status=QualificationRecordStatus(payload["record_status"]),
            valid_until=_parse_date(payload.get("valid_until")),
            facts=facts,
            nqr_record_url=payload.get("nqr_record_url"),
            marathi_translation_reviewed=bool(payload.get("marathi_translation_reviewed", False)),
        ),
    )
