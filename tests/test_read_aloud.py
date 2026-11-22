"""Tests for the opt-in browser-native read-aloud control."""

from __future__ import annotations

from types import SimpleNamespace

from app.read_aloud import (
    LOCALE_TAGS,
    READ_ALOUD_COPY,
    build_read_aloud_html,
    render_read_aloud,
)


class FakeStreamlit:
    """Capture the caption and embedded component without launching a browser."""

    def __init__(self) -> None:
        self.captions: list[str] = []
        self.html_calls: list[tuple[str, int, bool]] = []
        self.components = SimpleNamespace(v1=SimpleNamespace(html=self._html))

    def caption(self, value: str) -> None:
        self.captions.append(value)

    def _html(self, markup: str, *, height: int, scrolling: bool) -> None:
        self.html_calls.append((markup, height, scrolling))


def test_locales_have_matching_read_aloud_copy_and_voice_tags() -> None:
    assert set(READ_ALOUD_COPY) == set(LOCALE_TAGS)
    assert set(READ_ALOUD_COPY["English"]) == set(READ_ALOUD_COPY["मराठी"])
    assert LOCALE_TAGS == {"English": "en-IN", "मराठी": "mr-IN"}


def test_html_escapes_visible_text_and_exposes_keyboard_accessible_controls() -> None:
    source = 'A & B <script>alert("not executable")</script>'
    markup = build_read_aloud_html(source, "English")

    assert (
        'data-text="A &amp; B &lt;script&gt;alert(&quot;not executable&quot;)'
        '&lt;/script&gt;"'
    ) in markup
    assert 'type="button"' in markup
    assert 'aria-live="polite"' in markup
    assert "focus-visible" in markup
    assert "speechSynthesis" in markup
    assert "synth.speak(utterance)" in markup


def test_speech_starts_only_from_explicit_read_button_and_stop_is_available() -> None:
    markup = build_read_aloud_html("A short introduction.", "English")

    click_handler = 'readButton.addEventListener("click"'
    assert click_handler in markup
    assert markup.index(click_handler) < markup.index("synth.speak(utterance)")
    assert 'stopButton.addEventListener("click"' in markup
    assert 'window.addEventListener("pagehide"' in markup
    assert "synth.cancel()" in markup


def test_marathi_html_requires_a_marathi_voice_and_localises_controls() -> None:
    markup = build_read_aloud_html("विद्यार्थ्यांसाठी माहिती.", "मराठी")

    assert 'lang="mr-IN"' in markup
    assert 'data-locale="mr-IN"' in markup
    assert "पानाची ओळख मोठ्याने वाचा" in markup
    assert "वाचन थांबवा" in markup
    assert "या भाषेसाठी उपकरणात आवाज उपलब्ध नाही." in markup


def test_render_read_aloud_keeps_visible_hint_and_uses_non_scrolling_frame() -> None:
    fake = FakeStreamlit()
    render_read_aloud(fake, "Visible introduction.", "English")

    assert fake.captions == [READ_ALOUD_COPY["English"]["hint"]]
    assert len(fake.html_calls) == 1
    markup, height, scrolling = fake.html_calls[0]
    assert "Visible introduction." in markup
    assert height == 118
    assert scrolling is False


def test_render_read_aloud_skips_empty_text() -> None:
    fake = FakeStreamlit()
    render_read_aloud(fake, "   ", "मराठी")

    assert fake.captions == []
    assert fake.html_calls == []
