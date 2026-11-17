"""Bilingual rendering for source-backed NCVET/NQR qualification explainers."""

from __future__ import annotations

from datetime import date
from typing import Any

from core.qualification_explainers import (
    ExplainerStatus,
    QualificationExplainerRecord,
    QualificationFactKind,
    build_qualification_explainer,
)
from services.qualification_catalogue import load_official_qualification_examples


FACT_ORDER = (
    QualificationFactKind.JOB_DESCRIPTION,
    QualificationFactKind.ENTRY_ROUTE,
    QualificationFactKind.MINIMUM_AGE,
    QualificationFactKind.TRAINING_DURATION,
    QualificationFactKind.LEARNING_MODULE,
    QualificationFactKind.PROGRESSION,
)


EXPLAINER_COPY: dict[str, dict[str, Any]] = {
    "English": {
        "heading": "Official NQR qualification example",
        "scope_note": (
            "This is one national qualification record. It is not a nearby training-provider "
            "listing, a seat-availability check or an employment outcome."
        ),
        "qualification_code": "Qualification code",
        "awarding_body": "Awarding body",
        "nsqf_level": "NSQF level",
        "valid_until": "NQR validity shown through",
        "current_note": "The NQR record is listed as current through {valid_until}. Re-check the record before applying.",
        "partial_note": "Only claims with complete, current source references are shown; other claims remain unknown.",
        "expired_note": "This qualification record is expired as of the selected date. Its claims are withheld from current guidance.",
        "archived_note": "This qualification is archived. Its claims are withheld from current guidance.",
        "unknown_note": "The qualification status or source is not verified. Job-role, entry and progression details remain unknown.",
        "job_description": "What the job role involves",
        "entry_route": "Alternative entry routes",
        "minimum_age": "Minimum age",
        "training_duration": "Total training duration",
        "learning_module": "Learning modules",
        "progression": "Published progression pathway",
        "nqr_link": "Open NQR qualification record",
        "file_link": "Open official qualification file",
        "source_reference": "Source reference",
        "verified_on": "Checked",
        "withheld": "Unverified or stale claims withheld",
        "eligibility_note": (
            "Eligibility is not calculated here. This qualification has alternative education "
            "and experience routes plus a minimum-age condition; the current education-only "
            "evaluator cannot safely assess all of them. Confirm every condition with the awarding "
            "body or provider."
        ),
        "availability_note": (
            "A national qualification record does not confirm a training provider, available "
            "seats, fees or delivery in the learner's district."
        ),
        "translation_note": (
            "Marathi text is a draft translation and has not yet been reviewed by a fluent "
            "human reviewer."
        ),
        "translation_reviewed": "Marathi wording has received human review.",
    },
    "मराठी": {
        "heading": "NQR मधील अधिकृत पात्रतेचे उदाहरण",
        "scope_note": (
            "ही राष्ट्रीय पात्रता नोंदींपैकी एक आहे. ही जवळच्या प्रशिक्षण संस्थेची यादी, "
            "जागांची उपलब्धता किंवा रोजगाराचा निकाल नाही."
        ),
        "qualification_code": "पात्रता संकेतांक",
        "awarding_body": "प्रमाणपत्र देणारी संस्था",
        "nsqf_level": "NSQF स्तर",
        "valid_until": "NQR नोंदीनुसार वैधता",
        "current_note": "NQR नोंद {valid_until} पर्यंत वैध दाखवली आहे. अर्ज करण्यापूर्वी नोंद पुन्हा तपासा.",
        "partial_note": "पूर्ण आणि अद्ययावत स्रोत असलेली माहितीच दाखवली आहे; इतर माहिती अज्ञात राहते.",
        "expired_note": "निवडलेल्या तारखेनुसार ही पात्रता कालबाह्य आहे. सध्याच्या मार्गदर्शनातून तिचे तपशील लपवले आहेत.",
        "archived_note": "ही पात्रता संग्रहित आहे. सध्याच्या मार्गदर्शनातून तिचे तपशील लपवले आहेत.",
        "unknown_note": "पात्रतेची स्थिती किंवा स्रोत पडताळलेला नाही. काम, प्रवेश आणि प्रगतीचे तपशील अज्ञात आहेत.",
        "job_description": "या कामात काय करावे लागते",
        "entry_route": "प्रवेशाचे पर्यायी मार्ग",
        "minimum_age": "किमान वय",
        "training_duration": "एकूण प्रशिक्षण कालावधी",
        "learning_module": "अभ्यासाचे घटक",
        "progression": "प्रकाशित प्रगतीचा मार्ग",
        "nqr_link": "NQR पात्रता नोंद उघडा",
        "file_link": "अधिकृत पात्रता फाइल उघडा",
        "source_reference": "स्रोताचा संदर्भ",
        "verified_on": "पडताळणी",
        "withheld": "न पडताळलेली किंवा जुनी माहिती लपवली आहे",
        "eligibility_note": (
            "येथे पात्रतेचा निर्णय दिला जात नाही. या पात्रतेमध्ये शिक्षण आणि अनुभवाचे "
            "पर्यायी मार्ग तसेच किमान वयाची अट आहे. सध्याची शिक्षणापुरती तपासणी या सर्व अटी "
            "सुरक्षितपणे तपासू शकत नाही. प्रमाणपत्र देणाऱ्या संस्था किंवा प्रशिक्षण केंद्राकडून "
            "प्रत्येक अट तपासा."
        ),
        "availability_note": (
            "राष्ट्रीय पात्रता नोंदीमुळे विद्यार्थ्याच्या जिल्ह्यात प्रशिक्षण केंद्र, जागा, "
            "शुल्क किंवा अभ्यासक्रम उपलब्ध असल्याची खात्री होत नाही."
        ),
        "translation_note": (
            "मराठी मजकूर हा प्राथमिक अनुवाद आहे. त्याची तज्ज्ञ मराठी भाषातज्ज्ञाकडून "
            "पडताळणी झालेली नाही."
        ),
        "translation_reviewed": "मराठी मजकुराची मानवी पडताळणी झाली आहे.",
    },
}


def _format_level(value: object) -> str:
    return format(value.normalize(), "f") if hasattr(value, "normalize") else str(value)


def render_qualification_explainers(
    st: Any,
    locale: str,
    records: tuple[QualificationExplainerRecord, ...] | None = None,
    *,
    as_of: date | None = None,
) -> None:
    """Render only current, source-verified qualification claims."""
    copy = EXPLAINER_COPY[locale]
    st.subheader(copy["heading"])
    st.caption(copy["scope_note"])

    catalogue = records if records is not None else load_official_qualification_examples()
    for record in catalogue:
        view = build_qualification_explainer(record, as_of=as_of)
        course = record.course
        st.write(f"{course.title} — {course.trade}")
        st.write(f"{copy['qualification_code']}: {course.qualification_code}")
        if course.awarding_body:
            st.write(f"{copy['awarding_body']}: {course.awarding_body}")

        if view.status == ExplainerStatus.EXPIRED:
            st.warning(copy["expired_note"])
        elif view.status == ExplainerStatus.ARCHIVED:
            st.warning(copy["archived_note"])
        elif view.status == ExplainerStatus.UNKNOWN:
            st.info(copy["unknown_note"])
        elif view.status == ExplainerStatus.PARTIAL:
            st.warning(copy["partial_note"])
        else:
            valid_until = record.valid_until.isoformat() if record.valid_until else "not stated"
            st.success(copy["current_note"].format(valid_until=valid_until))

        if view.status in {ExplainerStatus.CURRENT, ExplainerStatus.PARTIAL}:
            if course.nsqf_level is not None:
                st.write(f"{copy['nsqf_level']}: {_format_level(course.nsqf_level)}")
            if record.valid_until is not None:
                st.write(f"{copy['valid_until']}: {record.valid_until.isoformat()}")
            if record.nqr_record_url:
                st.markdown(f"[{copy['nqr_link']}]({record.nqr_record_url})")
            if course.source_url:
                st.markdown(f"[{copy['file_link']}]({course.source_url})")

            for kind in FACT_ORDER:
                facts = tuple(fact for fact in view.visible_facts if fact.kind == kind)
                if not facts:
                    continue
                st.markdown(f"**{copy[kind.value]}**")
                for fact in facts:
                    text = fact.text_en if locale == "English" else fact.text_mr
                    st.write(text)
                    st.caption(
                        f"{fact.source_publisher} · {fact.source_reference} · "
                        f"{copy['verified_on']} {fact.last_verified_at.isoformat()}"
                    )
                    st.markdown(f"[{copy['source_reference']}]({fact.source_url})")

            if view.withheld_fact_count:
                st.caption(f"{copy['withheld']}: {view.withheld_fact_count}")
            st.caption(copy["eligibility_note"])
            st.caption(copy["availability_note"])

        if record.marathi_translation_reviewed:
            st.caption(copy["translation_reviewed"])
        else:
            st.caption(copy["translation_note"])
