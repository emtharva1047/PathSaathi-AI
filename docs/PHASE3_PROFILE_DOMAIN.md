# Phase 3 — Learner/Parent Context and Eligibility Domain

**Implementation slices:** Days 13–14, 14–15 November 2026  
**Status:** Separate learner/parent domain records and verified-criteria eligibility are implemented; guided bilingual profile capture is session-only. Durable storage and counselling orchestration remain future work.

## Learner and parent context

The storage-independent records in `core/profiles.py` are immutable:

- `LearnerProfile` contains a pseudonymous reference, normalized education level,
  optional state/district reference codes, an optional income-band code (taxonomy pending mentor/pilot review),
  interests, work preferences and preferred language.
- `ParentContext` contains a separate participant reference, explicitly reported
  concern categories, priorities and preferred language.
- `FamilyCounsellingContext` composes the two records without merging or overwriting
  either participant's preferences. The references must be distinct.

The domain intentionally has no fields for names, phone numbers, email addresses,
exact addresses, dates of birth or exact household income. Region values are reference
codes rather than free-text addresses. The income-band code is only a configured
category identifier; the actual band taxonomy and labels remain unconfigured pending
pilot/mentor review. No exact income amount is accepted in that field.

Parent concerns are explicit self-reports. The model does not infer concerns or emotions
from conversation text. The guided UI now collects the corresponding choices into session-local context only; no profile write API or database persistence is used.

## Guided bilingual capture

`app/profile_flow.py` renders seven short steps, one main question at a time:

1. Learner's highest completed education level (unknown is the default).
2. Optional broad state code. Maharashtra (`MH`) is labelled as a provisional pilot assumption, not a confirmed deployment region.
3. Learner interests.
4. Learner work preferences.
5. Parent/guardian's explicitly reported concern categories.
6. Parent/guardian priorities.
7. A review that shows learner and parent perspectives separately.

The Back/Continue controls and question-level progress indicator are local to this flow. English and Marathi labels/help text are maintained together and tested for matching keys. The existing page-level Help remains available.

The flow stores only a `FamilyCounsellingContext` draft in Streamlit session state when the user chooses to keep it. It is not submitted to FastAPI or written to SQLite. The draft may disappear when the session ends. No names, phone numbers, email addresses, exact income or exact address are requested. District-level and household-income-band inputs remain disabled until their pilot taxonomies are approved; missing values remain unset.

The review explicitly describes the feature as a conversation aid, not an aptitude/psychometric test or prediction of success. Parent concerns are self-reported; no emotion inference is performed.

## Education normalization

`EducationLevel` is a set of normalized labels, not an ordered ranking. Equivalence
between school, ITI/vocational, diploma and other credentials must be mapped from the
specific qualification's published entry criteria. The application must not assume
that one label is automatically equivalent to another.

## Three-state eligibility

`core/eligibility.py` evaluates only a qualification's published education requirement:

| Status | Rule |
|---|---|
| `eligible` | The learner's recorded normalized education level appears in an accepted-level set from complete, verified criteria. |
| `ineligible` | Complete, verified criteria exist, but the recorded level is not in the accepted set. Equivalence must still be confirmed before excluding a pathway. |
| `unknown` | Criteria are missing, unverified or stale, or the learner's education level is unknown. |

A verified criteria record requires a qualification code, accepted education levels,
publisher, absolute HTTP(S) source URL and verification date. Results carry the
qualification code and source reference. They explicitly set `admission_decision=False`
and `scope=education_requirement_only`: other criteria and the provider's admission
decision may still apply.

No official qualification entry criteria have been added in this increment. The
`example.org` source in tests is a synthetic fixture only. Real criteria must be
transcribed from the exact NCVET/NQR qualification record and reviewed before use.

## Validation

- Profile tests cover participant separation, preference separation, optional fields,
  broad region codes, income-band-only storage and duplicate/blank preference handling.
- Eligibility tests cover eligible, ineligible and unknown states; missing, unverified
  and stale criteria; source requirements; and invalid source URLs.
- The original domain increment passed its 16 focused local tests and GitHub Actions run #144.
- The guided-flow increment adds bilingual UI/domain tests for one-question rendering, navigation, role separation, unknown values and session-only save. PR #32 was merged as `b2c9ee6`; GitHub Actions run #148 passed compileall, Ruff, 138 Pytest tests and the live Streamlit/FastAPI process smoke check (one existing Starlette/httpx deprecation warning).

## Deliberate limitations

- No profile database tables or write API are introduced; the current draft is session-only.
- No household-income band is requested until an approved band taxonomy exists.
- No age, subject, disability, income threshold or other entry rule is inferred.
- No aptitude/psychometric score or prediction of success is produced.
- The SIH dummy outcome dataset and mentor-confirmed pilot settings remain external
  dependencies tracked in issues #5 and #6.

## Next Phase 3 work

Build transparent advisory pathway shortlisting with reasons tied to the learner's
stated interests and work preferences, while preserving an unrestricted option to
explore other pathways. Do not rank learners or claim validated psychometrics.


## Transparent advisory pathway shortlisting

The pathway matcher is implemented in core/pathways.py and rendered through
app/pathway_flow.py. It consumes only the learner's explicit interest and work-preference
tags. Parent concerns, parent priorities, education level, broad region and income are
not used to rank or filter preference matches.

Each result retains:
- Exact matched interest and work-preference tags.
- Stable reason codes such as interest:technology and work_preference:hands_on.
- English and Marathi explanations of the matched signals.
- A separate eligible, ineligible or unknown education-criterion result.
- An unrestricted list of all catalogue options, including those not shortlisted.

The ordering is a deterministic presentation of exact catalogue-tag overlaps, with
stable course-identifier tie-breaking. It is not a learner score, aptitude test,
psychometric assessment or prediction of success. An ineligible or unknown education
result does not silently remove an option from exploration.

The current Streamlit screen uses four clearly labelled synthetic demonstration themes.
They are not official course listings, NCVET/NQR records, NSQF mappings, provider offers,
fees or outcome evidence. No placement, earnings, safety or job-security values are
generated. All demo eligibility remains unknown because no official criteria are loaded.

When official catalogue records are introduced, each option must retain its course-source
status. Entry criteria are evaluated only when attached to the same source-verified
qualification code; missing or unverified criteria remain unknown. Human review of
Marathi terminology and actual course mappings remains outstanding.
