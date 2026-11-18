"""Load curated multi-route qualification criteria with strict provenance checks."""

from __future__ import annotations

import json
from datetime import date
from decimal import Decimal
from importlib.resources import files
from typing import Any

from core.eligibility import CriteriaVerificationStatus
from core.multi_route_eligibility import (
    CriterionSource,
    EducationLevelCondition,
    MinimumAgeCondition,
    MultiRouteQualificationCriteria,
    PriorNSQFCondition,
    QualificationEntryRoute,
    RelevantExperienceCondition,
)
from core.profiles import EducationLevel


def _parse_date(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def _source(payload: dict[str, Any]) -> CriterionSource:
    return CriterionSource(
        publisher=payload["publisher"],
        url=payload["url"],
        reference=payload["reference"],
        last_verified_at=_parse_date(payload.get("last_verified_at")),
        verification_status=CriteriaVerificationStatus(
            payload.get("verification_status", "needs_review")
        ),
    )


def _condition(payload: dict[str, Any]):
    kind = payload["kind"]
    source = _source(payload["source"])
    if kind == "education_level":
        return EducationLevelCondition(
            condition_id=payload["condition_id"],
            accepted_levels=frozenset(EducationLevel(value) for value in payload["accepted_levels"]),
            source=source,
        )
    if kind == "prior_nsqf":
        return PriorNSQFCondition(
            condition_id=payload["condition_id"],
            minimum_level=Decimal(str(payload["minimum_level"])),
            source=source,
        )
    if kind == "relevant_experience":
        return RelevantExperienceCondition(
            condition_id=payload["condition_id"],
            minimum_months=payload["minimum_months"],
            industry_code=payload["industry_code"],
            industry_label_en=payload["industry_label_en"],
            industry_label_mr=payload["industry_label_mr"],
            source=source,
        )
    if kind == "minimum_age":
        return MinimumAgeCondition(
            condition_id=payload["condition_id"],
            minimum_years=payload["minimum_years"],
            source=source,
        )
    raise ValueError(f"Unsupported qualification entry condition kind: {kind}")


def load_multi_route_qualification_examples() -> tuple[MultiRouteQualificationCriteria, ...]:
    """Load source-backed OR/AND entry criteria from packaged JSON."""
    resource = files("data.qualifications").joinpath(
        "assistant_baking_technician_entry_routes.json"
    )
    payload = json.loads(resource.read_text(encoding="utf-8"))
    routes = tuple(
        QualificationEntryRoute(
            route_id=route["route_id"],
            conditions=tuple(_condition(item) for item in route["conditions"]),
        )
        for route in payload["routes"]
    )
    return (
        MultiRouteQualificationCriteria(
            qualification_code=payload["qualification_code"],
            qualification_version=payload["qualification_version"],
            routes=routes,
            source=_source(payload["source"]),
            valid_until=_parse_date(payload.get("valid_until")),
        ),
    )


def load_assistant_baking_technician_entry_criteria() -> MultiRouteQualificationCriteria:
    """Return the curated NQR 12209 entry-criteria record."""
    return load_multi_route_qualification_examples()[0]
