# Accessibility implementation review

**Review date:** 5 November 2026  
**Scope:** Static code and interaction-contract review of the English/Marathi Streamlit shell.  
**Status:** Implementation improvements recorded; target-user and assistive-technology validation remain open.

## Scope and method

The review inspected the current Streamlit shell, its locale catalogue and the existing automated tests. It assessed whether the shell exposes the low-literacy navigation cues required by the project brief. No participant sessions, browser-based screen-reader tests, contrast measurements or human translation review were performed. This document is therefore an implementation review, not a usability study or an accessibility-conformance claim.

## Findings and changes

| Area | Finding before this increment | Change in this increment |
|---|---|---|
| Progress | The user could select a section, but there was no explicit indication of their position in the three-section journey. | Added a labelled step indicator and progress bar in both locales. |
| Back/continue | Navigation depended on the sidebar section list; the main content had no explicit step controls. | Added labelled Back and Continue controls where a previous or next section exists. |
| Help | The shell had no contextual help affordance. | Added a Help expander explaining navigation, language switching and the prototype's no-data-collection status. |
| Localisation | Navigation labels were translated, but step/help/control copy did not yet exist. | Added matching English and Marathi keys. Stable internal page keys keep navigation state independent of translated labels. |
| Regression coverage | Tests checked translation-key parity and API fallback, but not the rendered navigation affordances. | Added render-contract tests for the English home state and Marathi profile state. |

## Existing safeguards retained

- Language selection remains labelled and available in the sidebar.
- The API status and offline fallback remain visible; the informational shell does not require the API to be online.
- The current placeholder profile screen explicitly states that it does not collect personal information.
- The prototype continues to disclose that guidance is not a guarantee of admission, employment, placement or earnings.

## Not yet validated

The following require a real browser/device or human review and must not be marked complete based on the static checks above:

- Keyboard-only focus order, focus visibility and activation of radio/button controls.
- Screen-reader names, roles, progress announcements and expander behaviour.
- Text contrast, browser zoom and narrow mobile viewport behaviour.
- Whether the step wording, Back/Continue labels and help instructions are understood by low-digital-familiarity users.
- Marathi terminology and readability reviewed by a fluent human speaker.
- Whether optional read-aloud is needed, and which accessible implementation is appropriate.

No claim of WCAG conformance is made. Automated rendering-contract tests cannot establish screen-reader compatibility, colour contrast or user comprehension.

## Next validation protocol

1. Confirm the pilot language and participant approach with the mentor/sponsor; Maharashtra/Marathi remains an assumption.
2. Obtain a fluent Marathi reviewer for fixed UI and counselling copy.
3. With appropriate consent and safeguarding review, ask a small, non-identifying set of adult target users to: change language, move Home → Learner profile → Explore pathways, use Back, find Help, and explain the API-offline message.
4. Repeat with keyboard-only navigation, a screen reader, browser zoom and a narrow mobile viewport.
5. Record task-level observations without names, exact addresses, household income or unnecessary personal details. Treat a small sample as formative feedback, not representative research.
6. Decide whether read-aloud is needed before implementing it; text must remain available as an equivalent.

Issue tracking: [#14 — accessibility and usability review](https://github.com/emtharva1047/PathSaathi-AI/issues/14). The issue remains open until human and device-level validation is completed.
