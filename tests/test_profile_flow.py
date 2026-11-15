"""Integration-style tests for the bilingual, session-only guided profile flow."""

from __future__ import annotations

from core.profiles import (
    ConcernCategory,
    EducationLevel,
    PreferredLanguage,
)
from app.profile_flow import (
    PROFILE_COPY,
    PROFILE_STEPS,
    build_family_context,
    render_profile_capture,
)


class FakeStreamlit:
    def __init__(self, *, state: dict | None = None, clicked: str | None = None) -> None:
        self.session_state = state if state is not None else {}
        self.clicked = clicked
        self.calls: list[tuple[str, tuple, dict]] = []
        self.buttons: list[str] = []

    def progress(self, *args, **kwargs) -> None:
        self.calls.append(("progress", args, kwargs))

    def subheader(self, *args, **kwargs) -> None:
        self.calls.append(("subheader", args, kwargs))

    def caption(self, *args, **kwargs) -> None:
        self.calls.append(("caption", args, kwargs))

    def info(self, *args, **kwargs) -> None:
        self.calls.append(("info", args, kwargs))

    def success(self, *args, **kwargs) -> None:
        self.calls.append(("success", args, kwargs))

    def write(self, *args, **kwargs) -> None:
        self.calls.append(("write", args, kwargs))

    def selectbox(self, label: str, *, options, index: int = 0, format_func=None, key: str):
        self.calls.append(("selectbox", (label,), {"options": options, "key": key}))
        if key not in self.session_state:
            self.session_state[key] = options[index]
        return self.session_state[key]

    def multiselect(self, label: str, *, options, format_func=None, key: str):
        self.calls.append(("multiselect", (label,), {"options": options, "key": key}))
        self.session_state.setdefault(key, [])
        return self.session_state[key]

    def button(self, label: str, **kwargs):
        self.buttons.append(label)
        self.calls.append(("button", (label,), kwargs))
        if label == self.clicked and kwargs.get("on_click"):
            kwargs["on_click"](*kwargs.get("args", ()))
        return label == self.clicked


def test_both_locales_have_complete_profile_copy() -> None:
    english = PROFILE_COPY["English"]
    marathi = PROFILE_COPY["मराठी"]

    assert set(english) == set(marathi)
    assert len(english["step_titles"]) == len(PROFILE_STEPS) == 7
    assert len(english["step_help"]) == len(PROFILE_STEPS)


def test_each_step_asks_one_question_in_both_languages() -> None:
    for locale in PROFILE_COPY:
        for step in range(6):
            fake = FakeStreamlit(state={"profile_capture_step": step})
            render_profile_capture(fake, locale)
            inputs = [call for call in fake.calls if call[0] in {"selectbox", "multiselect"}]
            assert len(inputs) == 1
            assert fake.calls[1][1][0] == PROFILE_COPY[locale]["step_titles"][step]


def test_back_and_continue_change_only_the_guided_step() -> None:
    back = FakeStreamlit(
        state={"profile_capture_step": 3},
        clicked=PROFILE_COPY["English"]["back"],
    )
    render_profile_capture(back, "English")
    assert back.session_state["profile_capture_step"] == 2

    forward = FakeStreamlit(
        state={"profile_capture_step": 2},
        clicked=PROFILE_COPY["English"]["next"],
    )
    render_profile_capture(forward, "English")
    assert forward.session_state["profile_capture_step"] == 3


def test_learner_and_parent_answers_remain_role_separated() -> None:
    state = {
        "profile_education_level": EducationLevel.GRADE_10,
        "profile_state_code": "MH",
        "profile_interests": ["technology", "design_and_creativity"],
        "profile_work_preferences": ["hands_on"],
        "profile_parent_concerns": [
            ConcernCategory.WORKPLACE_SAFETY,
            ConcernCategory.INCOME,
        ],
        "profile_parent_priorities": ["affordable_training", "learner_choice"],
    }

    context = build_family_context(state, "English")

    assert context.learner.education_level == EducationLevel.GRADE_10
    assert context.learner.interests == ("technology", "design_and_creativity")
    assert context.learner.work_preferences == ("hands_on",)
    assert context.parent.concerns == (
        ConcernCategory.WORKPLACE_SAFETY,
        ConcernCategory.INCOME,
    )
    assert context.parent.priorities == ("affordable_training", "learner_choice")
    assert context.learner.learner_ref != context.parent.participant_ref
    assert context.learner.state_code == "MH"
    assert context.learner.household_income_band_code is None


def test_optional_and_unknown_answers_remain_unknown() -> None:
    context = build_family_context({}, "English")

    assert context.learner.education_level == EducationLevel.UNKNOWN
    assert context.learner.state_code is None
    assert context.learner.household_income_band_code is None
    assert context.learner.interests == ()
    assert context.learner.work_preferences == ()
    assert context.parent.concerns == ()
    assert context.parent.priorities == ()


def test_marathi_locale_is_preserved_in_both_participant_records() -> None:
    context = build_family_context({}, "मराठी")

    assert context.learner.preferred_language == PreferredLanguage.MARATHI
    assert context.parent.preferred_language == PreferredLanguage.MARATHI


def test_review_save_keeps_draft_only_in_session_state() -> None:
    state = {
        "profile_capture_step": 6,
        "profile_education_level": EducationLevel.GRADE_12,
        "profile_interests": ["health_and_care"],
        "profile_parent_concerns": [ConcernCategory.PLACEMENT_AND_JOB_SECURITY],
    }
    fake = FakeStreamlit(state=state, clicked=PROFILE_COPY["English"]["save"])

    render_profile_capture(fake, "English")

    saved = fake.session_state["profile_saved_context"]
    assert saved.learner.education_level == EducationLevel.GRADE_12
    assert saved.learner.interests == ("health_and_care",)
    assert saved.parent.concerns == (ConcernCategory.PLACEMENT_AND_JOB_SECURITY,)
    assert any(call[0] == "success" for call in fake.calls)
    button_calls = [call for call in fake.calls if call[0] == "button"]
    assert button_calls
    assert all(call[2]["use_container_width"] is True for call in button_calls)
    assert not any(call[0] in {"form_submit_button", "download_button"} for call in fake.calls)


def test_region_step_does_not_collect_income_or_exact_location() -> None:
    fake = FakeStreamlit(state={"profile_capture_step": 1})
    render_profile_capture(fake, "English")

    inputs = [call for call in fake.calls if call[0] in {"selectbox", "multiselect"}]
    assert len(inputs) == 1
    assert inputs[0][2]["key"] == "profile_state_code"
    rendered = " ".join(
        str(argument) for _, args, _ in fake.calls for argument in args
    ).lower()
    assert "income bands are not collected" in rendered
