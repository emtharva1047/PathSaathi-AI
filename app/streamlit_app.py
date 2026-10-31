"""Initial Streamlit shell with English and Marathi navigation labels."""

import streamlit as st


TRANSLATIONS = {
    "English": {
        "title": "PathSaathi AI",
        "tagline": "Explore vocational pathways together.",
        "language": "Language",
        "welcome": "Start with a conversation about interests, skills and family questions.",
        "notice": "Guidance only: recommendations are not guarantees of admission, employment or earnings.",
    },
    "मराठी": {
        "title": "PathSaathi AI",
        "tagline": "व्यावसायिक शिक्षणाचे पर्याय एकत्र समजून घ्या.",
        "language": "भाषा",
        "welcome": "आवडी, कौशल्ये आणि कुटुंबाच्या प्रश्नांपासून सुरुवात करा.",
        "notice": "ही मार्गदर्शन सेवा आहे; प्रवेश, नोकरी किंवा उत्पन्नाची हमी नाही.",
    },
}


def main() -> None:
    """Render the first accessible application shell."""
    st.set_page_config(page_title="PathSaathi AI", page_icon="🎓", layout="centered")
    locale = st.sidebar.selectbox("Language / भाषा", list(TRANSLATIONS))
    copy = TRANSLATIONS[locale]

    st.title(copy["title"])
    st.subheader(copy["tagline"])
    st.info(copy["notice"])
    st.write(copy["welcome"])
    st.caption("Phase 2 foundation build — counselling, evidence and family workflows are coming next.")


if __name__ == "__main__":
    main()
