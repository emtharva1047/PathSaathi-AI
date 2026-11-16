"""Bilingual Streamlit rendering for transparent advisory pathway exploration."""

from __future__ import annotations

from typing import Any

from app.profile_flow import build_family_context
from core.domain import CourseRecord
from core.eligibility import EligibilityStatus
from core.pathways import AdvisoryPathway, ShortlistState, build_pathway_shortlist


DEMO_PATHWAYS = (
    AdvisoryPathway(
        course=CourseRecord(
            course_id="demo-technology-support",
            title="Illustrative technology-support theme",
            trade="Technology support",
            verification_status="synthetic_demo",
        ),
        display_title_mr="तंत्रज्ञान सहाय्य — केवळ उदाहरण",
        display_trade_mr="तंत्रज्ञान सहाय्य",
        interest_tags=("technology", "working_with_people"),
        work_preference_tags=("computer_based", "people_facing"),
    ),
    AdvisoryPathway(
        course=CourseRecord(
            course_id="demo-repair-maintenance",
            title="Illustrative repair and maintenance theme",
            trade="Repair and maintenance",
            verification_status="synthetic_demo",
        ),
        display_title_mr="दुरुस्ती आणि देखभाल — केवळ उदाहरण",
        display_trade_mr="दुरुस्ती आणि देखभाल",
        interest_tags=("repair_and_making", "technology"),
        work_preference_tags=("hands_on", "independent_work"),
    ),
    AdvisoryPathway(
        course=CourseRecord(
            course_id="demo-creative-production",
            title="Illustrative creative-production theme",
            trade="Creative production",
            verification_status="synthetic_demo",
        ),
        display_title_mr="सर्जनशील निर्मिती — केवळ उदाहरण",
        display_trade_mr="सर्जनशील निर्मिती",
        interest_tags=("design_and_creativity",),
        work_preference_tags=("indoor", "computer_based"),
    ),
    AdvisoryPathway(
        course=CourseRecord(
            course_id="demo-agriculture-services",
            title="Illustrative agriculture and nature theme",
            trade="Agriculture and nature services",
            verification_status="synthetic_demo",
        ),
        display_title_mr="शेती आणि निसर्ग सेवा — केवळ उदाहरण",
        display_trade_mr="शेती आणि निसर्ग सेवा",
        interest_tags=("agriculture_and_nature",),
        work_preference_tags=("outdoor", "hands_on"),
    ),
)


PATHWAY_COPY: dict[str, dict[str, Any]] = {
    "English": {
        "catalogue_notice": (
            "Illustrative demo catalogue only. These are not official course listings, "
            "NCVET/NQR records, NSQF mappings, fees or outcome records."
        ),
        "learner_agency": (
            "Only the learner's stated interests and work preferences drive this shortlist. "
            "Parent concerns and priorities stay separate for family discussion."
        ),
        "matches_heading": "Preference matches with verified education eligibility",
        "verification_heading": "Preference matches — eligibility not yet confirmed",
        "verification_notice": (
            "These options match the learner's stated preferences but are not eligible until "
            "official entry criteria and learner information are verified. They are shown "
            "for discussion, not as eligible recommendations."
        ),
        "no_eligible": (
            "No preference match currently has a verified eligible result. Unknown or "
            "ineligible must not be treated as eligible."
        ),
        "explore_heading": "Explore all other pathways",
        "no_preferences": (
            "No learner interests or work preferences were shared. No shortlist is generated; "
            "all options remain open to explore."
        ),
        "no_matches": (
            "No illustrative options match the selected preferences. Every option remains "
            "available to explore."
        ),
        "no_catalogue": "No pathway catalogue is available yet. No recommendation was generated.",
        "eligible_match_label": "Preference match and verified education criterion met",
        "verification_match_label": "Preference match — eligibility unknown; not an eligible recommendation",
        "ineligible_label": (
            "Preference match, but the published education criterion is not met; confirm equivalence"
        ),
        "also_match_label": "Also matches preferences but is outside the shortlist display limit",
        "no_match_label": "No selected preference match — still available to explore",
        "why_label": "Why this option appears",
        "eligibility_label": "Education eligibility",
        "eligibility_scope": (
            "This checks only a published education requirement. It is not an admission "
            "decision; other conditions may apply."
        ),
        "eligibility_status": {
            "eligible": "Eligible against the published education criterion only",
            "ineligible": "Published education criterion not met; confirm equivalence before ruling it out",
            "unknown": "Unknown — verified entry criteria or learner information are missing",
        },
        "eligibility_explanations": {
            "criteria_not_available": "Official entry criteria are not loaded for this option.",
            "criteria_not_verified": "The entry criteria are not sufficiently verified.",
            "learner_education_unknown": "The learner's completed education level was not shared.",
            "published_education_requirement_met": (
                "The recorded education level matches the published criterion. Other entry "
                "conditions and the provider's decision still apply."
            ),
            "published_education_requirement_not_met": (
                "The recorded level is not in the published accepted list. Confirm equivalence "
                "with the awarding body or provider before ruling out this option."
            ),
        },
        "synthetic_label": (
            "Synthetic demonstration record — not an official qualification or outcome record."
        ),
        "verified_label": (
            "Catalogue source marked verified; confirm current course availability with the provider."
        ),
        "review_label": "Catalogue source needs review before relying on this listing.",
        "stale_label": "Catalogue source is marked stale; verify it before relying on this listing.",
        "source_label": "Qualification source",
        "nsqf_label": "NSQF level",
        "no_more_options": "All catalogue options are shown above.",
    },
    "मराठी": {
        "catalogue_notice": (
            "ही केवळ उदाहरणासाठीची नमुना यादी आहे. हे अधिकृत अभ्यासक्रम, NCVET/NQR नोंदी, "
            "NSQF स्तर, शुल्क किंवा रोजगारविषयक पुरावे नाहीत."
        ),
        "learner_agency": (
            "ही यादी फक्त विद्यार्थ्याने सांगितलेल्या आवडी आणि कामाच्या आवडींवर आधारित आहे. "
            "पालकांच्या चिंता आणि प्राधान्ये कौटुंबिक चर्चेसाठी वेगळी ठेवली आहेत."
        ),
        "matches_heading": "शिक्षणाच्या पडताळलेल्या अटी पूर्ण करणारे जुळणारे पर्याय",
        "verification_heading": "आवडींशी जुळणारे पर्याय — पात्रतेची पुष्टी बाकी",
        "verification_notice": (
            "हे पर्याय विद्यार्थ्याच्या आवडींशी जुळतात; परंतु अधिकृत प्रवेशाच्या अटी आणि "
            "विद्यार्थ्याची माहिती पडताळल्याशिवाय पात्र मानता येणार नाहीत. हे चर्चेसाठीचे पर्याय आहेत."
        ),
        "no_eligible": (
            "सध्या कोणत्याही जुळणाऱ्या पर्यायासाठी पात्रतेची पडताळलेली पुष्टी नाही. "
            "माहिती नसणे किंवा अपात्र असणे म्हणजे पात्र असणे नाही."
        ),
        "explore_heading": "इतर सर्व पर्याय पाहा",
        "no_preferences": (
            "विद्यार्थ्याच्या आवडी किंवा कामाच्या आवडी दिलेल्या नाहीत. त्यामुळे यादी तयार "
            "केलेली नाही; सर्व पर्याय पाहण्यासाठी खुले आहेत."
        ),
        "no_matches": (
            "निवडलेल्या आवडींशी नमुना पर्याय जुळत नाहीत. तरीही प्रत्येक पर्याय पाहता येईल."
        ),
        "no_catalogue": "अभ्यासक्रमांची यादी अद्याप उपलब्ध नाही. कोणतीही शिफारस तयार केलेली नाही.",
        "eligible_match_label": "आवडींशी जुळतो आणि शिक्षणाची पडताळलेली अट पूर्ण करतो",
        "verification_match_label": "आवडींशी जुळतो — पात्रता अज्ञात; पात्र शिफारस नाही",
        "ineligible_label": "आवडींशी जुळतो; पण प्रकाशित शिक्षणाची अट पूर्ण नाही. समकक्षता तपासा",
        "also_match_label": "आवडींशी जुळणारा आणखी पर्याय; मुख्य यादीच्या मर्यादेबाहेर",
        "no_match_label": "निवडलेल्या आवडींशी जुळत नाही — तरीही पाहण्यासाठी उपलब्ध",
        "why_label": "हा पर्याय का दाखवला आहे",
        "eligibility_label": "शिक्षणाच्या अटींनुसार पात्रता",
        "eligibility_scope": (
            "ही तपासणी फक्त प्रकाशित शिक्षणाच्या अटींबाबत आहे. हा प्रवेशाचा निर्णय नाही; "
            "इतर अटी लागू असू शकतात."
        ),
        "eligibility_status": {
            "eligible": "फक्त प्रकाशित शिक्षणाची अट पूर्ण होते",
            "ineligible": "प्रकाशित शिक्षणाची अट पूर्ण होत नाही; नाकारण्यापूर्वी समकक्षतेची खात्री करा",
            "unknown": "माहित नाही — पडताळलेल्या प्रवेशाच्या अटी किंवा विद्यार्थ्याची माहिती अपुरी आहे",
        },
        "eligibility_explanations": {
            "criteria_not_available": "या पर्यायाच्या अधिकृत प्रवेशाच्या अटी उपलब्ध नाहीत.",
            "criteria_not_verified": "प्रवेशाच्या अटींची पुरेशी पडताळणी झालेली नाही.",
            "learner_education_unknown": "विद्यार्थ्याने पूर्ण केलेल्या शिक्षणाची माहिती दिलेली नाही.",
            "published_education_requirement_met": (
                "नोंदवलेले शिक्षण प्रकाशित अटींशी जुळते. इतर अटी आणि संस्थेचा निर्णय लागू राहतो."
            ),
            "published_education_requirement_not_met": (
                "नोंदवलेले शिक्षण स्वीकारलेल्या यादीत नाही. हा पर्याय नाकारण्यापूर्वी "
                "प्राधिकरण किंवा संस्थेकडून समकक्षतेची खात्री करा."
            ),
        },
        "synthetic_label": (
            "संगणकीय नमुना नोंद — अधिकृत पात्रता किंवा रोजगारविषयक पुरावा नाही."
        ),
        "verified_label": (
            "अभ्यासक्रमाचा स्रोत पडताळलेला आहे; उपलब्धता संस्थेकडून पुन्हा तपासा."
        ),
        "review_label": "या नोंदीवर अवलंबून राहण्यापूर्वी स्रोताची पडताळणी आवश्यक आहे.",
        "stale_label": "स्रोत जुना असल्याचे नोंदले आहे; वापरण्यापूर्वी पुन्हा तपासा.",
        "source_label": "पात्रतेचा स्रोत",
        "nsqf_label": "NSQF स्तर",
        "no_more_options": "यादीतील सर्व पर्याय वर दाखवले आहेत.",
    },
}


def _catalogue_status(pathway: AdvisoryPathway, copy: dict[str, Any]) -> str:
    status = pathway.course.verification_status
    if status == "synthetic_demo":
        return copy["synthetic_label"]
    if pathway.course.has_verified_source:
        return copy["verified_label"]
    if status == "stale":
        return copy["stale_label"]
    return copy["review_label"]


def _render_option(
    st: Any,
    recommendation: Any,
    locale: str,
    copy: dict[str, Any],
    status_label: str,
) -> None:
    pathway = recommendation.pathway
    title = pathway.course.title if locale == "English" else pathway.display_title_mr
    trade = pathway.course.trade if locale == "English" else pathway.display_trade_mr
    st.write(f"{title} — {trade}")
    st.caption(status_label)
    explanation = (
        recommendation.explanation_en if locale == "English" else recommendation.explanation_mr
    )
    st.write(f"{copy['why_label']}: {explanation}")
    status = recommendation.eligibility.status.value
    st.write(f"{copy['eligibility_label']}: {copy['eligibility_status'][status]}")
    st.caption(
        copy["eligibility_explanations"].get(
            recommendation.eligibility.reason_code,
            copy["eligibility_scope"],
        )
    )
    st.caption(_catalogue_status(pathway, copy))
    if pathway.course.nsqf_level is not None:
        st.write(f"{copy['nsqf_label']}: {pathway.course.nsqf_level}")
    if recommendation.eligibility.source_url:
        st.write(
            f"{copy['source_label']}: {recommendation.eligibility.source_publisher} — "
            f"{recommendation.eligibility.source_url}"
        )


def render_pathway_explorer(
    st: Any,
    locale: str,
    pathways: tuple[AdvisoryPathway, ...] = DEMO_PATHWAYS,
) -> None:
    """Render the full option set; a shortlist never removes an exploration choice."""
    copy = PATHWAY_COPY[locale]
    context = build_family_context(st.session_state, locale)
    result = build_pathway_shortlist(context.learner, pathways)

    st.info(copy["catalogue_notice"])
    st.caption(copy["learner_agency"])

    if result.state == ShortlistState.NO_CATALOGUE:
        st.info(copy["no_catalogue"])
        return
    if result.state == ShortlistState.NO_PREFERENCES:
        st.info(copy["no_preferences"])
    elif result.state == ShortlistState.NO_MATCHES:
        st.info(copy["no_matches"])
    elif result.state == ShortlistState.MATCHES_NOT_ELIGIBLE:
        st.info(copy["no_eligible"])

    if result.shortlist:
        st.subheader(copy["matches_heading"])
        for recommendation in result.shortlist:
            _render_option(
                st, recommendation, locale, copy, copy["eligible_match_label"]
            )

    if result.needs_verification:
        st.subheader(copy["verification_heading"])
        st.info(copy["verification_notice"])
        for recommendation in result.needs_verification:
            _render_option(
                st, recommendation, locale, copy, copy["verification_match_label"]
            )

    st.subheader(copy["explore_heading"])
    for recommendation in result.explore_all:
        if recommendation.eligibility.status == EligibilityStatus.INELIGIBLE:
            status_label = copy["ineligible_label"]
        elif recommendation.matches_preferences:
            status_label = copy["also_match_label"]
        else:
            status_label = copy["no_match_label"]
        _render_option(st, recommendation, locale, copy, status_label)
    if not result.explore_all:
        st.caption(copy["no_more_options"])
