"""Tests for bilingual rendering of the advisory pathway explorer."""

from app.pathway_flow import DEMO_PATHWAYS, PATHWAY_COPY, render_pathway_explorer
from core.profiles import ConcernCategory


class FakeStreamlit:
    def __init__(self, state: dict | None = None) -> None:
        self.session_state = state if state is not None else {}
        self.calls: list[tuple[str, tuple, dict]] = []

    def __getattr__(self, name: str):
        def record(*args, **kwargs):
            self.calls.append((name, args, kwargs))
        return record


def rendered_text(fake: FakeStreamlit) -> str:
    return " ".join(
        str(value)
        for _, args, _ in fake.calls
        for value in args
    )


def test_bilingual_pathway_copy_has_matching_keys() -> None:
    assert set(PATHWAY_COPY["English"]) == set(PATHWAY_COPY["मराठी"])


def test_empty_profile_keeps_every_demo_option_available_in_english() -> None:
    fake = FakeStreamlit()

    render_pathway_explorer(fake, "English")

    text = rendered_text(fake)
    assert PATHWAY_COPY["English"]["no_preferences"] in text
    assert PATHWAY_COPY["English"]["synthetic_label"] in text
    assert len(DEMO_PATHWAYS) == 4
    for item in DEMO_PATHWAYS:
        assert item.course.title in text
    assert PATHWAY_COPY["English"]["eligibility_status"]["unknown"] in text


def test_learner_preferences_drive_shortlist_but_parent_concerns_stay_separate() -> None:
    fake = FakeStreamlit(
        {
            "profile_interests": ["technology"],
            "profile_work_preferences": [],
            "profile_parent_concerns": [ConcernCategory.WORKPLACE_SAFETY],
            "profile_parent_priorities": ["workplace_safety"],
        }
    )

    render_pathway_explorer(fake, "English")

    text = rendered_text(fake)
    assert PATHWAY_COPY["English"]["verification_heading"] in text
    assert PATHWAY_COPY["English"]["verification_notice"] in text
    assert "Illustrative technology-support theme" in text
    assert "Illustrative repair and maintenance theme" in text
    assert "workplace safety" not in text.lower()
    assert PATHWAY_COPY["English"]["learner_agency"] in text


def test_marathi_explorer_shows_all_options_and_unknown_eligibility() -> None:
    fake = FakeStreamlit(
        {
            "profile_interests": ["design_and_creativity"],
            "profile_work_preferences": ["computer_based"],
        }
    )

    render_pathway_explorer(fake, "मराठी")

    text = rendered_text(fake)
    assert PATHWAY_COPY["मराठी"]["verification_heading"] in text
    assert PATHWAY_COPY["मराठी"]["verification_notice"] in text
    assert PATHWAY_COPY["मराठी"]["eligibility_status"]["unknown"] in text
    assert PATHWAY_COPY["मराठी"]["synthetic_label"] in text
    for item in DEMO_PATHWAYS:
        assert item.display_title_mr in text


def test_no_match_still_renders_full_exploration_list() -> None:
    fake = FakeStreamlit({"profile_interests": ["agriculture_and_nature"]})

    render_pathway_explorer(
        fake,
        "English",
        pathways=(DEMO_PATHWAYS[0], DEMO_PATHWAYS[2]),
    )

    text = rendered_text(fake)
    assert PATHWAY_COPY["English"]["no_matches"] in text
    assert DEMO_PATHWAYS[0].course.title in text
    assert DEMO_PATHWAYS[2].course.title in text
