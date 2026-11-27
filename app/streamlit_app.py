"""Accessible bilingual Streamlit shell for PathSaathi AI."""

from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from app.pathway_flow import render_pathway_explorer
from app.qualification_flow import (
    render_multi_route_eligibility,
    render_qualification_explainers,
)
from app.profile_flow import render_profile_capture
from app.counselling_flow import render_joint_counselling
from app.read_aloud import render_read_aloud
from app.outcome_import_flow import render_outcome_import
from app.course_explorer import render_course_explorer
from app.outcome_explorer import render_outcome_explorer


API_TIMEOUT_SECONDS = 2.0
DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"

TRANSLATIONS = {
    "English": {
        "title": "PathSaathi AI",
        "tagline": "Explore vocational pathways together.",
        "language": "Language / भाषा",
        "navigation": "Choose a section",
        "nav_home": "Home",
        "nav_profile": "Learner profile",
        "nav_conversation": "Family conversation",
        "nav_pathways": "Explore pathways",
        "conversation_heading": "Family counselling conversation",
        "conversation_description": "Learner and parent/guardian questions are recorded separately. Choose one short prompt at a time; every answer is optional.",
        "progress": "Step {step} of {total}",
        "help_title": "Need help?",
        "help_body": (
            "Use the section list to move between Home, Learner profile, Family conversation and Explore pathways. "
            "You can change language at any time. Profile and conversation drafts stay in this "
            "Streamlit session only; they are not sent to the API or written to a database."
        ),
        "back": "Back",
        "next": "Continue",
        "api_label": "Connection to counselling service",
        "api_online": "API connected",
        "api_offline": "API not reachable",
        "api_fallback": "You can still explore this demo. Live counselling features need the API.",
        "notice": (
            "Guidance only: recommendations are not guarantees of admission, employment, "
            "placement or earnings."
        ),
        "welcome": (
            "Start with a conversation about interests, skills and family questions. "
            "Learners and parents can explore options together."
        ),
        "home_next": "Next: tell us about the learner's education and interests.",
        "profile_heading": "Learner profile",
        "profile_description": (
            "A short profile will help explain which training options may fit the learner's "
            "education, interests and location."
        ),
        "profile_placeholder": (
            "Answer one short question at a time. Optional questions can be skipped. "
            "This draft stays in the current session only."
        ),
        "pathways_heading": "Explore vocational pathways",
        "pathways_description": (
            "Bring forward options that match the learner's stated interests and work preferences. "
            "Show education eligibility separately and only from verified criteria."
        ),
        "pathways_placeholder": (
            "Preference matching uses illustrative themes only. A separately sourced national "
            "NQR qualification example appears below; it is not a local provider offer or outcome."
        ),
        "footer": (
            "Prototype for SIH26241. Outcome figures will be shown only when their source, "
            "cohort and metric definitions are available."
        ),
    },
    "मराठी": {
        "title": "PathSaathi AI",
        "tagline": "व्यावसायिक शिक्षणाचे पर्याय एकत्र समजून घ्या.",
        "language": "भाषा / Language",
        "navigation": "विभाग निवडा",
        "nav_home": "मुख्यपृष्ठ",
        "nav_profile": "विद्यार्थ्याची माहिती",
        "nav_conversation": "कौटुंबिक चर्चा",
        "nav_pathways": "शिक्षणाचे पर्याय",
        "conversation_heading": "विद्यार्थी आणि पालकांचे समुपदेशन",
        "conversation_description": "विद्यार्थी आणि पालक/पालकप्रतिनिधी यांचे प्रश्न स्वतंत्रपणे नोंदवले जातात. एका वेळी एक छोटा प्रश्न घ्या; प्रत्येक उत्तर ऐच्छिक आहे.",
        "progress": "टप्पा {step} / {total}",
        "help_title": "मदत हवी आहे?",
        "help_body": (
            "मुख्यपृष्ठ, विद्यार्थ्याची माहिती, कौटुंबिक चर्चा आणि शिक्षणाचे पर्याय या विभागांमध्ये "
            "जाण्यासाठी विभाग सूची वापरा. तुम्ही कधीही भाषा बदलू शकता. विद्यार्थ्याची माहिती आणि "
            "कौटुंबिक चर्चेचे मसुदे फक्त सध्याच्या सत्रात राहतात; ते API कडे पाठवले जात नाहीत "
            "किंवा डेटाबेसमध्ये लिहिले जात नाहीत."
        ),
        "back": "मागील टप्पा",
        "next": "पुढील टप्पा",
        "api_label": "समुपदेशन सेवेशी जोडणी",
        "api_online": "API जोडलेले आहे",
        "api_offline": "API शी जोडणी होत नाही",
        "api_fallback": (
            "तुम्ही हा डेमो पाहू शकता. प्रत्यक्ष समुपदेशन सुविधांसाठी API आवश्यक आहे."
        ),
        "notice": (
            "ही केवळ मार्गदर्शन सेवा आहे. प्रवेश, नोकरी, प्लेसमेंट किंवा उत्पन्नाची "
            "हमी दिली जात नाही."
        ),
        "welcome": (
            "विद्यार्थ्याच्या आवडी, कौशल्ये आणि कुटुंबाच्या प्रश्नांपासून सुरुवात करा. "
            "विद्यार्थी आणि पालक एकत्र पर्याय समजून घेऊ शकतात."
        ),
        "home_next": "पुढील टप्पा: विद्यार्थ्याचे शिक्षण आणि आवडी सांगा.",
        "profile_heading": "विद्यार्थ्याची माहिती",
        "profile_description": (
            "विद्यार्थ्याचे शिक्षण, आवडी आणि ठिकाण समजल्यास योग्य प्रशिक्षण पर्याय "
            "समजावून सांगता येतील."
        ),
        "profile_placeholder": (
            "एकावेळी एक छोटा प्रश्न सोडवा. ऐच्छिक प्रश्न वगळू शकता. हा मसुदा "
            "फक्त सध्याच्या सत्रात राहील."
        ),
        "pathways_heading": "व्यावसायिक शिक्षणाचे पर्याय",
        "pathways_description": (
            "विद्यार्थ्याने सांगितलेल्या आवडी आणि कामाच्या आवडींशी जुळणारे पर्याय आधी दाखवले जातात. "
            "शिक्षणानुसार पात्रता स्वतंत्रपणे आणि पडताळलेल्या अटींवरच दाखवली जाते."
        ),
        "pathways_placeholder": (
            "आवडींशी जुळवण्यासाठी फक्त उदाहरणार्थ पर्याय वापरले आहेत. खाली NQR मधील एक "
            "राष्ट्रीय पात्रता नोंद दिली आहे; ती स्थानिक प्रशिक्षण केंद्र किंवा रोजगाराचा पुरावा नाही."
        ),
        "footer": (
            "SIH26241 साठी नमुना आवृत्ती. स्रोत, गट आणि मोजमापांची व्याख्या उपलब्ध "
            "असल्यावरच रोजगारविषयक आकडे दाखवले जातील."
        ),
    },
}


def _health_endpoint(api_base_url: str | None) -> str | None:
    """Resolve and validate the configured API base URL without making a request."""
    configured_url = (
        api_base_url
        if api_base_url is not None
        else os.getenv("PATHSAATHI_API_URL", DEFAULT_API_BASE_URL)
    )
    base_url = configured_url.strip().rstrip("/")
    if not base_url:
        return None

    try:
        parsed = urlsplit(base_url)
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
        ):
            return None
        _ = parsed.port
    except ValueError:
        return None

    return f"{base_url}/health"


def is_api_healthy(
    api_base_url: str | None = None,
    timeout: float = API_TIMEOUT_SECONDS,
) -> bool:
    """Check the API health contract without making the UI depend on the API."""
    health_url = _health_endpoint(api_base_url)
    if health_url is None:
        return False

    try:
        request = Request(health_url, headers={"Accept": "application/json"})
        with urlopen(request, timeout=timeout) as response:
            if response.status != 200:
                return False
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError, ValueError):
        return False

    return (
        isinstance(payload, dict)
        and payload.get("status") == "ok"
        and payload.get("service") == "pathsaathi-api"
    )


def main() -> None:
    """Render the bilingual shell with explicit progress, navigation and help."""
    import streamlit as st

    st.set_page_config(page_title="PathSaathi AI", page_icon="🎓", layout="centered")

    locale = st.sidebar.selectbox("Language / भाषा", list(TRANSLATIONS))
    copy = TRANSLATIONS[locale]
    page_keys = ("home", "profile", "conversation", "pathways")
    if st.session_state.get("page_navigation") not in page_keys:
        st.session_state["page_navigation"] = "home"

    selected_page = st.sidebar.radio(
        copy["navigation"],
        page_keys,
        format_func=lambda key: copy[f"nav_{key}"],
        key="page_navigation",
    )
    selected_index = page_keys.index(selected_page)

    def set_page(page: str) -> None:
        """Update the stable page key before Streamlit reruns the script."""
        st.session_state["page_navigation"] = page

    st.sidebar.caption(copy["api_label"])
    if is_api_healthy():
        st.sidebar.success(copy["api_online"])
    else:
        st.sidebar.warning(copy["api_offline"])
    st.sidebar.caption(copy["api_fallback"])

    st.progress(
        (selected_index + 1) / len(page_keys),
        text=copy["progress"].format(step=selected_index + 1, total=len(page_keys)),
    )
    with st.expander(copy["help_title"], expanded=False):
        st.write(copy["help_body"])

    read_aloud_text = ""
    if selected_page == "home":
        st.title(copy["title"])
        st.subheader(copy["tagline"])
        st.info(copy["notice"])
        st.write(copy["welcome"])
        st.markdown(f"**{copy['home_next']}**")
        read_aloud_text = " ".join((copy["tagline"], copy["notice"], copy["welcome"], copy["home_next"]))
    elif selected_page == "profile":
        st.title(copy["profile_heading"])
        st.write(copy["profile_description"])
        st.info(copy["profile_placeholder"])
        render_profile_capture(st, locale)
        read_aloud_text = " ".join((copy["profile_heading"], copy["profile_description"], copy["profile_placeholder"]))
    elif selected_page == "conversation":
        st.title(copy["conversation_heading"])
        st.write(copy["conversation_description"])
        render_joint_counselling(st, locale)
        read_aloud_text = " ".join((copy["conversation_heading"], copy["conversation_description"]))
    else:
        st.title(copy["pathways_heading"])
        st.write(copy["pathways_description"])
        st.info(copy["pathways_placeholder"])
        render_pathway_explorer(st, locale)
        render_qualification_explainers(st, locale)
        render_multi_route_eligibility(st, locale)
        render_course_explorer(st, locale)
        render_outcome_import(st, locale)
        render_outcome_explorer(st, locale)
        read_aloud_text = " ".join((copy["pathways_heading"], copy["pathways_description"], copy["pathways_placeholder"]))

    if selected_page not in {"profile", "conversation"}:
        if selected_index > 0:
            st.button(
                copy["back"],
                key="back_navigation",
                on_click=set_page,
                args=(page_keys[selected_index - 1],),
                use_container_width=True,
            )
        if selected_index < len(page_keys) - 1:
            st.button(
                copy["next"],
                key="next_navigation",
                on_click=set_page,
                args=(page_keys[selected_index + 1],),
                use_container_width=True,
            )

    render_read_aloud(st, read_aloud_text, locale)
    st.caption(copy["footer"])


if __name__ == "__main__":
    main()
