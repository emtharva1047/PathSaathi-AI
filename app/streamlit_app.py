"""Accessible bilingual Streamlit shell for PathSaathi AI."""

from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


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
        "nav_pathways": "Explore pathways",
        "progress": "Step {step} of {total}",
        "help_title": "Need help?",
        "help_body": (
            "Use the section list to move between Home, Learner profile and Explore pathways. "
            "You can change language at any time. This prototype screen does not collect "
            "personal information."
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
            "Profile questions are being built. No personal information is collected on "
            "this screen yet."
        ),
        "pathways_heading": "Explore vocational pathways",
        "pathways_description": (
            "Compare training routes, job roles and progression options using evidence "
            "that matches the learner's context."
        ),
        "pathways_placeholder": (
            "The course catalogue and verified outcome evidence will appear here after "
            "their data-validation work is complete."
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
        "nav_pathways": "शिक्षणाचे पर्याय",
        "progress": "टप्पा {step} / {total}",
        "help_title": "मदत हवी आहे?",
        "help_body": (
            "मुख्यपृष्ठ, विद्यार्थ्याची माहिती आणि शिक्षणाचे पर्याय या विभागांमध्ये "
            "जाण्यासाठी विभाग सूची वापरा. तुम्ही कधीही भाषा बदलू शकता. या नमुना "
            "स्क्रीनवर वैयक्तिक माहिती घेतली जात नाही."
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
            "माहिती भरण्याचे प्रश्न तयार होत आहेत. या स्क्रीनवर सध्या कोणतीही "
            "वैयक्तिक माहिती घेतली जात नाही."
        ),
        "pathways_heading": "व्यावसायिक शिक्षणाचे पर्याय",
        "pathways_description": (
            "विद्यार्थ्याच्या परिस्थितीशी जुळणारे प्रशिक्षण, नोकरीची भूमिका आणि "
            "पुढील शिक्षणाचे पर्याय पुराव्याच्या आधारे समजून घ्या."
        ),
        "pathways_placeholder": (
            "माहितीची पडताळणी पूर्ण झाल्यानंतर अभ्यासक्रम आणि रोजगारविषयक "
            "पुरावे येथे दिसतील."
        ),
        "footer": (
            "SIH26241 साठी नमुना आवृत्ती. स्रोत, गट आणि मोजमापांची व्याख्या उपलब्ध "
            "असल्यावरच रोजगारविषयक आकडे दाखवले जातील."
        ),
    },
}


def is_api_healthy(
    api_base_url: str | None = None,
    timeout: float = API_TIMEOUT_SECONDS,
) -> bool:
    """Check the API health contract without making the UI depend on the API."""
    base_url = (api_base_url or os.getenv("PATHSAATHI_API_URL", DEFAULT_API_BASE_URL)).rstrip("/")
    request = Request(f"{base_url}/health", headers={"Accept": "application/json"})

    try:
        with urlopen(request, timeout=timeout) as response:
            if response.status != 200:
                return False
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, UnicodeDecodeError):
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
    page_keys = ("home", "profile", "pathways")
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

    if selected_page == "home":
        st.title(copy["title"])
        st.subheader(copy["tagline"])
        st.info(copy["notice"])
        st.write(copy["welcome"])
        st.markdown(f"**{copy['home_next']}**")
    elif selected_page == "profile":
        st.title(copy["profile_heading"])
        st.write(copy["profile_description"])
        st.info(copy["profile_placeholder"])
    else:
        st.title(copy["pathways_heading"])
        st.write(copy["pathways_description"])
        st.info(copy["pathways_placeholder"])

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

    st.caption(copy["footer"])


if __name__ == "__main__":
    main()
