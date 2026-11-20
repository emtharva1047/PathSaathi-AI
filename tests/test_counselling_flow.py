"""Tests for deterministic, role-separated joint counselling prompts."""

from __future__ import annotations

from app.counselling_flow import (
    COUNSELLING_COPY,
    PROMPTS,
    build_review,
    record_response,
    render_joint_counselling,
)


class FakeCounsellingStreamlit:
    """Small Streamlit test double with explicit button and widget state."""

    def __init__(
        self,
        *,
        state: dict | None = None,
        clicked_key: str | None = None,
        selected: list[str] | None = None,
    ) -> None:
        self.session_state = state if state is not None else {}
        self.clicked_key = clicked_key
        self.selected = selected
        self.calls: list[tuple[str, tuple, dict]] = []

    def progress(self, *args, **kwargs) -> None:
        self.calls.append(("progress", args, kwargs))

    def subheader(self, *args, **kwargs) -> None:
        self.calls.append(("subheader", args, kwargs))

    def caption(self, *args, **kwargs) -> None:
        self.calls.append(("caption", args, kwargs))

    def info(self, *args, **kwargs) -> None:
        self.calls.append(("info", args, kwargs))

    def write(self, *args, **kwargs) -> None:
        self.calls.append(("write", args, kwargs))

    def markdown(self, *args, **kwargs) -> None:
        self.calls.append(("markdown", args, kwargs))

    def success(self, *args, **kwargs) -> None:
        self.calls.append(("success", args, kwargs))

    def multiselect(self, label: str, *, options, format_func, key: str):
        self.calls.append(("multiselect", (label,), {"options": options, "key": key}))
        if self.selected is not None:
            self.session_state[key] = self.selected
        return self.session_state.get(key, [])

    def button(self, label: str, **kwargs) -> bool:
        self.calls.append(("button", (label,), kwargs))
        return kwargs.get("key") == self.clicked_key


def test_prompt_catalogues_match_and_marathi_is_explicitly_draft() -> None:
    english = COUNSELLING_COPY["English"]
    marathi = COUNSELLING_COPY["मराठी"]

    assert set(english) == set(marathi)
    assert set(english["prompt_titles"]) == {prompt.prompt_id for prompt in PROMPTS}
    assert set(english["prompt_questions"]) == {prompt.prompt_id for prompt in PROMPTS}
    assert set(english["option_labels"]) == {prompt.prompt_id for prompt in PROMPTS}
    for prompt in PROMPTS:
        assert set(english["option_labels"][prompt.prompt_id]) == set(prompt.options)
        assert set(marathi["option_labels"][prompt.prompt_id]) == set(prompt.options)
    assert "draft" in english["translation_status"].lower() or "prototype" in english["translation_status"].lower()
    assert "मसुदा" in marathi["translation_status"]


def test_prompts_distinguish_roles_and_question_types() -> None:
    assert [prompt.role for prompt in PROMPTS] == [
        "learner", "parent", "learner", "parent", "learner", "shared"
    ]
    assert {prompt.category for prompt in PROMPTS} == {
        "evidence_question", "self_reported_concern", "preference", "family_discussion"
    }


def test_answers_are_role_separated_and_do_not_overwrite_other_participant() -> None:
    state: dict = {}
    record_response(state, "learner_priorities", ["hands_on_learning"])
    record_response(state, "parent_reported_concerns", ["workplace_safety"])

    review = {item.prompt_id: item for item in build_review(state)}
    assert review["learner_priorities"].role == "learner"
    assert review["learner_priorities"].selected_values == ("hands_on_learning",)
    assert review["parent_reported_concerns"].role == "parent"
    assert review["parent_reported_concerns"].selected_values == ("workplace_safety",)
    assert state["joint_counselling_answers"]["learner_priorities"]["role"] != state[
        "joint_counselling_answers"
    ]["parent_reported_concerns"]["role"]


def test_empty_skipped_and_unanswered_states_remain_distinct() -> None:
    state: dict = {}
    record_response(state, "learner_evidence_questions", [])
    record_response(state, "parent_reported_concerns", skipped=True)

    review = {item.prompt_id: item for item in build_review(state)}
    assert review["learner_evidence_questions"].status == "empty"
    assert review["parent_reported_concerns"].status == "skipped"
    assert review["learner_priorities"].status == "not_answered"


def test_revised_answer_has_a_revision_count_and_keeps_its_role() -> None:
    state: dict = {}
    record_response(state, "learner_priorities", ["hands_on_learning"])
    record_response(state, "learner_priorities", ["computer_based_learning"])

    item = next(item for item in build_review(state) if item.prompt_id == "learner_priorities")
    assert item.status == "answered"
    assert item.selected_values == ("computer_based_learning",)
    assert item.revision_count == 1
    assert item.role == "learner"


def test_unknown_prompt_and_unknown_options_are_rejected_or_ignored() -> None:
    state: dict = {}
    record_response(state, "learner_priorities", ["not-a-real-option"])
    item = next(item for item in build_review(state) if item.prompt_id == "learner_priorities")
    assert item.status == "empty"
    assert item.selected_values == ()

    try:
        record_response(state, "unknown_prompt", ["anything"])
    except ValueError as error:
        assert "Unknown counselling prompt" in str(error)
    else:
        raise AssertionError("Unknown prompt identifiers must be rejected")


def test_one_short_question_is_rendered_at_a_time_in_both_locales() -> None:
    for locale in COUNSELLING_COPY:
        for index, prompt in enumerate(PROMPTS):
            fake = FakeCounsellingStreamlit(state={"joint_counselling_step": index})
            render_joint_counselling(fake, locale)
            inputs = [call for call in fake.calls if call[0] == "multiselect"]
            assert len(inputs) == 1
            assert inputs[0][2]["options"] == prompt.options
            rendered_questions = [
                args[0]
                for name, args, _ in fake.calls
                if name == "write" and args
            ]
            assert COUNSELLING_COPY[locale]["prompt_questions"][prompt.prompt_id] in rendered_questions


def test_skip_continue_and_back_navigation_save_only_the_current_prompt() -> None:
    first = PROMPTS[0]
    skip = FakeCounsellingStreamlit(
        state={"joint_counselling_step": 0},
        clicked_key=f"joint_counselling_skip_{first.prompt_id}",
    )
    render_joint_counselling(skip, "English")
    assert skip.session_state["joint_counselling_step"] == 1
    assert build_review(skip.session_state)[0].status == "skipped"

    second = PROMPTS[1]
    back = FakeCounsellingStreamlit(
        state={"joint_counselling_step": 1},
        clicked_key="joint_counselling_back",
        selected=["workplace_safety"],
    )
    render_joint_counselling(back, "English")
    assert back.session_state["joint_counselling_step"] == 0
    assert build_review(back.session_state)[1].selected_values == ("workplace_safety",)


def test_continue_with_no_selection_records_empty_and_advances() -> None:
    prompt = PROMPTS[0]
    fake = FakeCounsellingStreamlit(
        state={"joint_counselling_step": 0},
        clicked_key=f"joint_counselling_continue_{prompt.prompt_id}",
    )
    render_joint_counselling(fake, "English")
    assert fake.session_state["joint_counselling_step"] == 1
    assert build_review(fake.session_state)[0].status == "empty"


def test_review_allows_revision_and_preserves_learner_agency() -> None:
    review_state = {"joint_counselling_step": len(PROMPTS)}
    review = FakeCounsellingStreamlit(state=review_state)
    render_joint_counselling(review, "English")
    rendered = " ".join(
        str(value)
        for _, args, _ in review.calls
        for value in args
    )
    assert COUNSELLING_COPY["English"]["agency_note"] in rendered
    assert "Parent/guardian — self-reported" in rendered

    revise = FakeCounsellingStreamlit(
        state={"joint_counselling_step": len(PROMPTS)},
        clicked_key="joint_counselling_revise_learner_next_step",
    )
    render_joint_counselling(revise, "English")
    assert revise.session_state["joint_counselling_step"] == 4


def test_review_can_be_kept_only_in_session_and_has_no_external_writes() -> None:
    state = {"joint_counselling_step": len(PROMPTS)}
    fake = FakeCounsellingStreamlit(
        state=state,
        clicked_key="joint_counselling_keep",
    )
    render_joint_counselling(fake, "मराठी")
    assert fake.session_state["joint_counselling_reviewed"] is True
    assert "joint_counselling_answers" not in fake.session_state
    assert any("डेटाबेसमध्ये साठवली जात नाहीत" in str(args) for name, args, _ in fake.calls if name == "caption")
    assert not any(name in {"text_input", "form_submit_button", "download_button"} for name, _, _ in fake.calls)


def test_review_status_displays_revision_count() -> None:
    state = {"joint_counselling_step": len(PROMPTS)}
    record_response(state, "learner_priorities", ["hands_on_learning"])
    record_response(state, "learner_priorities", ["computer_based_learning"])
    fake = FakeCounsellingStreamlit(state=state)
    render_joint_counselling(fake, "English")
    captions = [args[0] for name, args, _ in fake.calls if name == "caption"]
    assert any("Revised 1 time(s)" in caption for caption in captions)
