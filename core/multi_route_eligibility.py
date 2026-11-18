"""Source-backed OR/AND qualification entry-route evaluation.

This module is deliberately separate from the education-only evaluator in
core.eligibility. It does not make admission, aptitude, employment or earnings decisions.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum
from re import fullmatch
from urllib.parse import urlsplit

from core.domain import normalize_nsqf_level
from core.eligibility import CriteriaVerificationStatus, EligibilityStatus
from core.profiles import EducationLevel


class PriorQualificationRelevance(StrEnum):
    UNKNOWN = "unknown"
    VERIFIED_RELEVANT = "verified_relevant"
    VERIFIED_NOT_RELEVANT = "verified_not_relevant"


@dataclass(frozen=True, slots=True)
class CriterionSource:
    """Publisher and exact source location for one criterion or evidence record."""

    publisher: str
    url: str
    reference: str
    last_verified_at: date | None
    verification_status: CriteriaVerificationStatus = CriteriaVerificationStatus.NEEDS_REVIEW

    def __post_init__(self) -> None:
        for name in ("publisher", "url", "reference"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty.")
            object.__setattr__(self, name, value.strip())
        parsed = urlsplit(self.url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Criterion source URL must be an absolute HTTP(S) URL.")
        if not isinstance(self.verification_status, CriteriaVerificationStatus):
            raise ValueError("Unsupported criterion source verification status.")
        if self.verification_status == CriteriaVerificationStatus.VERIFIED and self.last_verified_at is None:
            raise ValueError("Verified criterion sources require a verification date.")

    def is_current(self, as_of: date) -> bool:
        return (
            self.verification_status == CriteriaVerificationStatus.VERIFIED
            and self.last_verified_at is not None
            and self.last_verified_at <= as_of
        )


def _validate_id(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not fullmatch(r"[a-z][a-z0-9_-]{1,63}", value):
        raise ValueError(f"{field_name} must be a normalized lowercase identifier.")


@dataclass(frozen=True, slots=True)
class EducationLevelCondition:
    condition_id: str
    accepted_levels: frozenset[EducationLevel]
    source: CriterionSource

    def __post_init__(self) -> None:
        _validate_id(self.condition_id, "condition_id")
        levels = frozenset(self.accepted_levels)
        if not levels or EducationLevel.UNKNOWN in levels:
            raise ValueError("Education conditions need known, non-empty accepted levels.")
        if any(not isinstance(level, EducationLevel) for level in levels):
            raise ValueError("Education conditions must use normalized education levels.")
        object.__setattr__(self, "accepted_levels", levels)


@dataclass(frozen=True, slots=True)
class PriorNSQFCondition:
    condition_id: str
    minimum_level: Decimal
    source: CriterionSource

    def __post_init__(self) -> None:
        _validate_id(self.condition_id, "condition_id")
        level = normalize_nsqf_level(self.minimum_level)
        if level is None:
            raise ValueError("Prior NSQF conditions require a minimum level.")
        object.__setattr__(self, "minimum_level", level)


@dataclass(frozen=True, slots=True)
class RelevantExperienceCondition:
    condition_id: str
    minimum_months: int
    industry_code: str
    industry_label_en: str
    industry_label_mr: str
    source: CriterionSource

    def __post_init__(self) -> None:
        _validate_id(self.condition_id, "condition_id")
        if (
            isinstance(self.minimum_months, bool)
            or not isinstance(self.minimum_months, int)
            or self.minimum_months <= 0
        ):
            raise ValueError("minimum_months must be a positive integer.")
        if not fullmatch(r"[a-z][a-z0-9_]{1,39}", self.industry_code):
            raise ValueError("industry_code must be a normalized category code.")
        for name in ("industry_label_en", "industry_label_mr"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty.")
            object.__setattr__(self, name, value.strip())


@dataclass(frozen=True, slots=True)
class MinimumAgeCondition:
    condition_id: str
    minimum_years: int
    source: CriterionSource

    def __post_init__(self) -> None:
        _validate_id(self.condition_id, "condition_id")
        if (
            isinstance(self.minimum_years, bool)
            or not isinstance(self.minimum_years, int)
            or not 1 <= self.minimum_years <= 120
        ):
            raise ValueError("minimum_years must be an integer between 1 and 120.")


EntryCondition = (
    EducationLevelCondition
    | PriorNSQFCondition
    | RelevantExperienceCondition
    | MinimumAgeCondition
)


@dataclass(frozen=True, slots=True)
class QualificationEntryRoute:
    """One alternative route; every condition inside it is an AND requirement."""

    route_id: str
    conditions: tuple[EntryCondition, ...]

    def __post_init__(self) -> None:
        _validate_id(self.route_id, "route_id")
        conditions = tuple(self.conditions)
        if not conditions:
            raise ValueError("An entry route must contain at least one condition.")
        ids = [condition.condition_id for condition in conditions]
        if len(ids) != len(set(ids)):
            raise ValueError("Condition identifiers must be unique within a route.")
        object.__setattr__(self, "conditions", conditions)


@dataclass(frozen=True, slots=True)
class MultiRouteQualificationCriteria:
    """Versioned qualification criteria containing alternative OR routes."""

    qualification_code: str
    qualification_version: str
    routes: tuple[QualificationEntryRoute, ...]
    source: CriterionSource
    valid_until: date | None = None

    def __post_init__(self) -> None:
        for name in ("qualification_code", "qualification_version"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty.")
            object.__setattr__(self, name, value.strip())
        routes = tuple(self.routes)
        if not routes:
            raise ValueError("Multi-route criteria must contain at least one route.")
        ids = [route.route_id for route in routes]
        if len(ids) != len(set(ids)):
            raise ValueError("Route identifiers must be unique.")
        object.__setattr__(self, "routes", routes)


@dataclass(frozen=True, slots=True)
class PriorQualificationEvidence:
    """Prior NSQF qualification evidence; relevance must be explicitly verified."""

    qualification_code: str
    qualification_version: str
    nsqf_level: Decimal
    relevance_status: PriorQualificationRelevance = PriorQualificationRelevance.UNKNOWN
    verification_status: CriteriaVerificationStatus = CriteriaVerificationStatus.NEEDS_REVIEW
    source: CriterionSource | None = None

    def __post_init__(self) -> None:
        for name in ("qualification_code", "qualification_version"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty.")
            object.__setattr__(self, name, value.strip())
        level = normalize_nsqf_level(self.nsqf_level)
        if level is None:
            raise ValueError("Prior qualification evidence requires an NSQF level.")
        object.__setattr__(self, "nsqf_level", level)
        if not isinstance(self.relevance_status, PriorQualificationRelevance):
            raise ValueError("Unsupported prior qualification relevance status.")
        if not isinstance(self.verification_status, CriteriaVerificationStatus):
            raise ValueError("Unsupported prior qualification verification status.")
        if self.verification_status == CriteriaVerificationStatus.VERIFIED:
            if self.source is None or self.source.verification_status != CriteriaVerificationStatus.VERIFIED:
                raise ValueError("Verified prior qualifications require a verified source.")


@dataclass(frozen=True, slots=True)
class RelevantExperienceEvidence:
    """Verified non-overlapping months by industry; employer names are not stored."""

    industry_code: str
    months: int
    verification_status: CriteriaVerificationStatus = CriteriaVerificationStatus.NEEDS_REVIEW
    evidence_reference: str | None = None
    last_verified_at: date | None = None

    def __post_init__(self) -> None:
        if not fullmatch(r"[a-z][a-z0-9_]{1,39}", self.industry_code):
            raise ValueError("industry_code must be a normalized category code.")
        if isinstance(self.months, bool) or not isinstance(self.months, int) or self.months < 0:
            raise ValueError("months must be a non-negative integer.")
        if not isinstance(self.verification_status, CriteriaVerificationStatus):
            raise ValueError("Unsupported experience verification status.")
        if self.evidence_reference is not None:
            if not self.evidence_reference.strip():
                raise ValueError("evidence_reference cannot be blank.")
            object.__setattr__(self, "evidence_reference", self.evidence_reference.strip())
        if self.verification_status == CriteriaVerificationStatus.VERIFIED:
            if not self.evidence_reference or self.last_verified_at is None:
                raise ValueError("Verified experience requires an opaque evidence reference and date.")


@dataclass(frozen=True, slots=True)
class LearnerEligibilityEvidence:
    """Minimum optional facts; None means not supplied and an empty tuple means none reported.

    Age is stored only as completed years, never as a date of birth. Experience is one
    non-overlapping total per industry category, not a sum of potentially overlapping jobs.
    """

    education_level: EducationLevel = EducationLevel.UNKNOWN
    age_in_completed_years: int | None = None
    prior_qualifications: tuple[PriorQualificationEvidence, ...] | None = None
    relevant_experience: tuple[RelevantExperienceEvidence, ...] | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.education_level, EducationLevel):
            raise ValueError("education_level must use a normalized EducationLevel value.")
        if self.age_in_completed_years is not None:
            age = self.age_in_completed_years
            if isinstance(age, bool) or not isinstance(age, int) or not 0 <= age <= 120:
                raise ValueError("age_in_completed_years must be an integer between 0 and 120.")
        if self.prior_qualifications is not None:
            prior = tuple(self.prior_qualifications)
            if any(not isinstance(item, PriorQualificationEvidence) for item in prior):
                raise ValueError("prior_qualifications must contain prior qualification evidence.")
            keys = [(item.qualification_code, item.qualification_version) for item in prior]
            if len(keys) != len(set(keys)):
                raise ValueError("Prior qualification evidence cannot contain duplicate records.")
            object.__setattr__(self, "prior_qualifications", prior)
        if self.relevant_experience is not None:
            experience = tuple(self.relevant_experience)
            if any(not isinstance(item, RelevantExperienceEvidence) for item in experience):
                raise ValueError("relevant_experience must contain experience evidence.")
            codes = [item.industry_code for item in experience]
            if len(codes) != len(set(codes)):
                raise ValueError("Experience evidence needs one non-overlapping total per industry.")
            object.__setattr__(self, "relevant_experience", experience)


@dataclass(frozen=True, slots=True)
class ConditionEvaluation:
    condition_id: str
    condition_kind: str
    status: EligibilityStatus
    reason_code: str
    explanation_en: str
    explanation_mr: str
    missing_information: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RouteEvaluation:
    route_id: str
    status: EligibilityStatus
    conditions: tuple[ConditionEvaluation, ...]


@dataclass(frozen=True, slots=True)
class MultiRouteEligibilityResult:
    status: EligibilityStatus
    reason_code: str
    explanation_en: str
    explanation_mr: str
    qualification_code: str
    qualification_version: str
    route_evaluations: tuple[RouteEvaluation, ...]
    missing_information: tuple[str, ...]
    source_publisher: str
    source_url: str
    source_reference: str
    last_verified_at: date | None
    valid_until: date | None
    scope: str = "advisory_entry_route_screening"
    admission_decision: bool = False


def _unknown(
    condition_id: str,
    kind: str,
    reason: str,
    missing: tuple[str, ...],
    en: str,
    mr: str,
) -> ConditionEvaluation:
    return ConditionEvaluation(
        condition_id=condition_id,
        condition_kind=kind,
        status=EligibilityStatus.UNKNOWN,
        reason_code=reason,
        explanation_en=en,
        explanation_mr=mr,
        missing_information=missing,
    )


def _evaluate_condition(
    condition: EntryCondition,
    evidence: LearnerEligibilityEvidence,
    *,
    as_of: date,
) -> ConditionEvaluation:
    if not condition.source.is_current(as_of):
        return _unknown(
            condition.condition_id,
            type(condition).__name__,
            "criterion_source_not_current",
            (f"current verified source for {condition.condition_id}",),
            "This published condition is not backed by a current verified source.",
            "या प्रकाशित अटीसाठी सध्याचा पडताळलेला स्रोत उपलब्ध नाही.",
        )

    if isinstance(condition, EducationLevelCondition):
        if evidence.education_level == EducationLevel.UNKNOWN:
            return _unknown(
                condition.condition_id,
                "education_level",
                "education_level_not_provided",
                ("highest completed education level",),
                "The learner's highest completed education level has not been provided.",
                "विद्यार्थ्याने पूर्ण केलेल्या सर्वोच्च शिक्षणाची माहिती दिलेली नाही.",
            )
        labels_en = {
            EducationLevel.BELOW_GRADE_8: "below Grade 8",
            EducationLevel.GRADE_8: "Grade 8",
            EducationLevel.GRADE_10: "Grade 10",
            EducationLevel.GRADE_12: "Grade 12",
            EducationLevel.ITI_OR_VOCATIONAL: "ITI or vocational qualification",
            EducationLevel.DIPLOMA: "Diploma",
            EducationLevel.GRADUATE: "Graduate",
            EducationLevel.OTHER: "Other",
        }
        labels_mr = {
            EducationLevel.BELOW_GRADE_8: "इयत्ता ८ वी पेक्षा कमी",
            EducationLevel.GRADE_8: "इयत्ता ८ वी",
            EducationLevel.GRADE_10: "इयत्ता १० वी",
            EducationLevel.GRADE_12: "इयत्ता १२ वी",
            EducationLevel.ITI_OR_VOCATIONAL: "आयटीआय किंवा व्यावसायिक पात्रता",
            EducationLevel.DIPLOMA: "डिप्लोमा",
            EducationLevel.GRADUATE: "पदवीधर",
            EducationLevel.OTHER: "इतर",
        }
        level = evidence.education_level
        met = level in condition.accepted_levels
        status = EligibilityStatus.ELIGIBLE if met else EligibilityStatus.INELIGIBLE
        return ConditionEvaluation(
            condition_id=condition.condition_id,
            condition_kind="education_level",
            status=status,
            reason_code="education_requirement_met" if met else "education_requirement_not_met",
            explanation_en=(
                f"Recorded education ({labels_en[level]}) meets this route's published requirement."
                if met
                else f"Recorded education ({labels_en[level]}) does not meet this route's published requirement."
            ),
            explanation_mr=(
                f"नोंदवलेले शिक्षण ({labels_mr[level]}) या मार्गाची प्रकाशित अट पूर्ण करते."
                if met
                else f"नोंदवलेले शिक्षण ({labels_mr[level]}) या मार्गाची प्रकाशित अट पूर्ण करत नाही."
            ),
        )

    if isinstance(condition, MinimumAgeCondition):
        age = evidence.age_in_completed_years
        if age is None:
            return _unknown(
                condition.condition_id,
                "minimum_age",
                "age_not_provided",
                ("age in completed years",),
                "Age in completed years is needed; no date of birth is collected.",
                "पूर्ण झालेल्या वर्षांतील वय आवश्यक आहे; जन्मतारीख गोळा केली जात नाही.",
            )
        met = age >= condition.minimum_years
        status = EligibilityStatus.ELIGIBLE if met else EligibilityStatus.INELIGIBLE
        return ConditionEvaluation(
            condition_id=condition.condition_id,
            condition_kind="minimum_age",
            status=status,
            reason_code="minimum_age_met" if met else "minimum_age_not_met",
            explanation_en=(
                f"Reported age ({age} years) meets the published minimum of "
                f"{condition.minimum_years} years; the provider may verify it."
                if met
                else f"Reported age ({age} years) is below the published minimum of "
                f"{condition.minimum_years} years."
            ),
            explanation_mr=(
                f"सांगितलेले वय ({age} वर्षे) प्रकाशित किमान {condition.minimum_years} "
                "वर्षांची अट पूर्ण करते; प्रशिक्षण केंद्र पडताळणी करू शकते."
                if met
                else f"सांगितलेले वय ({age} वर्षे) प्रकाशित किमान "
                f"{condition.minimum_years} वर्षांपेक्षा कमी आहे."
            ),
        )

    if isinstance(condition, PriorNSQFCondition):
        prior = evidence.prior_qualifications
        if prior is None:
            return _unknown(
                condition.condition_id,
                "prior_nsqf",
                "prior_qualification_not_provided",
                ("verified relevant prior NSQF qualification and level",),
                "A prior qualification record is needed to confirm NSQF level and relevance.",
                "NSQF स्तर आणि संबंधितता तपासण्यासाठी आधीच्या पात्रतेची माहिती आवश्यक आहे.",
            )
        unresolved = False
        for item in prior:
            if (
                item.verification_status != CriteriaVerificationStatus.VERIFIED
                or item.source is None
                or not item.source.is_current(as_of)
                or item.relevance_status == PriorQualificationRelevance.UNKNOWN
            ):
                unresolved = True
                continue
            if item.relevance_status == PriorQualificationRelevance.VERIFIED_RELEVANT:
                if item.nsqf_level >= condition.minimum_level:
                    return ConditionEvaluation(
                        condition_id=condition.condition_id,
                        condition_kind="prior_nsqf",
                        status=EligibilityStatus.ELIGIBLE,
                        reason_code="verified_relevant_prior_nsqf_met",
                        explanation_en=(
                            f"A verified relevant prior qualification at NSQF level "
                            f"{item.nsqf_level} meets the minimum level {condition.minimum_level}."
                        ),
                        explanation_mr=(
                            f"NSQF स्तर {item.nsqf_level} ची पडताळलेली संबंधित पूर्व-पात्रता "
                            f"किमान {condition.minimum_level} स्तराची अट पूर्ण करते."
                        ),
                    )
        if unresolved:
            return _unknown(
                condition.condition_id,
                "prior_nsqf",
                "prior_qualification_needs_verification",
                ("verification and relevance of prior NSQF qualification",),
                "A prior qualification or its relevance is missing or not verified.",
                "पूर्व-पात्रता किंवा तिची संबंधितता उपलब्ध नाही किंवा पडताळलेली नाही.",
            )
        return ConditionEvaluation(
            condition_id=condition.condition_id,
            condition_kind="prior_nsqf",
            status=EligibilityStatus.INELIGIBLE,
            reason_code="verified_relevant_prior_nsqf_not_met",
            explanation_en=(
                f"No verified relevant prior qualification at NSQF level "
                f"{condition.minimum_level} or above was recorded."
            ),
            explanation_mr=(
                f"NSQF स्तर {condition.minimum_level} किंवा त्यापेक्षा उच्च स्तराची "
                "पडताळलेली संबंधित पूर्व-पात्रता नोंदलेली नाही."
            ),
        )

    if isinstance(condition, RelevantExperienceCondition):
        experience = evidence.relevant_experience
        if experience is None:
            return _unknown(
                condition.condition_id,
                "relevant_experience",
                "relevant_experience_not_provided",
                (f"verified {condition.industry_label_en} experience in months",),
                f"Verified {condition.industry_label_en} experience is needed.",
                f"पडताळलेला {condition.industry_label_mr} अनुभव आवश्यक आहे.",
            )
        matching = [item for item in experience if item.industry_code == condition.industry_code]
        if not matching:
            return ConditionEvaluation(
                condition_id=condition.condition_id,
                condition_kind="relevant_experience",
                status=EligibilityStatus.INELIGIBLE,
                reason_code="relevant_experience_not_recorded",
                explanation_en=f"No {condition.industry_label_en} experience was reported.",
                explanation_mr=f"{condition.industry_label_mr} अनुभव नोंदवलेला नाही.",
            )
        item = matching[0]
        if (
            item.verification_status != CriteriaVerificationStatus.VERIFIED
            or item.last_verified_at is None
            or item.last_verified_at > as_of
            or not item.evidence_reference
        ):
            return _unknown(
                condition.condition_id,
                "relevant_experience",
                "relevant_experience_needs_verification",
                (f"verification of {condition.industry_label_en} experience",),
                f"The reported {condition.industry_label_en} experience is not verified.",
                f"सांगितलेला {condition.industry_label_mr} अनुभव पडताळलेला नाही.",
            )
        met = item.months >= condition.minimum_months
        status = EligibilityStatus.ELIGIBLE if met else EligibilityStatus.INELIGIBLE
        return ConditionEvaluation(
            condition_id=condition.condition_id,
            condition_kind="relevant_experience",
            status=status,
            reason_code="relevant_experience_met" if met else "relevant_experience_not_met",
            explanation_en=(
                f"Verified {condition.industry_label_en} experience ({item.months} months) "
                f"meets the {condition.minimum_months}-month requirement."
                if met
                else f"Verified {condition.industry_label_en} experience ({item.months} months) "
                f"is below the {condition.minimum_months}-month requirement."
            ),
            explanation_mr=(
                f"पडताळलेला {condition.industry_label_mr} अनुभव ({item.months} महिने) "
                f"{condition.minimum_months} महिन्यांची अट पूर्ण करतो."
                if met
                else f"पडताळलेला {condition.industry_label_mr} अनुभव ({item.months} महिने) "
                f"{condition.minimum_months} महिन्यांपेक्षा कमी आहे."
            ),
        )

    raise TypeError(f"Unsupported entry condition: {type(condition).__name__}")


def _route_status(conditions: tuple[ConditionEvaluation, ...]) -> EligibilityStatus:
    statuses = tuple(item.status for item in conditions)
    if all(status == EligibilityStatus.ELIGIBLE for status in statuses):
        return EligibilityStatus.ELIGIBLE
    if all(status != EligibilityStatus.UNKNOWN for status in statuses):
        return EligibilityStatus.INELIGIBLE
    return EligibilityStatus.UNKNOWN


def evaluate_multi_route_eligibility(
    evidence: LearnerEligibilityEvidence,
    criteria: MultiRouteQualificationCriteria,
    *,
    as_of: date | None = None,
) -> MultiRouteEligibilityResult:
    """Evaluate OR routes with AND conditions; missing or unverified facts stay unknown."""
    today = as_of or date.today()
    criteria_current = criteria.source.is_current(today) and (
        criteria.valid_until is None or criteria.valid_until >= today
    )
    evaluations: list[RouteEvaluation] = []
    for route in criteria.routes:
        if criteria_current:
            conditions = tuple(
                _evaluate_condition(condition, evidence, as_of=today)
                for condition in route.conditions
            )
        else:
            conditions = tuple(
                _unknown(
                    condition.condition_id,
                    type(condition).__name__,
                    "qualification_criteria_not_current",
                    ("current verified qualification criteria",),
                    "The qualification criteria are expired or not currently verified.",
                    "पात्रतेचे निकष कालबाह्य आहेत किंवा सध्या पडताळलेले नाहीत.",
                )
                for condition in route.conditions
            )
        evaluations.append(
            RouteEvaluation(
                route_id=route.route_id,
                status=_route_status(conditions),
                conditions=conditions,
            )
        )

    routes = tuple(evaluations)
    if any(route.status == EligibilityStatus.ELIGIBLE for route in routes):
        status = EligibilityStatus.ELIGIBLE
        reason = "at_least_one_complete_route_met"
        en = (
            "At least one complete published entry route is met by the supplied information. "
            "This is advisory screening, not an admission decision."
        )
        mr = (
            "दिलेल्या माहितीनुसार पात्रतेचा किमान एक पूर्ण प्रकाशित मार्ग पूर्ण होतो. "
            "ही प्राथमिक माहिती आहे; प्रवेशाचा अंतिम निर्णय नाही."
        )
    elif all(route.status == EligibilityStatus.INELIGIBLE for route in routes):
        status = EligibilityStatus.INELIGIBLE
        reason = "all_routes_fully_evaluated_and_not_met"
        en = (
            "Every published entry route was fully evaluated and at least one required "
            "condition failed in each route. Confirm equivalence with the awarding body "
            "or provider before ruling out the qualification."
        )
        mr = (
            "प्रत्येक प्रकाशित प्रवेश मार्ग तपासला गेला आणि प्रत्येक मार्गातील किमान एक "
            "आवश्यक अट पूर्ण झाली नाही. पात्रता नाकारण्यापूर्वी प्रमाणपत्र देणाऱ्या "
            "संस्थेकडून किंवा प्रशिक्षण केंद्राकडून समतुल्यता तपासा."
        )
    else:
        status = EligibilityStatus.UNKNOWN
        reason = (
            "qualification_criteria_not_current"
            if not criteria_current
            else "one_or_more_routes_need_more_information"
        )
        en = (
            "The available information is not sufficient to evaluate every alternative "
            "entry route. Missing or unverified details remain unknown; no route is assumed."
        )
        mr = (
            "प्रवेशाचे सर्व पर्यायी मार्ग तपासण्यासाठी उपलब्ध माहिती अपुरी आहे. "
            "गहाळ किंवा अपडताळलेली माहिती अज्ञात ठेवली आहे; कोणताही मार्ग गृहित धरलेला नाही."
        )

    missing = tuple(
        dict.fromkeys(
            item
            for route in routes
            for condition in route.conditions
            for item in condition.missing_information
        )
    )
    return MultiRouteEligibilityResult(
        status=status,
        reason_code=reason,
        explanation_en=en,
        explanation_mr=mr,
        qualification_code=criteria.qualification_code,
        qualification_version=criteria.qualification_version,
        route_evaluations=routes,
        missing_information=missing,
        source_publisher=criteria.source.publisher,
        source_url=criteria.source.url,
        source_reference=criteria.source.reference,
        last_verified_at=criteria.source.last_verified_at,
        valid_until=criteria.valid_until,
    )
