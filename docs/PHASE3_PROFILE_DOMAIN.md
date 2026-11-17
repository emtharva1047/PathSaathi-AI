# Phase 3 — Learner/Parent Context and Eligibility Domain

**Implementation slices:** Days 13–15, 14–16 November 2026  
**Status:** Separate learner/parent domain records, verified-criteria eligibility, guided bilingual profile capture and deterministic advisory shortlisting are implemented. Profile drafts remain session-only; durable storage and counselling orchestration remain future work.

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

Extend qualification eligibility to represent all published alternative routes, including
academic education, prior NSQF qualification, relevant experience and minimum age. Do not
collapse multiple alternatives into one education-only test. Until the full rule model is
implemented, the Assistant Baking Technician example is explainer-only and its eligibility
remains unassessed.



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


## Validation evidence for advisory shortlisting

PR #34 was merged to main as commit ea0a145. Its GitHub Actions PR run #154 and merged-main run #155 both passed:
- Python package compilation.
- Ruff lint.
- 159 Pytest tests.
- Live Streamlit/FastAPI process smoke test.

Each run reported one existing Starlette/httpx deprecation warning. The 21 added tests cover the deterministic matcher, stable ties, incomplete/no-match exploration, exact reason codes, English/Marathi copy, parent-context separation, synthetic-data labels, source-code matching and separate eligibility states.

The current four-option Streamlit catalogue is explicitly synthetic. It is a UI demonstration only and must be replaced by validated source-linked catalogue records during the course/outcome explorer phase. It contains no official qualification, NSQF, fee, placement, earnings, safety or job-security facts. Human Marathi review and target-user accessibility testing remain open in issue #14.


### Eligibility gate and presentation

Preference overlap is not eligibility. Only an option whose attached education criterion is
verified and met may enter the eligible shortlist. Preference matches with unknown eligibility
appear in a separate verification group and are explicitly not eligible recommendations.
Options with an ineligible result remain in the full exploration list, labelled ineligible;
preference matching cannot promote them into the shortlist. All options remain visible.


Eligibility-gate follow-up PR #35 was validated by GitHub Actions run #157:
compileall, Ruff, 159 Pytest tests and the live Streamlit/FastAPI smoke test passed
(one existing Starlette/httpx deprecation warning). The regression suite confirms
that unknown matches are separated for verification and ineligible matches cannot
enter the eligible shortlist.


## Source-backed NQR qualification explainer — 17 November 2026

The bilingual Streamlit pathway page now renders one curated national NQR record:
Assistant Baking Technician (NQR record 12209; qualification code
QG-03-FI-02932-2024-V2-FICSI, V4.0). The NQR record lists NSQF Level 3 and validity through
26 August 2027. Its qualification file supplies the job description, four alternative
entry routes, minimum age 16, learning-module names/hours, total notional duration of
300 hours and the progression route to Baking Technician and Plant Biscuit Production
Specialist. The NQR page lists the latter at NSQF Level 4.

The typed contract in core/qualification_explainers.py separates record state from
claim-level provenance. The renderer shows claims only when the qualification record
is current and its source is verified, and each claim has its own publisher, URL,
source section and verification date. The NQR record's own publisher, URL and verification date are also required before its current status or validity can be used. Expired, archived, unknown, future-dated or
unverified claims are withheld. A partially sourced record shows only its verified
claims and counts the withheld remainder.

The curated source data lives in
data/qualifications/assistant_baking_technician.json and is loaded through
services/qualification_catalogue.py. The Marathi strings are draft translations,
explicitly labelled as awaiting fluent human review. The record is national, not a
local provider listing; no seats, fees, local availability, eligibility decision,
salary or placement outcomes are inferred.

The qualification includes alternative education and experience routes plus a
minimum-age condition. The current eligibility evaluator supports only a verified
education-level criterion, so this record is deliberately not attached to that
evaluator. A separate multi-condition eligibility model is still required.

### Fractional NSQF levels

NQR qualification records can refer to half-step levels such as 2.5. CourseRecord now
stores NSQF levels as Decimal values in 0.5 increments from 1 through 10.
SQLite/PostgreSQL-ready persistence uses NUMERIC(3,1), and API filters accept exact
half-step bounds. This avoids truncating or rejecting legitimate half-level values.
