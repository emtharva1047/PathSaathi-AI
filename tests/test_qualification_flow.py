"""Tests for bilingual rendering of the official qualification explainer."""

from dataclasses import replace
from datetime import date

from app.qualification_flow import EXPLAINER_COPY, render_qualification_explainers
from services.qualification_catalogue import load_official_qualification_examples


class FakeStreamlit:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple, dict]] = []

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
    assert "Eligibility is not calculated here" in text
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
