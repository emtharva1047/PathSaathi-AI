# Phase 3 — Learner/Parent Context and Eligibility Domain

**Implementation slice:** Day 13, 14 November 2026  
**Status:** First domain increment; UI capture, persistence and counselling orchestration remain future Phase 3 work.

## Learner and parent context

The storage-independent records in \`core/profiles.py\` are immutable:

- \`LearnerProfile\` contains a pseudonymous reference, normalized education level,
  optional state/district reference codes, an optional configured income-band code,
  interests, work preferences and preferred language.
- \`ParentContext\` contains a separate participant reference, explicitly reported
  concern categories, priorities and preferred language.
- \`FamilyCounsellingContext\` composes the two records without merging or overwriting
  either participant's preferences. The references must be distinct.

The domain intentionally has no fields for names, phone numbers, email addresses,
exact addresses, dates of birth or exact household income. Region values are reference
codes rather than free-text addresses. The income-band code is only a configured
category identifier; the actual band taxonomy and labels remain unconfigured pending
pilot/mentor review. No exact income amount is accepted in that field.

Parent concerns are explicit self-reports. The model does not infer concerns or emotions
from conversation text. These records are not yet persisted or collected through the UI.

## Education normalization

\`EducationLevel\` is a set of normalized labels, not an ordered ranking. Equivalence
between school, ITI/vocational, diploma and other credentials must be mapped from the
specific qualification's published entry criteria. The application must not assume
that one label is automatically equivalent to another.

## Three-state eligibility

\`core/eligibility.py\` evaluates only a qualification's published education requirement:

| Status | Rule |
|---|---|
| \`eligible\` | The learner's recorded normalized education level appears in an accepted-level set from complete, verified criteria. |
| \`ineligible\` | Complete, verified criteria exist, but the recorded level is not in the accepted set. Equivalence must still be confirmed before excluding a pathway. |
| \`unknown\` | Criteria are missing, unverified or stale, or the learner's education level is unknown. |

A verified criteria record requires a qualification code, accepted education levels,
publisher, absolute HTTP(S) source URL and verification date. Results carry the
qualification code and source reference. They explicitly set \`admission_decision=False\`
and \`scope=education_requirement_only\`: other criteria and the provider's admission
decision may still apply.

No official qualification entry criteria have been added in this increment. The
\`example.org\` source in tests is a synthetic fixture only. Real criteria must be
transcribed from the exact NCVET/NQR qualification record and reviewed before use.

## Validation

- Profile tests cover participant separation, preference separation, optional fields,
  broad region codes, income-band-only storage and duplicate/blank preference handling.
- Eligibility tests cover eligible, ineligible and unknown states; missing, unverified
  and stale criteria; source requirements; and invalid source URLs.
- Local validation on 14 November 2026: \`python -m compileall -q core tests\` and
  \`pytest -q\` (16 passed). GitHub Actions validation is required before merge.

## Deliberate limitations

- No profile database tables, write API or UI capture in this increment.
- No age, subject, disability, income threshold or other entry rule is inferred.
- No aptitude/psychometric score or prediction of success is produced.
- The SIH dummy outcome dataset and mentor-confirmed pilot settings remain external
  dependencies tracked in issues #5 and #6.

## Next Phase 3 work

Add guided bilingual profile capture with explicit learner/parent roles, then build
transparent advisory pathway shortlisting. Keep eligibility tied to exact verified
qualification sources and retain an unrestricted option to explore other pathways.
