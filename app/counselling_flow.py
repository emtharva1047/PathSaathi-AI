"""Deterministic, bilingual joint learner-parent counselling prompts.

All answers are kept in Streamlit session state. This module performs no API,
database, LLM, analytics, or external-service calls.
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CounsellingPrompt:
    """A fixed prompt owned by one participant role or the family together."""

    prompt_id: str
    role: str
    category: str
    options: tuple[str, ...]


@dataclass(frozen=True)
class CounsellingReviewItem:
    """Validated, privacy-minimised response summary for the review screen."""

    prompt_id: str
    role: str
    category: str
    status: str
    selected_values: tuple[str, ...]
    revision_count: int


PROMPTS = (
    CounsellingPrompt(
        "learner_evidence_questions",
        "learner",
        "evidence_question",
        (
            "qualification_requirements",
            "training_availability",
            "fees_and_costs",
            "workplace_safety",
            "job_outcomes",
            "progression",
        ),
    ),
    CounsellingPrompt(
        "parent_reported_concerns",
        "parent",
        "self_reported_concern",
        (
            "workplace_safety",
            "training_affordability",
            "income_evidence",
            "job_security",
            "social_perception",
            "local_training",
            "progression",
        ),
    ),
    CounsellingPrompt(
        "learner_priorities",
        "learner",
        "preference",
        (
            "learner_interest",
            "hands_on_learning",
            "computer_based_learning",
            "further_progression",
            "time_to_decide",
            "not_sure",
        ),
    ),
    CounsellingPrompt(
        "parent_information_needs",
        "parent",
        "evidence_question",
        (
            "official_entry_rules",
            "verified_training_availability",
            "published_fees_if_available",
            "outcome_data_if_available",
            "workplace_safety_evidence",
            "progression_records",
        ),
    ),
    CounsellingPrompt(
        "learner_next_step",
        "learner",
        "preference",
        (
            "review_evidence_together",
            "compare_pathways",
            "explore_independently",
            "take_time",
            "not_sure",
        ),
    ),
    CounsellingPrompt(
        "family_first_topic",
        "shared",
        "family_discussion",
        (
            "start_with_learner_questions",
            "review_parent_questions",
            "verify_entry_requirements",
            "compare_known_and_unknown",
            "pause_and_revisit",
        ),
    ),
)

PROMPT_BY_ID = {prompt.prompt_id: prompt for prompt in PROMPTS}


COUNSELLING_COPY: dict[str, dict[str, Any]] = {
    "English": {
        "progress": "Question {step} of {total}",
        "review_progress": "Review all {total} questions",
        "role_labels": {
            "learner": "Learner's own answer",
            "parent": "Parent/guardian — self-reported",
            "shared": "Family discussion",
        },
        "category_labels": {
            "evidence_question": "Information to verify",
            "self_reported_concern": "Concern personally raised by the parent/guardian",
            "preference": "Preference, not a suitability test",
            "family_discussion": "Topic for joint discussion",
        },
        "prompt_titles": {
            "learner_evidence_questions": "Learner: facts to check",
            "parent_reported_concerns": "Parent/guardian: questions or concerns",
            "learner_priorities": "Learner: what matters to you",
            "parent_information_needs": "Parent/guardian: information needed",
            "learner_next_step": "Learner: preferred next step",
            "family_first_topic": "Together: where to begin",
        },
        "prompt_questions": {
            "learner_evidence_questions": "Which facts would you like to check before deciding?",
            "parent_reported_concerns": "Which questions or concerns would you like to raise yourself?",
            "learner_priorities": "What matters most to you while exploring options?",
            "parent_information_needs": "Which information would help you discuss the options?",
            "learner_next_step": "What would you prefer to do next?",
            "family_first_topic": "Which topic would you like to review together first?",
        },
        "prompt_help": {
            "learner_evidence_questions": "Choose any topics. This records questions only; it does not claim that evidence is available.",
            "parent_reported_concerns": "Choose only concerns you personally wish to share. The system does not infer feelings or concerns.",
            "learner_priorities": "There is no right answer. These are the learner's preferences and can be changed.",
            "parent_information_needs": "Some information may not be available. Missing facts will remain unknown.",
            "learner_next_step": "The learner may choose to explore, compare, pause or decide later.",
            "family_first_topic": "Choose a starting point together. Either participant may disagree or ask to pause.",
        },
        "option_labels": {
            "learner_evidence_questions": {
                "qualification_requirements": "Qualification and entry requirements",
                "training_availability": "Whether training is available in a practical area",
                "fees_and_costs": "Fees and costs, if officially published",
                "workplace_safety": "Workplace safety information",
                "job_outcomes": "Published job and outcome evidence",
                "progression": "Further learning and NSQF progression",
            },
            "parent_reported_concerns": {
                "workplace_safety": "Workplace safety",
                "training_affordability": "Training affordability",
                "income_evidence": "Reliable income evidence",
                "job_security": "Job security",
                "social_perception": "Social perception",
                "local_training": "Training within a practical distance",
                "progression": "Further learning and progression",
            },
            "learner_priorities": {
                "learner_interest": "My own interests",
                "hands_on_learning": "Practical, hands-on learning",
                "computer_based_learning": "Computer-based learning",
                "further_progression": "Options to continue learning",
                "time_to_decide": "More time before deciding",
                "not_sure": "I am not sure yet",
            },
            "parent_information_needs": {
                "official_entry_rules": "Official qualification and entry rules",
                "verified_training_availability": "Verified training availability",
                "published_fees_if_available": "Published fees, if available",
                "outcome_data_if_available": "Verified outcome data, if available",
                "workplace_safety_evidence": "Evidence about workplace safety",
                "progression_records": "Official progression records",
            },
            "learner_next_step": {
                "review_evidence_together": "Review available evidence together",
                "compare_pathways": "Compare more than one pathway",
                "explore_independently": "Explore options independently",
                "take_time": "Take time and decide later",
                "not_sure": "I am not sure yet",
            },
            "family_first_topic": {
                "start_with_learner_questions": "Start with the learner's questions",
                "review_parent_questions": "Review the parent's self-reported questions",
                "verify_entry_requirements": "Check official entry requirements",
                "compare_known_and_unknown": "Separate known facts from unknown information",
                "pause_and_revisit": "Pause and return to the discussion later",
            },
        },
        "select_label": "Choose any that apply (optional)",
        "skip": "Skip this question",
        "back": "Back",
        "continue": "Continue",
        "review_title": "Review the family conversation",
        "review_help": "Check that each answer belongs to the right person. Select Revise to change that response.",
        "status_labels": {
            "not_answered": "Not answered yet",
            "empty": "Continued without selecting an answer",
            "skipped": "Skipped by the participant",
            "answered": "Answered",
        },
        "revised_status": "Revised {count} time(s) — {status}",
        "no_selection": "No option selected",
        "revise": "Revise answer",
        "keep": "Keep this conversation draft in this session",
        "kept": "Conversation draft kept in this Streamlit session only.",
        "draft_notice": "This records questions and preferences only. It does not provide factual evidence, infer emotion or assess aptitude.",
        "session_only": "Session-only draft: answers are not sent to the API, stored in a database, shared with a counsellor or used for analytics. Closing the session may clear them.",
        "agency_note": "The learner's own preferences and next-step choice remain visible. A parent/guardian response does not override the learner's choice.",
        "translation_status": "English wording is the current prototype copy.",
    },
    "मराठी": {
        "progress": "प्रश्न {step} / {total}",
        "review_progress": "सर्व {total} प्रश्नांची उजळणी",
        "role_labels": {
            "learner": "विद्यार्थ्याचे स्वतःचे उत्तर",
            "parent": "पालक/पालकप्रतिनिधी — स्वतः सांगितलेले",
            "shared": "कौटुंबिक चर्चा",
        },
        "category_labels": {
            "evidence_question": "पडताळायची माहिती",
            "self_reported_concern": "पालकांनी स्वतः सांगितलेली चिंता",
            "preference": "आवड; योग्यता चाचणी नाही",
            "family_discussion": "एकत्र चर्चेचा विषय",
        },
        "prompt_titles": {
            "learner_evidence_questions": "विद्यार्थी: पडताळायची माहिती",
            "parent_reported_concerns": "पालक: प्रश्न किंवा चिंता",
            "learner_priorities": "विद्यार्थी: तुमच्यासाठी काय महत्त्वाचे आहे",
            "parent_information_needs": "पालक: आवश्यक माहिती",
            "learner_next_step": "विद्यार्थी: पुढील पसंतीचा टप्पा",
            "family_first_topic": "एकत्र: सुरुवात कुठून करायची",
        },
        "prompt_questions": {
            "learner_evidence_questions": "निर्णय घेण्यापूर्वी कोणती माहिती पडताळून पाहायची आहे?",
            "parent_reported_concerns": "तुम्हाला स्वतः मांडायचे कोणते प्रश्न किंवा चिंता आहेत?",
            "learner_priorities": "पर्याय समजून घेताना तुम्हाला सर्वात महत्त्वाचे काय वाटते?",
            "parent_information_needs": "पर्यायांवर चर्चा करण्यासाठी कोणती माहिती उपयोगी ठरेल?",
            "learner_next_step": "पुढे काय करायला तुम्हाला आवडेल?",
            "family_first_topic": "सर्वांनी मिळून आधी कोणत्या विषयावर चर्चा करावी?",
        },
        "prompt_help": {
            "learner_evidence_questions": "हवे ते विषय निवडा. येथे फक्त प्रश्न नोंदवले जातात; पुरावा उपलब्ध असल्याचा दावा केला जात नाही.",
            "parent_reported_concerns": "तुम्हाला स्वतः सांगायच्या चिंता निवडा. प्रणाली भावना किंवा चिंता ओळखत नाही.",
            "learner_priorities": "एकच योग्य उत्तर नाही. या विद्यार्थ्याच्या स्वतःच्या आवडी आहेत; त्या बदलता येतात.",
            "parent_information_needs": "काही माहिती उपलब्ध नसेल. नसलेली माहिती अज्ञातच राहील.",
            "learner_next_step": "विद्यार्थी पर्याय पाहू शकतो, तुलना करू शकतो, थांबू शकतो किंवा नंतर निर्णय घेऊ शकतो.",
            "family_first_topic": "एकत्र सुरुवातीचा विषय निवडा. कोणालाही असहमती व्यक्त करता येते किंवा चर्चा थांबवता येते.",
        },
        "option_labels": {
            "learner_evidence_questions": {
                "qualification_requirements": "पात्रता आणि प्रवेशाच्या अटी",
                "training_availability": "सोयीच्या भागात प्रशिक्षण उपलब्ध आहे का",
                "fees_and_costs": "अधिकृतरीत्या जाहीर केलेले शुल्क आणि खर्च",
                "workplace_safety": "कामाच्या ठिकाणच्या सुरक्षिततेची माहिती",
                "job_outcomes": "प्रसिद्ध केलेले रोजगार आणि परिणामांचे पुरावे",
                "progression": "पुढील शिक्षण आणि NSQF प्रगती",
            },
            "parent_reported_concerns": {
                "workplace_safety": "कामाच्या ठिकाणची सुरक्षितता",
                "training_affordability": "प्रशिक्षण परवडण्याजोगे असणे",
                "income_evidence": "उत्पन्नाबाबत विश्वासार्ह पुरावा",
                "job_security": "नोकरीची सुरक्षितता",
                "social_perception": "समाजातील धारणा",
                "local_training": "सोयीच्या अंतरावर प्रशिक्षण",
                "progression": "पुढील शिक्षण आणि प्रगती",
            },
            "learner_priorities": {
                "learner_interest": "माझ्या स्वतःच्या आवडी",
                "hands_on_learning": "प्रत्यक्ष कृतीतून शिकणे",
                "computer_based_learning": "संगणकावर आधारित शिक्षण",
                "further_progression": "पुढे शिक्षण सुरू ठेवण्याचे पर्याय",
                "time_to_decide": "निर्णय घेण्यासाठी अधिक वेळ",
                "not_sure": "अजून खात्री नाही",
            },
            "parent_information_needs": {
                "official_entry_rules": "अधिकृत पात्रता आणि प्रवेशाच्या अटी",
                "verified_training_availability": "पडताळलेली प्रशिक्षण उपलब्धता",
                "published_fees_if_available": "उपलब्ध असल्यास जाहीर केलेले शुल्क",
                "outcome_data_if_available": "उपलब्ध असल्यास पडताळलेली परिणाम माहिती",
                "workplace_safety_evidence": "कामाच्या ठिकाणच्या सुरक्षिततेचे पुरावे",
                "progression_records": "अधिकृत प्रगतीचे अभिलेख",
            },
            "learner_next_step": {
                "review_evidence_together": "उपलब्ध पुरावे एकत्र पाहणे",
                "compare_pathways": "एकापेक्षा जास्त पर्यायांची तुलना करणे",
                "explore_independently": "पर्याय स्वतः समजून घेणे",
                "take_time": "वेळ घेऊन नंतर निर्णय घेणे",
                "not_sure": "अजून खात्री नाही",
            },
            "family_first_topic": {
                "start_with_learner_questions": "विद्यार्थ्याच्या प्रश्नांपासून सुरुवात",
                "review_parent_questions": "पालकांनी स्वतः सांगितलेल्या प्रश्नांची उजळणी",
                "verify_entry_requirements": "अधिकृत प्रवेशाच्या अटी तपासणे",
                "compare_known_and_unknown": "माहित असलेली आणि अज्ञात माहिती वेगळी करणे",
                "pause_and_revisit": "चर्चा थांबवून नंतर पुन्हा बोलणे",
            },
        },
        "select_label": "लागू असलेले पर्याय निवडा (ऐच्छिक)",
        "skip": "हा प्रश्न वगळा",
        "back": "मागे",
        "continue": "पुढे जा",
        "review_title": "कौटुंबिक चर्चेची उजळणी",
        "review_help": "प्रत्येक उत्तर योग्य व्यक्तीचे आहे का ते तपासा. उत्तर बदलण्यासाठी 'उत्तर बदला' निवडा.",
        "status_labels": {
            "not_answered": "अद्याप उत्तर दिलेले नाही",
            "empty": "पर्याय न निवडता पुढे गेले",
            "skipped": "सहभागीने प्रश्न वगळला",
            "answered": "उत्तर दिले",
        },
        "revised_status": "{count} वेळा बदलले — {status}",
        "no_selection": "कोणताही पर्याय निवडलेला नाही",
        "revise": "उत्तर बदला",
        "keep": "ही चर्चा फक्त सत्रात ठेवा",
        "kept": "चर्चेचा मसुदा फक्त या Streamlit सत्रात ठेवला आहे.",
        "draft_notice": "येथे फक्त प्रश्न आणि आवडी नोंदवल्या जातात. तथ्यात्मक पुरावा दिला जात नाही, भावना ओळखल्या जात नाहीत आणि क्षमता तपासली जात नाही.",
        "session_only": "फक्त सत्रातील मसुदा: उत्तरे API कडे पाठवली जात नाहीत, डेटाबेसमध्ये साठवली जात नाहीत, समुपदेशकासोबत शेअर केली जात नाहीत किंवा विश्लेषणासाठी वापरली जात नाहीत. सत्र बंद केल्यास ती नष्ट होऊ शकतात.",
        "agency_note": "विद्यार्थ्याच्या स्वतःच्या आवडी आणि पुढील टप्प्याची निवड स्पष्ट दिसते. पालकांचे उत्तर विद्यार्थ्याच्या निवडीवर मात करत नाही.",
        "translation_status": "मराठी मजकूर हा मानवी भाषिक पुनरावलोकनापूर्वीचा मसुदा आहे.",
    },
}


def _normalise_values(values: Any, prompt: CounsellingPrompt) -> tuple[str, ...]:
    """Return only known option identifiers in their catalogue order."""
    if not isinstance(values, (list, tuple, set)):
        return ()
    return tuple(option for option in prompt.options if option in values)


def _stored_response(
    state: Mapping[str, Any], prompt: CounsellingPrompt
) -> dict[str, Any] | None:
    """Read a response only when its role matches the fixed prompt owner."""
    answers = state.get("joint_counselling_answers", {})
    if not isinstance(answers, Mapping):
        return None
    response = answers.get(prompt.prompt_id)
    if not isinstance(response, Mapping) or response.get("role") != prompt.role:
        return None
    status = response.get("status")
    if status not in {"answered", "empty", "skipped"}:
        return None
    revision_count = response.get("revision_count", 0)
    if not isinstance(revision_count, int) or isinstance(revision_count, bool):
        revision_count = 0
    return {
        "status": status,
        "selected_values": _normalise_values(response.get("selected_values", ()), prompt),
        "revision_count": max(0, revision_count),
    }


def record_response(
    state: MutableMapping[str, Any],
    prompt_id: str,
    selected_values: Any = (),
    *,
    skipped: bool = False,
) -> None:
    """Record one role-owned response and count meaningful revisions."""
    prompt = PROMPT_BY_ID.get(prompt_id)
    if prompt is None:
        raise ValueError(f"Unknown counselling prompt: {prompt_id}")

    selected = () if skipped else _normalise_values(selected_values, prompt)
    status = "skipped" if skipped else "answered" if selected else "empty"
    previous = _stored_response(state, prompt)
    revision_count = previous["revision_count"] if previous else 0
    if previous is not None and (
        previous["status"] != status or previous["selected_values"] != selected
    ):
        revision_count += 1

    raw_answers = state.get("joint_counselling_answers", {})
    answers = dict(raw_answers) if isinstance(raw_answers, Mapping) else {}
    answers[prompt_id] = {
        "role": prompt.role,
        "category": prompt.category,
        "status": status,
        "selected_values": list(selected),
        "revision_count": revision_count,
    }
    state["joint_counselling_answers"] = answers
    state.pop("joint_counselling_reviewed", None)


def build_review(state: Mapping[str, Any]) -> tuple[CounsellingReviewItem, ...]:
    """Return all prompts in fixed order, including unanswered and skipped states."""
    items: list[CounsellingReviewItem] = []
    for prompt in PROMPTS:
        response = _stored_response(state, prompt)
        if response is None:
            items.append(
                CounsellingReviewItem(
                    prompt.prompt_id, prompt.role, prompt.category, "not_answered", (), 0
                )
            )
            continue
        items.append(
            CounsellingReviewItem(
                prompt.prompt_id,
                prompt.role,
                prompt.category,
                response["status"],
                response["selected_values"],
                response["revision_count"],
            )
        )
    return tuple(items)


def _render_review(st: Any, locale: str, copy: dict[str, Any]) -> None:
    """Render a role-separated review and allow a participant to revise their answer."""
    st.progress(1.0, text=copy["review_progress"].format(total=len(PROMPTS)))
    st.subheader(copy["review_title"])
    st.caption(copy["review_help"])
    st.caption(copy["translation_status"])

    for index, (prompt, item) in enumerate(zip(PROMPTS, build_review(st.session_state))):
        role = copy["role_labels"][item.role]
        category = copy["category_labels"][item.category]
        st.markdown(f"**{role} · {category}**")
        st.write(copy["prompt_titles"][prompt.prompt_id])
        st.write(copy["prompt_questions"][prompt.prompt_id])
        status = copy["status_labels"][item.status]
        if item.revision_count:
            status = copy["revised_status"].format(
                count=item.revision_count, status=status
            )
        st.caption(status)
        labels = copy["option_labels"][prompt.prompt_id]
        selected_labels = [labels[value] for value in item.selected_values]
        st.write(", ".join(selected_labels) if selected_labels else copy["no_selection"])
        if st.button(
            f"{copy['revise']} {index + 1}",
            key=f"joint_counselling_revise_{prompt.prompt_id}",
            use_container_width=True,
        ):
            st.session_state["joint_counselling_step"] = index
            st.session_state.pop("joint_counselling_reviewed", None)
            return

    st.info(copy["agency_note"])
    st.caption(copy["session_only"])
    if st.button(copy["back"], key="joint_counselling_review_back", use_container_width=True):
        st.session_state["joint_counselling_step"] = len(PROMPTS) - 1
        return
    if st.button(copy["keep"], key="joint_counselling_keep", use_container_width=True):
        st.session_state["joint_counselling_reviewed"] = True
    if st.session_state.get("joint_counselling_reviewed"):
        st.success(copy["kept"])


def render_joint_counselling(st: Any, locale: str) -> None:
    """Render one deterministic learner/parent/family prompt at a time."""
    copy = COUNSELLING_COPY.get(locale, COUNSELLING_COPY["English"])
    step = st.session_state.get("joint_counselling_step", 0)
    if not isinstance(step, int) or isinstance(step, bool) or not 0 <= step <= len(PROMPTS):
        step = 0
        st.session_state["joint_counselling_step"] = step

    if step == len(PROMPTS):
        _render_review(st, locale, copy)
        return

    prompt = PROMPTS[step]
    st.progress(
        (step + 1) / (len(PROMPTS) + 1),
        text=copy["progress"].format(step=step + 1, total=len(PROMPTS)),
    )
    st.subheader(copy["prompt_titles"][prompt.prompt_id])
    st.caption(
        f"{copy['role_labels'][prompt.role]} · "
        f"{copy['category_labels'][prompt.category]}"
    )
    st.write(copy["prompt_questions"][prompt.prompt_id])
    st.caption(copy["prompt_help"][prompt.prompt_id])
    st.caption(copy["translation_status"])
    st.info(copy["draft_notice"])

    widget_key = f"joint_counselling_answer_{prompt.prompt_id}"
    saved = _stored_response(st.session_state, prompt)
    if saved is not None and saved["status"] == "skipped":
        st.session_state[widget_key] = []
    elif widget_key not in st.session_state and saved is not None:
        st.session_state[widget_key] = list(saved["selected_values"])

    selected = st.multiselect(
        copy["select_label"],
        options=prompt.options,
        format_func=copy["option_labels"][prompt.prompt_id].get,
        key=widget_key,
    )
    if selected is None:
        selected = st.session_state.get(widget_key, ())

    if st.button(
        copy["skip"],
        key=f"joint_counselling_skip_{prompt.prompt_id}",
        use_container_width=True,
    ):
        record_response(st.session_state, prompt.prompt_id, skipped=True)
        st.session_state["joint_counselling_step"] = step + 1
        return

    if step > 0 and st.button(
        copy["back"], key="joint_counselling_back", use_container_width=True
    ):
        record_response(st.session_state, prompt.prompt_id, selected)
        st.session_state["joint_counselling_step"] = step - 1
        return

    if st.button(
        copy["continue"],
        key=f"joint_counselling_continue_{prompt.prompt_id}",
        use_container_width=True,
    ):
        record_response(st.session_state, prompt.prompt_id, selected)
        st.session_state["joint_counselling_step"] = step + 1
        return
