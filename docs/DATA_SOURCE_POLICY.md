# Data Source and Provenance Policy

## Preferred source hierarchy
1. Official government qualification and vocational education registries.
2. Official training provider, ITI, polytechnic and institution course pages.
3. Official examination/admission notices and qualification documents.
4. Reputable secondary sources for context, clearly labelled as secondary.

Potential starting points (verify current availability and applicability before importing):
- NCVET: https://ncvet.gov.in/
- National Qualification Register: https://www.nqr.gov.in/
- Skill India Digital Hub: https://www.skillindiadigital.gov.in/

## Required record metadata
record_id; title and provider; qualification level/framework if verified; eligibility description and source; duration and source; fees only when publicly verified with date and scope; source_url; source_publisher; last_verified_at (ISO date); confidence/status (verified, needs_review, stale, unknown); interpretation notes.

## Rules
- Do not scrape or republish content contrary to terms or licence.
- Do not infer official recognition from provider marketing.
- Do not invent fees, salary, employment, placement or admission claims.
- Store null/unknown where a field cannot be verified.
- Record date checked and re-check before release.
- Treat job outcomes as variable; avoid guaranteed or individual salary predictions.
- Use synthetic demo data and label illustrative records as synthetic.
