"""Cross-flow acceptance tests for the Phase 3 learner/family journey."""

from __future__ import annotations

from copy import deepcopy
from datetime import date

import pytest

from app.counselling_flow import (
    COUNSELLING_COPY,
    PROMPTS,
    record_response,
    render_joint_counselling,
)
from app.pathway_flow import DEMO_PATHWAYS
from app.profile_flow import PROFILE_COPY, build_family_context
from core.eligibility import EligibilityStatus
from core.multi_route_eligibility import (
    LearnerEligibilityEvidence,
    evaluate_multi_route_eligibility,
)
from core.pathways import ShortlistState, build_pathway_shortlist
from core.profiles import ConcernCategory, EducationLevel
from services.eligibility_catalogue import load_assistant_baking_technician_entry_criteria


class ReviewStreamlit:
    """Capture the review surface without creating a browser or external service."""

    def __init__(self, state: dict) -> None:
        self.session_state = state
        self.calls: list[tuple[str, tuple, dict]] = []

    def __getattr__(self, name: str):
        def record(*args, **kwargs):
            self.calls.append((name, args, kwargs))
            if name == "button":
                return False
            return None

        return record


def _rendered_text(fake: ReviewStreamlit) -> str:
    return " ".join(
        str(value)
        for _, args, _ in fake.calls
        for value in args
    )


@pytest.mark.parametrize("locale", ["English", "मराठी"])
def test_phase3_session_journey_preserves_learner_and_parent_boundaries(
    locale: str,
) -> None:
    """Profile, advisory matching, eligibility and family review share no role data."""
    profile_state = {
        "profile_education_level": EducationLevel.GRADE_10,
        "profile_state_code": "MH",
        "profile_interests": ["technology"],
        "profile_work_preferences": ["hands_on"],
        "profile_parent_concerns": [ConcernCategory.WORKPLACE_SAFETY],
        "profile_parent_priorities": ["learner_choice"],
    }
    context = build_family_context(profile_state, locale)

    assert context.learner.learner_ref != context.parent.participant_ref
    assert context.parent.concerns == (ConcernCategory.WORKPLACE_SAFETY,)

    shortlist = build_pathway_shortlist(context.learner, DEMO_PATHWAYS)
    assert shortlist.state == ShortlistState.MATCHES_NEED_VERIFICATION
    assert shortlist.shortlist == ()
    assert shortlist.needs_verification
    assert len(shortlist.all_options) == len(DEMO_PATHWAYS)
    assert all(
        item.eligibility.status == EligibilityStatus.UNKNOWN
        for item in shortlist.all_options
    )
    reason_codes = {
        reason
        for item in shortlist.all_options
        for reason in item.reason_codes
    }
    assert reason_codes <= {"interest:technology", "work_preference:hands_on"}
    assert not any("workplace_safety" in reason for reason in reason_codes)

    criteria = load_assistant_baking_technician_entry_criteria()
    eligibility = evaluate_multi_route_eligibility(
        LearnerEligibilityEvidence(education_level=context.learner.education_level),
        criteria,
        as_of=date(2026, 11, 23),
    )
    assert eligibility.status == EligibilityStatus.UNKNOWN
    assert eligibility.admission_decision is False
    assert "age in completed years" in eligibility.missing_information

    state = {
        "joint_counselling_step": len(PROMPTS),
        "profile_saved_context": context,
    }
    record_response(state, "parent_reported_concerns", ["income_evidence"])
    record_response(state, "learner_next_step", ["take_time"])
    answers_before_review = deepcopy(state["joint_counselling_answers"])

    fake = ReviewStreamlit(state)
    render_joint_counselling(fake, locale)
    rendered = _rendered_text(fake)
    profile_copy = PROFILE_COPY[locale]
    conversation_copy = COUNSELLING_COPY[locale]

    assert conversation_copy["profile_context_learner"] in rendered
    assert conversation_copy["profile_context_parent"] in rendered
    assert profile_copy["education_labels"][EducationLevel.GRADE_10] in rendered
    assert profile_copy["interest_labels"]["technology"] in rendered
    assert profile_copy["work_preference_labels"]["hands_on"] in rendered
    assert (
        profile_copy["concern_labels"][ConcernCategory.WORKPLACE_SAFETY]
        in rendered
    )
    assert profile_copy["priority_labels"]["learner_choice"] in rendered
    assert (
        conversation_copy["option_labels"]["parent_reported_concerns"][
            "income_evidence"
        ]
        in rendered
    )
    assert (
        conversation_copy["option_labels"]["learner_next_step"]["take_time"]
        in rendered
    )
    assert state["joint_counselling_answers"] == answers_before_review
    assert state["profile_saved_context"] == context
