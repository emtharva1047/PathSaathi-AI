"""Opt-in browser-native read-aloud for visible page introductions.

Speech is started only by an explicit user action. Text remains visible in the
main Streamlit page; audio is neither recorded nor sent to a remote service.
"""

from __future__ import annotations

from html import escape


LOCALE_TAGS = {"English": "en-IN", "मराठी": "mr-IN"}

READ_ALOUD_COPY = {
    "English": {
        "read": "Read page introduction aloud",
        "stop": "Stop reading",
        "hint": (
            "Optional: uses a voice installed on this device. Availability varies by "
            "browser and language; the text remains visible."
        ),
        "unsupported": "Read-aloud is not supported by this browser.",
        "no_voice": (
            "No installed voice for this language was found. You can still read the "
            "text on screen."
        ),
        "voice_pending": "Checking available device voices…",
        "ready": "Ready. Select Read page introduction aloud to listen.",
        "speaking": "Reading aloud.",
        "finished": "Finished reading.",
        "stopped": "Reading stopped.",
        "error": (
            "The browser could not start read-aloud. The text remains available "
            "on screen."
        ),
    },
    "मराठी": {
        "read": "पानाची ओळख मोठ्याने वाचा",
        "stop": "वाचन थांबवा",
        "hint": (
            "ऐच्छिक: या उपकरणात उपलब्ध असलेला आवाज वापरला जातो. ब्राउझर आणि "
            "भाषेनुसार आवाज उपलब्धता बदलू शकते; मजकूर स्क्रीनवरही उपलब्ध आहे."
        ),
        "unsupported": "या ब्राउझरमध्ये मोठ्याने वाचण्याची सुविधा उपलब्ध नाही.",
        "no_voice": (
            "या भाषेसाठी उपकरणात आवाज उपलब्ध नाही. मजकूर स्क्रीनवर वाचता येईल."
        ),
        "voice_pending": "उपलब्ध आवाज तपासत आहे…",
        "ready": "तयार. ऐकण्यासाठी मोठ्याने वाचा निवडा.",
        "speaking": "मोठ्याने वाचत आहे.",
        "finished": "वाचन पूर्ण झाले.",
        "stopped": "वाचन थांबवले.",
        "error": "ब्राउझरला मोठ्याने वाचता आले नाही. मजकूर स्क्रीनवर उपलब्ध आहे.",
    },
}


def build_read_aloud_html(text: str, locale: str) -> str:
    """Build an escaped, user-initiated speech control for an installed device voice."""
    copy = READ_ALOUD_COPY.get(locale, READ_ALOUD_COPY["English"])
    language = LOCALE_TAGS.get(locale, LOCALE_TAGS["English"])
    attributes = {
        "text": text,
        "locale": language,
        "unsupported": copy["unsupported"],
        "no_voice": copy["no_voice"],
        "voice_pending": copy["voice_pending"],
        "ready": copy["ready"],
        "speaking": copy["speaking"],
        "finished": copy["finished"],
        "stopped": copy["stopped"],
        "error": copy["error"],
    }
    data_attributes = " ".join(
        f'data-{name.replace("_", "-")}="{escape(value, quote=True)}"'
        for name, value in attributes.items()
    )
    read_label = escape(copy["read"], quote=True)
    stop_label = escape(copy["stop"], quote=True)

    return f"""
<section id="pathsaathi-read-aloud" lang="{language}" {data_attributes}>
  <style>
    #pathsaathi-read-aloud .controls {{ display: flex; flex-wrap: wrap; gap: 0.6rem; }}
    #pathsaathi-read-aloud button {{
      min-height: 44px; padding: 0.65rem 1rem; border: 2px solid #17324d;
      border-radius: 8px; background: #17324d; color: #fff;
      font: inherit; font-weight: 600; cursor: pointer;
    }}
    #pathsaathi-read-aloud button.secondary {{ background: #fff; color: #17324d; }}
    #pathsaathi-read-aloud button:focus-visible {{
      outline: 3px solid #b45309; outline-offset: 3px;
    }}
    #pathsaathi-read-aloud button:disabled {{ opacity: 0.55; cursor: not-allowed; }}
    #pathsaathi-read-aloud .status {{ margin: 0.5rem 0 0; font-size: 0.9rem; }}
  </style>
  <div class="controls">
    <button type="button" data-action="read">{read_label}</button>
    <button type="button" class="secondary" data-action="stop" disabled>{stop_label}</button>
  </div>
  <p class="status" data-status role="status" aria-live="polite">{escape(copy["voice_pending"])}</p>
</section>
<script>
(() => {{
  const root = document.getElementById("pathsaathi-read-aloud");
  if (!root) return;

  const readButton = root.querySelector('[data-action="read"]');
  const stopButton = root.querySelector('[data-action="stop"]');
  const status = root.querySelector("[data-status]");
  const synth = window.speechSynthesis;
  const supported = Boolean(
    synth && typeof window.SpeechSynthesisUtterance === "function"
  );
  let stoppedByUser = false;

  function findVoice() {{
    if (!supported) return null;
    const voices = synth.getVoices();
    const language = root.dataset.locale.toLowerCase();
    const baseLanguage = language.split("-")[0];
    return voices.find((voice) => voice.lang.toLowerCase() === language)
      || voices.find((voice) => {{
        const candidate = voice.lang.toLowerCase();
        return candidate === baseLanguage || candidate.startsWith(baseLanguage + "-");
      }});
  }}

  function refreshStatus() {{
    if (!supported) {{
      readButton.disabled = true;
      stopButton.disabled = true;
      status.textContent = root.dataset.unsupported;
      return;
    }}
    const voices = synth.getVoices();
    if (!voices.length) {{
      status.textContent = root.dataset.voicePending;
    }} else {{
      status.textContent = findVoice() ? root.dataset.ready : root.dataset.noVoice;
    }}
  }}

  readButton.addEventListener("click", () => {{
    if (!supported) {{
      status.textContent = root.dataset.unsupported;
      return;
    }}
    const voice = findVoice();
    if (!voice) {{
      status.textContent = synth.getVoices().length
        ? root.dataset.noVoice : root.dataset.voicePending;
      return;
    }}

    synth.cancel();
    stoppedByUser = false;
    const utterance = new window.SpeechSynthesisUtterance(root.dataset.text);
    utterance.voice = voice;
    utterance.lang = voice.lang || root.dataset.locale;
    utterance.rate = 0.95;
    utterance.onstart = () => {{
      stopButton.disabled = false;
      status.textContent = root.dataset.speaking;
    }};
    utterance.onend = () => {{
      stopButton.disabled = true;
      status.textContent = root.dataset.finished;
    }};
    utterance.onerror = () => {{
      stopButton.disabled = true;
      if (!stoppedByUser) status.textContent = root.dataset.error;
    }};
    stopButton.disabled = false;
    synth.speak(utterance);
  }});

  stopButton.addEventListener("click", () => {{
    if (supported) synth.cancel();
    stoppedByUser = true;
    stopButton.disabled = true;
    status.textContent = root.dataset.stopped;
  }});

  if (supported) {{
    if (typeof synth.addEventListener === "function") {{
      synth.addEventListener("voiceschanged", refreshStatus);
    }} else {{
      synth.onvoiceschanged = refreshStatus;
    }}
  }}
  window.addEventListener("pagehide", () => {{
    if (supported) synth.cancel();
  }});
  refreshStatus();
}})();
</script>
"""


def render_read_aloud(st: object, text: str, locale: str) -> None:
    """Render optional read-aloud controls without collecting or transmitting audio."""
    if not text.strip():
        return
    copy = READ_ALOUD_COPY.get(locale, READ_ALOUD_COPY["English"])
    st.caption(copy["hint"])
    st.components.v1.html(
        build_read_aloud_html(text, locale),
        height=118,
        scrolling=False,
    )
