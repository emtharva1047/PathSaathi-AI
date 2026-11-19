"""Bilingual rendering for source-backed NCVET/NQR qualification explainers."""

from __future__ import annotations

from datetime import date
from typing import Any

from core.eligibility import EligibilityStatus
from core.multi_route_eligibility import (
    LearnerEligibilityEvidence,
    MultiRouteQualificationCriteria,
    evaluate_multi_route_eligibility,
)
from core.profiles import EducationLevel
from core.qualification_explainers import (
    ExplainerStatus,
    QualificationExplainerRecord,
    QualificationFactKind,
    build_qualification_explainer,
)
from services.eligibility_catalogue import load_assistant_baking_technician_entry_criteria
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
        "record_checked": "NQR record checked",
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
            "Eligibility is assessed separately below using all four published alternative "
            "routes. Missing age, prior-qualification or experience evidence remains unknown. "
            "This is advisory screening, not an admission decision."
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
        "record_checked": "NQR नोंद पडताळली",
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
            "खालील विभागात पात्रतेचे चारही प्रकाशित पर्यायी मार्ग स्वतंत्रपणे तपासले आहेत. "
            "वय, पूर्व-पात्रता किंवा अनुभवाची माहिती उपलब्ध किंवा पडताळलेली नसल्यास ती अज्ञात "
            "राहते. ही प्राथमिक तपासणी आहे; प्रवेशाचा अंतिम निर्णय नाही."
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
            if record.record_source_publisher and record.record_last_verified_at:
                st.caption(
                    f"{record.record_source_publisher} · "
                    f"{copy['record_checked']} {record.record_last_verified_at.isoformat()}"
                )
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


ELIGIBILITY_COPY: dict[str, dict[str, Any]] = {
    "English": {
        "heading": "Qualification entry-route screening",
        "privacy_note": (
            "This screen uses only the education level from a learner profile explicitly kept "
            "in the current session. It does not ask for age, date of birth, prior qualification "
            "documents or work history. Missing facts remain unknown."
        ),
        "profile_missing": (
            "No session-only learner profile has been saved yet. All learner-specific conditions "
            "remain unknown until the learner chooses to save a profile."
        ),
        "result_label": "Overall preliminary result",
        "status_eligible": (
            "At least one complete published route appears to be met. The awarding body or "
            "provider must confirm the evidence; this is not an admission decision."
        ),
        "status_ineligible": (
            "Every published route was evaluated and at least one condition failed in each. "
            "Confirm equivalence with the awarding body or provider before ruling out this option."
        ),
        "status_unknown": (
            "Cannot determine yet. Some required learner information or verification is missing; "
            "no route has been assumed."
        ),
        "route_labels": {
            "grade-10": "Route 1 — Grade 10",
            "grade-8-plus-36-months": "Route 2 — Grade 8 plus 36 months of Food Industry experience",
            "prior-nsqf-2-5-plus-18-months": "Route 3 — Relevant NSQF 2.5+ plus 18 months of experience",
            "prior-nsqf-2-plus-36-months": "Route 4 — Relevant NSQF 2.0+ plus 36 months of experience",
        },
        "condition_labels": {
            "education_level": "Education requirement",
            "minimum_age": "Minimum age",
            "prior_nsqf": "Relevant prior NSQF qualification",
            "relevant_experience": "Relevant industry experience",
        },
        "condition_status": {
            "eligible": "Met",
            "ineligible": "Not met",
            "unknown": "Unknown — information missing or needs verification",
        },
        "source_link": "Open the exact qualification-file source",
        "source_checked": "Source checked",
        "criteria_current": "The published criteria are within their recorded validity period.",
        "criteria_expired": (
            "The qualification criteria are expired or their source is not currently verified. "
            "All route conditions are withheld as unknown."
        ),
        "missing_summary": (
            "{count} missing or unverified condition(s) are keeping the overall result unknown."
        ),
        "not_available": "not recorded",
        "advisory_note": (
            "This is not an admission decision. Age is represented only as completed years in the "
            "domain model. No date of birth, employer name, exact address or identity document is "
            "collected. Any eventual evidence requires appropriate consent and awarding-body/provider verification."
        ),
    },
    "मराठी": {
        "heading": "पात्रतेच्या प्रवेश मार्गांची प्राथमिक तपासणी",
        "privacy_note": (
            "या विभागात सध्याच्या सत्रात जतन केलेल्या विद्यार्थ्याच्या माहितीतील फक्त शिक्षणाचा "
            "वापर होतो. वय, जन्मतारीख, पूर्व-पात्रतेची कागदपत्रे किंवा कामाचा इतिहास विचारला जात नाही. "
            "गहाळ माहिती अज्ञात ठेवली जाते."
        ),
        "profile_missing": (
            "विद्यार्थ्याची सत्रापुरती माहिती अद्याप जतन केलेली नाही. विद्यार्थी माहिती जतन करेपर्यंत "
            "सर्व वैयक्तिक अटी अज्ञात राहतील."
        ),
        "result_label": "एकूण प्राथमिक निकाल",
        "status_eligible": (
            "प्रकाशित प्रवेश मार्गांपैकी किमान एक मार्ग पूर्ण झालेला दिसतो. प्रमाणपत्र देणारी संस्था "
            "किंवा प्रशिक्षण केंद्र पुरावा तपासेल; हा प्रवेशाचा अंतिम निर्णय नाही."
        ),
        "status_ineligible": (
            "प्रत्येक प्रकाशित मार्ग तपासला गेला आणि प्रत्येक मार्गातील किमान एक अट पूर्ण झाली नाही. "
            "हा पर्याय नाकारण्यापूर्वी संस्थेकडून समतुल्यता तपासा."
        ),
        "status_unknown": (
            "अद्याप निर्णय देता येत नाही. काही आवश्यक माहिती किंवा पडताळणी उपलब्ध नाही; कोणताही "
            "प्रवेश मार्ग गृहित धरलेला नाही."
        ),
        "route_labels": {
            "grade-10": "मार्ग १ — इयत्ता १० वी",
            "grade-8-plus-36-months": "मार्ग २ — इयत्ता ८ वी आणि अन्न उद्योगातील ३६ महिन्यांचा अनुभव",
            "prior-nsqf-2-5-plus-18-months": "मार्ग ३ — संबंधित NSQF २.५+ आणि १८ महिन्यांचा अनुभव",
            "prior-nsqf-2-plus-36-months": "मार्ग ४ — संबंधित NSQF २.०+ आणि ३६ महिन्यांचा अनुभव",
        },
        "condition_labels": {
            "education_level": "शिक्षणाची अट",
            "minimum_age": "किमान वय",
            "prior_nsqf": "संबंधित पूर्व NSQF पात्रता",
            "relevant_experience": "संबंधित उद्योगातील अनुभव",
        },
        "condition_status": {
            "eligible": "अट पूर्ण",
            "ineligible": "अट पूर्ण नाही",
            "unknown": "अज्ञात — माहिती अपुरी किंवा पडताळणी आवश्यक",
        },
        "source_link": "पात्रता फाइलमधील अचूक स्रोत उघडा",
        "source_checked": "स्रोत पडताळला",
        "criteria_current": "प्रकाशित निकष नोंदवलेल्या वैधता कालावधीत आहेत.",
        "criteria_expired": (
            "पात्रतेचे निकष कालबाह्य आहेत किंवा त्यांचा स्रोत सध्या पडताळलेला नाही. "
            "सर्व प्रवेश अटी अज्ञात ठेवल्या आहेत."
        ),
        "missing_summary": (
            "गहाळ किंवा अपडताळलेल्या {count} अटींमुळे एकूण निकाल अज्ञात आहे."
        ),
        "not_available": "नोंद उपलब्ध नाही",
        "advisory_note": (
            "हा प्रवेशाचा अंतिम निर्णय नाही. मॉडेलमध्ये वय फक्त पूर्ण झालेल्या वर्षांत वापरले जाते. "
            "जन्मतारीख, नियोक्त्याचे नाव, अचूक पत्ता किंवा ओळखपत्र गोळा केले जात नाही. पुढील पुराव्यासाठी "
            "योग्य संमती आणि प्रमाणपत्र देणाऱ्या संस्था किंवा प्रशिक्षण केंद्राची पडताळणी आवश्यक आहे."
        ),
    },
}


def _session_eligibility_evidence(st: Any) -> tuple[LearnerEligibilityEvidence, bool]:
    """Reuse only explicitly saved, session-local education; never infer missing facts."""
    session_state = getattr(st, "session_state", None)
    saved_context = (
        session_state.get("profile_saved_context")
        if hasattr(session_state, "get")
        else None
    )
    learner = getattr(saved_context, "learner", None)
    education_level = getattr(learner, "education_level", EducationLevel.UNKNOWN)
    if not isinstance(education_level, EducationLevel):
        education_level = EducationLevel.UNKNOWN
    return (
        LearnerEligibilityEvidence(education_level=education_level),
        saved_context is not None,
    )


def render_multi_route_eligibility(
    st: Any,
    locale: str,
    evidence: LearnerEligibilityEvidence | None = None,
    criteria: MultiRouteQualificationCriteria | None = None,
    *,
    as_of: date | None = None,
) -> None:
    """Render source-linked route/condition explanations without collecting new personal data."""
    copy = ELIGIBILITY_COPY[locale]
    criteria = criteria or load_assistant_baking_technician_entry_criteria()
    if evidence is None:
        evidence, has_saved_profile = _session_eligibility_evidence(st)
    else:
        has_saved_profile = evidence.education_level != EducationLevel.UNKNOWN

    today = as_of or date.today()
    criteria_current = criteria.source.is_current(today) and (
        criteria.valid_until is None or criteria.valid_until >= today
    )
    result = evaluate_multi_route_eligibility(evidence, criteria, as_of=today)

    st.subheader(copy["heading"])
    st.caption(copy["privacy_note"])
    if not has_saved_profile:
        st.info(copy["profile_missing"])

    if criteria_current:
        st.caption(copy["criteria_current"])
    else:
        st.warning(copy["criteria_expired"])

    status_label = copy[f"status_{result.status.value}"]
    st.markdown(f"**{copy['result_label']}**")
    if result.status == EligibilityStatus.ELIGIBLE:
        st.success(status_label)
    elif result.status == EligibilityStatus.INELIGIBLE:
        st.warning(status_label)
    else:
        st.info(status_label)

    explanation = result.explanation_en if locale == "English" else result.explanation_mr
    st.write(explanation)
    st.caption(
        f"{result.qualification_code} · {result.qualification_version} · "
        f"{result.source_publisher} · {copy['source_checked']} "
        f"{result.last_verified_at.isoformat() if result.last_verified_at else copy['not_available']}"
    )
    st.markdown(f"[{copy['source_link']}]({result.source_url})")

    route_sources = {route.route_id: route for route in criteria.routes}
    for route_result in result.route_evaluations:
        route = route_sources[route_result.route_id]
        route_label = copy["route_labels"].get(route.route_id, route.route_id)
        route_status = copy["condition_status"][route_result.status.value]
        st.markdown(f"**{route_label} — {route_status}**")
        for condition_result, condition in zip(
            route_result.conditions, route.conditions, strict=True
        ):
            condition_label = copy["condition_labels"][condition_result.condition_kind]
            condition_status = copy["condition_status"][condition_result.status.value]
            st.markdown(f"**{condition_label}: {condition_status}**")
            condition_explanation = (
                condition_result.explanation_en
                if locale == "English"
                else condition_result.explanation_mr
            )
            st.write(condition_explanation)
            st.caption(
                f"{condition.source.publisher} · {condition.source.reference} · "
                f"{copy['source_checked']} "
                f"{condition.source.last_verified_at.isoformat() if condition.source.last_verified_at else copy['not_available']}"
            )
            st.markdown(f"[{copy['source_link']}]({condition.source.url})")

    if result.missing_information:
        st.caption(copy["missing_summary"].format(count=len(result.missing_information)))
    st.caption(copy["advisory_note"])
