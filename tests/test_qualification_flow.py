"""Tests for bilingual rendering of the official qualification explainer."""

from dataclasses import replace
from datetime import date
from types import SimpleNamespace

from app.qualification_flow import (
    ELIGIBILITY_COPY,
    EXPLAINER_COPY,
    render_multi_route_eligibility,
    render_qualification_explainers,
)
from core.profiles import EducationLevel
from services.eligibility_catalogue import load_assistant_baking_technician_entry_criteria
from services.qualification_catalogue import load_official_qualification_examples


class FakeStreamlit:
    def __init__(self, session_state: dict | None = None) -> None:
        self.calls: list[tuple[str, tuple, dict]] = []
        self.session_state = session_state if session_state is not None else {}

    def __getattr__(self, name: str):
        def record(*args, **kwargs):
            self.calls.append((name, args, kwargs))
        return record


def rendered_text(fake: FakeStreamlit) -> str:
    return " ".join(
        str(value)
        for _, args, _ in fake.calls
        for value in args
    )


def test_explainer_copy_has_matching_english_and_marathi_keys() -> None:
    assert set(EXPLAINER_COPY["English"]) == set(EXPLAINER_COPY["मराठी"])


def test_english_explainer_shows_nsqf_entry_routes_duration_and_progression() -> None:
    fake = FakeStreamlit()

    render_qualification_explainers(fake, "English", as_of=date(2026, 11, 17))

    text = rendered_text(fake)
    assert "Assistant Baking Technician" in text
    assert "NSQF level: 3" in text
    assert "Grade 10 pass; no experience required." in text
    assert "300 hours" in text
    assert "Plant Biscuit Production Specialist" in text
    assert "not a nearby training-provider listing" in text
    assert "Eligibility is assessed separately below" in text
    assert "https://www.nqr.gov.in/qualifications/12209" in text
    assert "has not yet been reviewed" in text
    assert "NQR record checked" in text


def test_marathi_explainer_marks_translation_as_unreviewed() -> None:
    fake = FakeStreamlit()

    render_qualification_explainers(fake, "मराठी", as_of=date(2026, 11, 17))

    text = rendered_text(fake)
    assert "सहाय्यक बेकिंग तंत्रज्ञ" not in text  # The official title remains unchanged.
    assert "उत्पादने भाजणे" in text
    assert "पर्यायी प्रवेश मार्ग" in text
    assert "मराठी मजकूर हा प्राथमिक अनुवाद आहे" in text
    assert "प्रशिक्षण केंद्र" in text


def test_expired_record_displays_warning_and_withholds_qualification_facts() -> None:
    fake = FakeStreamlit()
    record = load_official_qualification_examples()[0]
    expired = replace(record, valid_until=date(2026, 11, 16))

    render_qualification_explainers(
        fake,
        "English",
        records=(expired,),
        as_of=date(2026, 11, 17),
    )

    text = rendered_text(fake)
    assert EXPLAINER_COPY["English"]["expired_note"] in text
    assert "Assistant Baking Technician" in text
    assert "Bake products, maintain consistent quality" not in text
    assert "Plant Biscuit Production Specialist" not in text



def test_eligibility_copy_has_matching_english_and_marathi_keys() -> None:
    assert set(ELIGIBILITY_COPY["English"]) == set(ELIGIBILITY_COPY["मराठी"])


def test_unknown_profile_renders_all_four_routes_and_exact_condition_sources() -> None:
    fake = FakeStreamlit()

    render_multi_route_eligibility(fake, "English", as_of=date(2026, 11, 19))

    text = rendered_text(fake)
    assert "Cannot determine yet" in text
    assert "No session-only learner profile has been saved yet" in text
    assert "Route 1 — Grade 10" in text
    assert "Route 2 — Grade 8 plus 36 months" in text
    assert "Route 3 — Relevant NSQF 2.5+" in text
    assert "Route 4 — Relevant NSQF 2.0+" in text
    assert "Age in completed years is needed" in text
    assert "A prior qualification record is needed" in text
    assert "https://www.nqr.gov.in/qualification/file/English%20Q-file%20Baking%20Tech..pdf" in text
    assert fake.calls


def test_saved_grade_10_profile_shows_met_education_but_unknown_age() -> None:
    fake = FakeStreamlit(
        {
            "profile_saved_context": SimpleNamespace(
                learner=SimpleNamespace(education_level=EducationLevel.GRADE_10)
            )
        }
    )

    render_multi_route_eligibility(fake, "English", as_of=date(2026, 11, 19))

    text = rendered_text(fake)
    assert "Recorded education (Grade 10) meets this route's published requirement." in text
    assert "Age in completed years is needed" in text
    assert "Cannot determine yet" in text
    assert "This is not an admission decision" in text


def test_marathi_eligibility_panel_explains_unknown_conditions() -> None:
    fake = FakeStreamlit()

    render_multi_route_eligibility(fake, "मराठी", as_of=date(2026, 11, 19))

    text = rendered_text(fake)
    assert "प्रवेशाचे सर्व पर्यायी मार्ग" in text
    assert "मार्ग १ — इयत्ता १० वी" in text
    assert "पूर्ण झालेल्या वर्षांतील वय आवश्यक आहे" in text
    assert "जन्मतारीख गोळा केली जात नाही" in text


def test_expired_criteria_withholds_every_route_as_unknown() -> None:
    fake = FakeStreamlit()
    criteria = replace(
        load_assistant_baking_technician_entry_criteria(),
        valid_until=date(2026, 11, 18),
    )

    render_multi_route_eligibility(
        fake,
        "English",
        criteria=criteria,
        as_of=date(2026, 11, 19),
    )

    text = rendered_text(fake)
    assert ELIGIBILITY_COPY["English"]["criteria_expired"] in text
    assert "Cannot determine yet" in text
    assert "The qualification criteria are expired or not currently verified." in text
    assert "Alternative route 1" in text
    assert "Route 1 — Grade 10" not in text
    assert "36 months of Food Industry experience" not in text
    assert "three years of relevant Food Industry experience" not in text
