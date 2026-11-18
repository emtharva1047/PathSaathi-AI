# Phase 3 — Source-backed Qualification and NSQF Explainers

**Implementation slice:** Day 16, 17 November 2026  
**Status:** One curated NQR qualification example is rendered in English and draft Marathi. The source-gated contract and half-step NSQF storage/API support are implemented; human Marathi review and broader catalogue ingestion remain open.

## Official source model

The National Qualifications Register is NCVET's public record of NSQF-aligned qualifications. Its qualification files provide structured information including qualification details, entry requirements, learning modules, progression and other approval material.

The prototype includes one current NQR example:

| Field | Recorded value |
|---|---|
| NQR record | 12209 |
| Qualification | Assistant Baking Technician |
| Qualification code/version | QG-03-FI-02932-2024-V2-FICSI, V4.0 |
| Sector | Food Processing |
| Awarding body | Food Industry Capacity and Skill Initiative (FICSI) |
| NSQF level | 3 |
| Validity shown by NQR | Through 26 August 2027 |
| Source file approval | 39th NSQC, 27 August 2024 |
| Last checked | 17 November 2026 |

Sources:
- [NQR qualification record](https://www.nqr.gov.in/qualifications/12209)
- [Qualification File PDF](https://www.nqr.gov.in/qualification/file/English%20Q-file%20Baking%20Tech..pdf)
- [NQR overview](https://nqr.gov.in/aboutus)
- [Qualification File structure](https://nqr.gov.in/qualificationfile)

## Explainer content

The exact qualification file and linked NQR page support the following claims:

- Job description: baking products, maintaining consistency and quality, following standard operating procedures and operating ovens in coordination with the production unit.
- Four alternative entry routes: Grade 10 with no experience; Grade 8 with three years of relevant Food Industry experience; a relevant NSQF Level 2.5 qualification with 1.5 years of relevant experience; or a relevant NSQF Level 2 qualification with three years of relevant experience.
- Minimum age: 16 years.
- Total notional training duration: 300 hours.
- Learning modules: prepare for production (60 hours), bake products in the oven (120 hours), food-safety guidelines in food processing (30 hours), employability skills (30 hours) and on-the-job training (60 hours).
- Published progression: Baking Technician to Plant Biscuit Production Specialist; the NQR page lists the latter at NSQF Level 4.

The interface links each displayed fact to its exact source URL and section/page reference. It displays the record validity and the last verification date.

## Claim-level gating

The pure domain contract is in core/qualification_explainers.py:

- Each fact has a stable identifier, kind, English and Marathi text, publisher, source URL, source section/page and last verification date.
- A verified fact must have complete provenance.
- The parent qualification record has a separate NQR state: current, expired, archived or unknown.
- A record past its valid-until date is treated as expired.
- Claims from expired, archived or unknown records are withheld.
- Unverified, stale or future-dated claims are withheld individually. A partial explainer shows only the verified remainder.
- The UI never substitutes a missing NSQF level, job role, entry rule or progression route.

No LLM is used to create these facts. The current rendering is deterministic.

## Eligibility and local availability limitations

This qualification has several alternative education/experience routes and a minimum-age condition. The multi-route evaluator now models all four published routes as OR alternatives with AND conditions. The current Streamlit profile wizard does not collect age, prior qualifications or experience, so the example remains unknown until those facts are deliberately supplied and verified. The older education-only evaluator remains separate and is not used to collapse the routes into a single Grade 10 check.

The NQR record is national. It does not confirm a local Maharashtra training centre, seats, fees, course delivery in a learner's district, or provider admission. The explainer includes no placement, salary, safety or job-security statistics.

The Marathi strings are draft translations. They are labelled as unreviewed until a fluent human reviewer checks terminology and comprehension. The English source file remains authoritative.

## NSQF precision

NQR records may use half-step levels, for example Level 2.5. CourseRecord now stores NSQF levels as Decimal values in 0.5 increments between 1 and 10. SQLAlchemy uses NUMERIC(3,1), repository filters use Decimal bounds, and the API serializes the level as a JSON number. Unknown values remain null.

## Multi-route eligibility

See [PHASE3_MULTI_ROUTE_ELIGIBILITY.md](PHASE3_MULTI_ROUTE_ELIGIBILITY.md) for the OR/AND route model, learner evidence contract, privacy constraints, bilingual result explanations and test coverage. Eligibility remains advisory, not an admission decision. Human Marathi review is still required.


## Validation evidence

PR [#36](https://github.com/emtharva1047/PathSaathi-AI/pull/36) was merged to main as
[8f681248](https://github.com/emtharva1047/PathSaathi-AI/commit/8f681248bf21ceb239b862b484d70e22cec6f970).
The final PR run [#165](https://github.com/emtharva1047/PathSaathi-AI/actions/runs/44013837400)
and merged-main run
[#166](https://github.com/emtharva1047/PathSaathi-AI/actions/runs/44013967127)
both passed Python compilation, Ruff, 176 Pytest tests and the live Streamlit/FastAPI
offline/online/offline smoke check. Each run recorded one existing Starlette/httpx
deprecation warning.
