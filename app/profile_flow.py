"""Guided, session-only learner and parent profile capture for Streamlit."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from core.profiles import (
    ConcernCategory,
    EducationLevel,
    FamilyCounsellingContext,
    LearnerProfile,
    ParentContext,
    PreferredLanguage,
)


PROFILE_STEPS = (
    "education",
    "region",
    "interests",
    "work_preferences",
    "parent_concerns",
    "parent_priorities",
    "review",
)

INTEREST_OPTIONS = (
    "technology",
    "repair_and_making",
    "design_and_creativity",
    "health_and_care",
    "agriculture_and_nature",
    "business_and_services",
    "working_with_people",
)

WORK_PREFERENCE_OPTIONS = (
    "hands_on",
    "computer_based",
    "outdoor",
    "indoor",
    "people_facing",
    "independent_work",
)

PARENT_PRIORITY_OPTIONS = (
    "workplace_safety",
    "income_evidence",
    "nearby_training",
    "affordable_training",
    "progression_options",
    "job_security",
    "learner_choice",
)

PROFILE_COPY: dict[str, dict[str, Any]] = {
    "English": {
        "progress": "Question {step} of {total}",
        "step_titles": (
            "Learner education",
            "Broad region (optional)",
            "Learner interests (optional)",
            "Learner work preferences (optional)",
            "Parent/guardian concerns (optional)",
            "Parent/guardian priorities (optional)",
            "Review the two perspectives",
        ),
        "step_help": (
            "Choose the highest level the learner has completed. If unsure, leave it as Not sure / not shared.",
            "A broad state-level code can help localise later evidence. This is optional; no address or city is requested.",
            "Choose any interests the learner wants to explore. The learner may choose none or change these later.",
            "Choose work settings the learner would like to explore. These are preferences, not a suitability test.",
            "Select concerns the parent or guardian has personally raised. The system does not infer feelings or concerns.",
            "Select what the parent or guardian considers important. Keep these priorities separate from the learner's choices.",
            "Check that the learner's interests and the parent's concerns remain separate before keeping this draft.",
        ),
        "education_label": "Highest completed education level",
        "education_labels": {
            EducationLevel.BELOW_GRADE_8: "Below Grade 8",
            EducationLevel.GRADE_8: "Grade 8",
            EducationLevel.GRADE_10: "Grade 10",
            EducationLevel.GRADE_12: "Grade 12",
            EducationLevel.ITI_OR_VOCATIONAL: "ITI / vocational qualification",
            EducationLevel.DIPLOMA: "Diploma",
            EducationLevel.GRADUATE: "Graduate",
            EducationLevel.OTHER: "Other / not listed",
            EducationLevel.UNKNOWN: "Not sure / prefer not to say",
        },
        "region_label": "State / broad region",
        "region_labels": {
            None: "Not shared",
            "MH": "Maharashtra (pilot assumption; not confirmed)",
        },
        "interest_label": "What would the learner like to explore?",
        "interest_labels": {
            "technology": "Technology",
            "repair_and_making": "Repairing and making things",
            "design_and_creativity": "Design and creative work",
            "health_and_care": "Health and care",
            "agriculture_and_nature": "Agriculture and nature",
            "business_and_services": "Business and services",
            "working_with_people": "Working with people",
        },
        "work_preference_label": "Which work settings sound interesting?",
        "work_preference_labels": {
            "hands_on": "Practical, hands-on work",
            "computer_based": "Computer-based work",
            "outdoor": "Outdoor work",
            "indoor": "Indoor work",
            "people_facing": "Work with people or customers",
            "independent_work": "Independent work",
        },
        "concern_label": "What concerns has the parent/guardian raised?",
        "concern_labels": {
            ConcernCategory.INCOME: "Income potential",
            ConcernCategory.PLACEMENT_AND_JOB_SECURITY: "Placement and job security",
            ConcernCategory.WORKPLACE_SAFETY: "Workplace safety",
            ConcernCategory.SOCIAL_PERCEPTION: "Social perception",
            ConcernCategory.AFFORDABILITY: "Training affordability",
            ConcernCategory.PROGRESSION: "Further learning and progression",
            ConcernCategory.OTHER: "Other concern",
        },
        "priority_label": "What matters most to the parent/guardian?",
        "priority_labels": {
            "workplace_safety": "A safe workplace",
            "income_evidence": "Reliable income evidence",
            "nearby_training": "Training within a practical distance",
            "affordable_training": "Affordable training",
            "progression_options": "Options to continue learning",
            "job_security": "Clear information about job security",
            "learner_choice": "The learner's own choice",
        },
        "income_note": "Household income bands are not collected yet because the pilot has not approved a band taxonomy.",
        "advisory_notice": "This is an optional conversation aid, not an aptitude test, psychometric assessment or prediction of success.",
        "learner_summary": "Learner perspective",
        "parent_summary": "Parent/guardian perspective",
        "education_summary": "Education",
        "region_summary": "Broad region",
        "interests_summary": "Interests",
        "work_summary": "Work preferences",
        "concerns_summary": "Reported concerns",
        "priorities_summary": "Priorities",
        "not_provided": "Not provided",
        "session_only": "Keeping this draft stores it only in the current Streamlit session. It is not sent to the API or written to a database. Closing the session may clear it.",
        "back": "Previous question",
        "next": "Continue",
        "save": "Keep this session draft",
        "saved": "Draft kept in this session only. No database or counsellor request was created.",
    },
    "मराठी": {
        "progress": "प्रश्न {step} / {total}",
        "step_titles": (
            "विद्यार्थ्याचे शिक्षण",
            "विभाग (ऐच्छिक)",
            "विद्यार्थ्याच्या आवडी (ऐच्छिक)",
            "विद्यार्थ्याच्या कामाच्या आवडी (ऐच्छिक)",
            "पालकांनी सांगितलेल्या चिंता (ऐच्छिक)",
            "पालकांची प्राधान्ये (ऐच्छिक)",
            "दोन्ही बाजूंची माहिती तपासा",
        ),
        "step_help": (
            "विद्यार्थ्याने पूर्ण केलेले सर्वात उच्च शिक्षण निवडा. खात्री नसल्यास 'माहित नाही / सांगू इच्छित नाही' निवडा.",
            "पुढे स्थानिक माहिती दाखवण्यासाठी राज्याचा व्यापक संकेत उपयोगी ठरू शकतो. हा पर्याय ऐच्छिक आहे; पत्ता किंवा शहर विचारले जात नाही.",
            "विद्यार्थ्याला जाणून घ्यायच्या आवडी निवडा. काहीही निवडणे बंधनकारक नाही; नंतर बदलता येईल.",
            "विद्यार्थ्याला आवडू शकणाऱ्या कामाच्या पद्धती निवडा. या आवडी आहेत; योग्यता चाचणी नाही.",
            "पालक किंवा पालकप्रतिनिधींनी स्वतः सांगितलेल्या चिंता निवडा. प्रणाली भावना किंवा चिंता ओळखण्याचा प्रयत्न करत नाही.",
            "पालक किंवा पालकप्रतिनिधींना महत्त्वाच्या वाटणाऱ्या गोष्टी निवडा. ही प्राधान्ये विद्यार्थ्याच्या निवडींपासून वेगळी राहतील.",
            "मसुदा ठेवण्यापूर्वी विद्यार्थ्याच्या आवडी आणि पालकांच्या चिंता वेगळ्या दाखवल्या आहेत याची खात्री करा.",
        ),
        "education_label": "पूर्ण केलेले सर्वात उच्च शिक्षण",
        "education_labels": {
            EducationLevel.BELOW_GRADE_8: "इयत्ता ८ वी पेक्षा कमी",
            EducationLevel.GRADE_8: "इयत्ता ८ वी",
            EducationLevel.GRADE_10: "इयत्ता १० वी",
            EducationLevel.GRADE_12: "इयत्ता १२ वी",
            EducationLevel.ITI_OR_VOCATIONAL: "आयटीआय / व्यावसायिक पात्रता",
            EducationLevel.DIPLOMA: "डिप्लोमा",
            EducationLevel.GRADUATE: "पदवीधर",
            EducationLevel.OTHER: "इतर / यादीत नाही",
            EducationLevel.UNKNOWN: "माहित नाही / सांगू इच्छित नाही",
        },
        "region_label": "राज्य / व्यापक विभाग",
        "region_labels": {
            None: "सांगू इच्छित नाही",
            "MH": "महाराष्ट्र (पायलट गृहितक; पुष्टी झालेली नाही)",
        },
        "interest_label": "विद्यार्थ्याला कोणत्या गोष्टी जाणून घ्यायच्या आहेत?",
        "interest_labels": {
            "technology": "तंत्रज्ञान",
            "repair_and_making": "दुरुस्ती आणि वस्तू तयार करणे",
            "design_and_creativity": "डिझाइन आणि सर्जनशील काम",
            "health_and_care": "आरोग्य आणि काळजी सेवा",
            "agriculture_and_nature": "शेती आणि निसर्ग",
            "business_and_services": "व्यवसाय आणि सेवा",
            "working_with_people": "लोकांसोबत काम करणे",
        },
        "work_preference_label": "कोणत्या प्रकारचे काम आवडू शकते?",
        "work_preference_labels": {
            "hands_on": "प्रत्यक्ष हाताने करायचे काम",
            "computer_based": "संगणकावर आधारित काम",
            "outdoor": "बाहेरचे काम",
            "indoor": "घरातील / कार्यालयातील काम",
            "people_facing": "लोक किंवा ग्राहकांसोबत काम",
            "independent_work": "स्वतंत्रपणे काम",
        },
        "concern_label": "पालकांनी कोणत्या चिंता सांगितल्या आहेत?",
        "concern_labels": {
            ConcernCategory.INCOME: "उत्पन्नाची शक्यता",
            ConcernCategory.PLACEMENT_AND_JOB_SECURITY: "नोकरी आणि नोकरीची सुरक्षितता",
            ConcernCategory.WORKPLACE_SAFETY: "कामाच्या ठिकाणची सुरक्षितता",
            ConcernCategory.SOCIAL_PERCEPTION: "समाजातील प्रतिष्ठा",
            ConcernCategory.AFFORDABILITY: "प्रशिक्षणाचा खर्च",
            ConcernCategory.PROGRESSION: "पुढील शिक्षण आणि प्रगती",
            ConcernCategory.OTHER: "इतर चिंता",
        },
        "priority_label": "पालकांना सर्वात महत्त्वाच्या वाटणाऱ्या गोष्टी कोणत्या?",
        "priority_labels": {
            "workplace_safety": "सुरक्षित कामाचे ठिकाण",
            "income_evidence": "उत्पन्नाबाबत विश्वासार्ह पुरावा",
            "nearby_training": "सोयीच्या अंतरावर प्रशिक्षण",
            "affordable_training": "परवडणारे प्रशिक्षण",
            "progression_options": "पुढे शिक्षण सुरू ठेवण्याचे पर्याय",
            "job_security": "नोकरीच्या सुरक्षिततेबद्दल स्पष्ट माहिती",
            "learner_choice": "विद्यार्थ्याची स्वतःची निवड",
        },
        "income_note": "पायलटसाठी उत्पन्नाच्या गटांची मान्य यादी अद्याप ठरलेली नसल्यामुळे घरगुती उत्पन्न विचारले जात नाही.",
        "advisory_notice": "ही ऐच्छिक चर्चा-सहाय्यक सुविधा आहे. ही क्षमता चाचणी, मानसशास्त्रीय चाचणी किंवा यशाचे भाकीत नाही.",
        "learner_summary": "विद्यार्थ्याची बाजू",
        "parent_summary": "पालकांची बाजू",
        "education_summary": "शिक्षण",
        "region_summary": "व्यापक विभाग",
        "interests_summary": "आवडी",
        "work_summary": "कामाच्या आवडी",
        "concerns_summary": "सांगितलेल्या चिंता",
        "priorities_summary": "प्राधान्ये",
        "not_provided": "माहिती दिलेली नाही",
        "session_only": "हा मसुदा फक्त सध्याच्या Streamlit सत्रात ठेवला जाईल. तो API कडे पाठवला जाणार नाही किंवा डेटाबेसमध्ये लिहिला जाणार नाही. सत्र बंद केल्यास माहिती नष्ट होऊ शकते.",
        "back": "मागील प्रश्न",
        "next": "पुढील प्रश्न",
        "save": "हा सत्र-मसुदा ठेवा",
        "saved": "मसुदा फक्त या सत्रात ठेवला आहे. डेटाबेस नोंद किंवा समुपदेशक विनंती तयार केलेली नाही.",
    },
}


def _selected_values(
    state: Mapping[str, Any], key: str, allowed: tuple[str, ...]
) -> tuple[str, ...]:
    values = state.get(key, ()) or ()
    if not isinstance(values, (list, tuple, set)):
        return ()
    return tuple(value for value in allowed if value in values)


def build_family_context(
    state: Mapping[str, Any], locale: str
) -> FamilyCounsellingContext:
    """Build role-separated domain records from validated, session-local choices."""
    try:
        education = EducationLevel(state.get("profile_education_level", EducationLevel.UNKNOWN))
    except (TypeError, ValueError):
        education = EducationLevel.UNKNOWN

    region = state.get("profile_state_code")
    state_code = "MH" if region == "MH" else None
    language = PreferredLanguage.MARATHI if locale == "मराठी" else PreferredLanguage.ENGLISH
    concerns: list[ConcernCategory] = []
    for value in state.get("profile_parent_concerns", ()) or ():
        try:
            concern = ConcernCategory(value)
        except (TypeError, ValueError):
            continue
        if concern not in concerns:
            concerns.append(concern)

    learner = LearnerProfile(
        learner_ref="learner_local",
        education_level=education,
        state_code=state_code,
        interests=_selected_values(state, "profile_interests", INTEREST_OPTIONS),
        work_preferences=_selected_values(
            state, "profile_work_preferences", WORK_PREFERENCE_OPTIONS
        ),
        preferred_language=language,
    )
    parent = ParentContext(
        participant_ref="parent_local",
        concerns=tuple(concerns),
        priorities=_selected_values(
            state, "profile_parent_priorities", PARENT_PRIORITY_OPTIONS
        ),
        preferred_language=language,
    )
    return FamilyCounsellingContext(learner=learner, parent=parent)


def render_profile_capture(st: Any, locale: str) -> None:
    """Render one short, role-labelled profile question at a time."""
    copy = PROFILE_COPY[locale]
    step = st.session_state.get("profile_capture_step", 0)
    if not isinstance(step, int) or not 0 <= step < len(PROFILE_STEPS):
        step = 0
        st.session_state["profile_capture_step"] = step

    total = len(PROFILE_STEPS)
    st.progress((step + 1) / total, text=copy["progress"].format(step=step + 1, total=total))
    st.subheader(copy["step_titles"][step])
    st.caption(copy["step_help"][step])

    if step == 0:
        education_options = list(EducationLevel)
        st.selectbox(
            copy["education_label"],
            options=education_options,
            index=education_options.index(EducationLevel.UNKNOWN),
            format_func=copy["education_labels"].get,
            key="profile_education_level",
        )
        st.info(copy["advisory_notice"])
    elif step == 1:
        st.selectbox(
            copy["region_label"],
            options=(None, "MH"),
            index=0,
            format_func=copy["region_labels"].get,
            key="profile_state_code",
        )
        st.caption(copy["income_note"])
    elif step == 2:
        st.multiselect(
            copy["interest_label"],
            options=INTEREST_OPTIONS,
            format_func=copy["interest_labels"].get,
            key="profile_interests",
        )
    elif step == 3:
        st.multiselect(
            copy["work_preference_label"],
            options=WORK_PREFERENCE_OPTIONS,
            format_func=copy["work_preference_labels"].get,
            key="profile_work_preferences",
        )
    elif step == 4:
        concern_options = list(ConcernCategory)
        st.multiselect(
            copy["concern_label"],
            options=concern_options,
            format_func=copy["concern_labels"].get,
            key="profile_parent_concerns",
        )
    elif step == 5:
        st.multiselect(
            copy["priority_label"],
            options=PARENT_PRIORITY_OPTIONS,
            format_func=copy["priority_labels"].get,
            key="profile_parent_priorities",
        )
    else:
        context = build_family_context(st.session_state, locale)
        learner = context.learner
        parent = context.parent
        st.write(copy["learner_summary"])
        st.write(
            f"{copy['education_summary']}: "
            f"{copy['education_labels'][learner.education_level]}"
        )
        st.write(
            f"{copy['region_summary']}: "
            f"{copy['region_labels'].get(learner.state_code, copy['not_provided'])}"
        )
        st.write(
            f"{copy['interests_summary']}: "
            f"{', '.join(copy['interest_labels'][value] for value in learner.interests) or copy['not_provided']}"
        )
        st.write(
            f"{copy['work_summary']}: "
            f"{', '.join(copy['work_preference_labels'][value] for value in learner.work_preferences) or copy['not_provided']}"
        )
        st.write(copy["parent_summary"])
        st.write(
            f"{copy['concerns_summary']}: "
            f"{', '.join(copy['concern_labels'][value] for value in parent.concerns) or copy['not_provided']}"
        )
        st.write(
            f"{copy['priorities_summary']}: "
            f"{', '.join(copy['priority_labels'][value] for value in parent.priorities) or copy['not_provided']}"
        )
        st.info(copy["advisory_notice"])
        st.caption(copy["session_only"])

        def save_draft() -> None:
            st.session_state["profile_saved_context"] = build_family_context(
                st.session_state, locale
            )

        st.button(
            copy["save"],
            key="profile_save",
            on_click=save_draft,
            use_container_width=True,
        )
        if st.session_state.get("profile_saved_context") is not None:
            st.success(copy["saved"])

    def move_to(target: int) -> None:
        st.session_state["profile_capture_step"] = target
        st.session_state.pop("profile_saved_context", None)

    if step > 0:
        st.button(
            copy["back"],
            key="profile_back",
            on_click=move_to,
            args=(step - 1,),
            use_container_width=True,
        )
    if step < total - 1:
        st.button(
            copy["next"],
            key="profile_next",
            on_click=move_to,
            args=(step + 1,),
            use_container_width=True,
        )
