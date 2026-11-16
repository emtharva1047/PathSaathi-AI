"""Deterministic, preference-led pathway shortlisting with no aptitude scoring."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

from core.domain import CourseRecord
from core.eligibility import EligibilityResult, QualificationEntryCriteria, evaluate_eligibility
from core.profiles import LearnerProfile


SUPPORTED_INTEREST_TAGS = frozenset(
    {
        "technology",
        "repair_and_making",
        "design_and_creativity",
        "health_and_care",
        "agriculture_and_nature",
        "business_and_services",
        "working_with_people",
    }
)
SUPPORTED_WORK_PREFERENCE_TAGS = frozenset(
    {
        "hands_on",
        "computer_based",
        "outdoor",
        "indoor",
        "people_facing",
        "independent_work",
    }
)

_SIGNAL_LABELS = {
    "en": {
        "technology": "technology",
        "repair_and_making": "repairing and making",
        "design_and_creativity": "design and creative work",
        "health_and_care": "health and care",
        "agriculture_and_nature": "agriculture and nature",
        "business_and_services": "business and services",
        "working_with_people": "working with people",
        "hands_on": "hands-on work",
        "computer_based": "computer-based work",
        "outdoor": "outdoor work",
        "indoor": "indoor work",
        "people_facing": "working with people or customers",
        "independent_work": "independent work",
    },
    "mr": {
        "technology": "तंत्रज्ञान",
        "repair_and_making": "दुरुस्ती आणि वस्तू तयार करणे",
        "design_and_creativity": "डिझाइन आणि सर्जनशील काम",
        "health_and_care": "आरोग्य आणि काळजी सेवा",
        "agriculture_and_nature": "शेती आणि निसर्ग",
        "business_and_services": "व्यवसाय आणि सेवा",
        "working_with_people": "लोकांसोबत काम",
        "hands_on": "प्रत्यक्ष हाताने करायचे काम",
        "computer_based": "संगणकावर आधारित काम",
        "outdoor": "बाहेरचे काम",
        "indoor": "घरातील किंवा कार्यालयातील काम",
        "people_facing": "लोक किंवा ग्राहकांसोबत काम",
        "independent_work": "स्वतंत्रपणे काम",
    },
}


class ShortlistState(StrEnum):
    """Exploration state; never interpreted as a judgement about the learner."""

    MATCHES_AVAILABLE = "matches_available"
    NO_PREFERENCES = "no_preferences"
    NO_MATCHES = "no_matches"
    NO_CATALOGUE = "no_catalogue"


@dataclass(frozen=True, slots=True)
class AdvisoryPathway:
    """A catalogue item plus explicit, reviewed preference tags and optional criteria."""

    course: CourseRecord
    display_title_mr: str
    display_trade_mr: str
    interest_tags: tuple[str, ...] = ()
    work_preference_tags: tuple[str, ...] = ()
    entry_criteria: QualificationEntryCriteria | None = None

    def __post_init__(self) -> None:
        if not self.display_title_mr.strip() or not self.display_trade_mr.strip():
            raise ValueError("Marathi display labels cannot be blank.")

        interest_tags = _normalise_tags(
            self.interest_tags, SUPPORTED_INTEREST_TAGS, "interest_tags"
        )
        work_tags = _normalise_tags(
            self.work_preference_tags,
            SUPPORTED_WORK_PREFERENCE_TAGS,
            "work_preference_tags",
        )
        if not interest_tags and not work_tags:
            raise ValueError("A pathway needs at least one explicit preference tag.")

        object.__setattr__(self, "interest_tags", interest_tags)
        object.__setattr__(self, "work_preference_tags", work_tags)

        if self.entry_criteria is not None:
            if not self.course.has_verified_source:
                raise ValueError(
                    "Qualification criteria can only be attached to a source-verified course."
                )
            if self.course.qualification_code != self.entry_criteria.qualification_code:
                raise ValueError("Course and qualification criteria codes must match.")


@dataclass(frozen=True, slots=True)
class PathwayRecommendation:
    """One option with exact preference overlaps and a separate eligibility result."""

    pathway: AdvisoryPathway
    matched_interests: tuple[str, ...]
    matched_work_preferences: tuple[str, ...]
    reason_codes: tuple[str, ...]
    explanation_en: str
    explanation_mr: str
    eligibility: EligibilityResult

    @property
    def matches_preferences(self) -> bool:
        """Whether at least one explicitly selected learner signal matched."""
        return bool(self.reason_codes)


@dataclass(frozen=True, slots=True)
class ShortlistResult:
    """All options remain available, whether shortlisted or not."""

    state: ShortlistState
    shortlist: tuple[PathwayRecommendation, ...]
    explore_all: tuple[PathwayRecommendation, ...]
    all_options: tuple[PathwayRecommendation, ...]


def _normalise_tags(
    values: tuple[str, ...],
    allowed: frozenset[str],
    field_name: str,
) -> tuple[str, ...]:
    items = tuple(values)
    if any(not isinstance(value, str) for value in items):
        raise ValueError(f"{field_name} must contain text tags.")
    cleaned = tuple(value.strip().casefold() for value in items)
    if any(not value for value in cleaned):
        raise ValueError(f"{field_name} cannot contain blank tags.")
    if len(cleaned) != len(set(cleaned)):
        raise ValueError(f"{field_name} cannot contain duplicate tags.")
    unsupported = set(cleaned) - allowed
    if unsupported:
        raise ValueError(f"{field_name} contains unsupported tags: {sorted(unsupported)}")
    return cleaned


def _explanations(
    matched_interests: tuple[str, ...],
    matched_work_preferences: tuple[str, ...],
    has_learner_signals: bool,
) -> tuple[tuple[str, ...], str, str]:
    reason_codes = tuple(
        [f"interest:{tag}" for tag in matched_interests]
        + [f"work_preference:{tag}" for tag in matched_work_preferences]
    )
    if not reason_codes:
        if has_learner_signals:
            return (
                reason_codes,
                "No selected learner interest or work preference matches this option. "
                "It remains available to explore.",
                "विद्यार्थ्याने निवडलेल्या आवडी किंवा कामाच्या आवडी या पर्यायाशी जुळत नाहीत. "
                "तरीही हा पर्याय पाहण्यासाठी उपलब्ध आहे.",
            )
        return (
            reason_codes,
            "No learner interests or work preferences were shared. Explore this option "
            "without a preference match.",
            "विद्यार्थ्याच्या आवडी किंवा कामाच्या आवडी दिलेल्या नाहीत. जुळणी गृहित न धरता "
            "हा पर्याय पाहता येईल.",
        )

    english_signals = [
        f"interest: {_SIGNAL_LABELS['en'][tag]}" for tag in matched_interests
    ] + [
        f"work preference: {_SIGNAL_LABELS['en'][tag]}"
        for tag in matched_work_preferences
    ]
    marathi_signals = [
        f"आवड: {_SIGNAL_LABELS['mr'][tag]}" for tag in matched_interests
    ] + [
        f"कामाची आवड: {_SIGNAL_LABELS['mr'][tag]}"
        for tag in matched_work_preferences
    ]
    return (
        reason_codes,
        "Matches the learner's stated " + "; ".join(english_signals) + ".",
        "विद्यार्थ्याने सांगितलेल्या " + "; ".join(marathi_signals) + " यांच्याशी जुळतो.",
    )


def build_pathway_shortlist(
    learner: LearnerProfile,
    pathways: Iterable[AdvisoryPathway],
    *,
    max_shortlist: int = 5,
) -> ShortlistResult:
    """Match exact learner preference tags; never infer ability or restrict exploration.

    Parent concerns, parent priorities, education level, location and income are not
    preference-ranking signals. Education eligibility is evaluated separately from
    the shortlist and only from criteria attached to a source-verified course.
    """
    if isinstance(max_shortlist, bool) or not isinstance(max_shortlist, int):
        raise ValueError("max_shortlist must be an integer.")
    if not 1 <= max_shortlist <= 20:
        raise ValueError("max_shortlist must be between 1 and 20.")

    catalogue = tuple(pathways)
    identifiers = [item.course.course_id for item in catalogue]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Pathway course identifiers must be unique.")

    learner_interests = {value.strip().casefold() for value in learner.interests}
    learner_work_preferences = {
        value.strip().casefold() for value in learner.work_preferences
    }
    has_learner_signals = bool(learner_interests or learner_work_preferences)

    recommendations: list[PathwayRecommendation] = []
    for pathway in catalogue:
        matched_interests = tuple(
            tag for tag in pathway.interest_tags if tag in learner_interests
        )
        matched_work_preferences = tuple(
            tag for tag in pathway.work_preference_tags if tag in learner_work_preferences
        )
        reason_codes, explanation_en, explanation_mr = _explanations(
            matched_interests,
            matched_work_preferences,
            has_learner_signals,
        )
        criteria = (
            pathway.entry_criteria
            if pathway.course.has_verified_source
            else None
        )
        eligibility = evaluate_eligibility(learner, criteria)
        recommendations.append(
            PathwayRecommendation(
                pathway=pathway,
                matched_interests=matched_interests,
                matched_work_preferences=matched_work_preferences,
                reason_codes=reason_codes,
                explanation_en=explanation_en,
                explanation_mr=explanation_mr,
                eligibility=eligibility,
            )
        )

    recommendations.sort(
        key=lambda item: (
            not item.matches_preferences,
            -len(item.reason_codes),
            item.pathway.course.course_id.casefold(),
        )
    )
    all_options = tuple(recommendations)
    matching = tuple(item for item in all_options if item.matches_preferences)
    shortlist = matching[:max_shortlist]
    shortlisted_ids = {item.pathway.course.course_id for item in shortlist}
    explore_all = tuple(
        item
        for item in all_options
        if item.pathway.course.course_id not in shortlisted_ids
    )

    if not catalogue:
        state = ShortlistState.NO_CATALOGUE
    elif not has_learner_signals:
        state = ShortlistState.NO_PREFERENCES
    elif not matching:
        state = ShortlistState.NO_MATCHES
    else:
        state = ShortlistState.MATCHES_AVAILABLE

    return ShortlistResult(
        state=state,
        shortlist=shortlist,
        explore_all=explore_all,
        all_options=all_options,
    )
