# Course catalogue explorer

The bilingual Streamlit course explorer reads only from the existing FastAPI
`GET /api/v1/courses` endpoint. It is a read-only discovery
surface; it does not seed, import, approve, update or persist catalogue records.

## Filters and query contract

The UI sends exact-match filters for:

- `state`
- `district`
- `trade`
- `provider_id`
- `min_nsqf_level`
- `max_nsqf_level`

NSQF levels are parsed through the shared domain normalizer and preserve exact
whole/half-step semantics from 1 to 10. A minimum above the maximum, an
out-of-range level, or a non-half-step decimal is rejected before a network
request. API pagination uses a fixed page size of 50 (within the API's 1–100
bound) and its stable `course_id` ordering.

The client uses the configured `PATHSAATHI_API_URL` base URL,
accepts only absolute HTTP(S) URLs without credentials/query/fragment, and
uses a short timeout. Offline, invalid-filter, malformed-response and empty
catalogue states are explicit. There is no local, curated or synthetic
fallback. The source-backed Assistant Baking Technician explainer remains a
separate curated NQR example and is not inserted into this API catalogue.

## Record display and provenance

Only API-returned fields are displayed: title, trade, qualification code,
awarding body, NSQF level, job roles, entry requirements, state, district,
provider ID, source publisher, source URL, publication date, last verification
date and verification status. Missing values and empty lists are labelled
unknown, not interpreted as zero or as an absent requirement.

A record is labelled as verified source metadata only when the API reports
`verification_status=verified` and `source_verified=true`
and the client independently confirms that publisher, verification date and a
credential-free HTTP(S) source URL are present. This is the current review
workflow label, not an independent PathSaathi audit. Needs-review, stale,
synthetic-demo and incomplete verified records remain visibly distinct.

Only HTTP(S) source URLs with a hostname and no embedded credentials are
rendered as clickable links. An unsafe supplied URL is shown as text with a
warning and is never opened.

## Decision-support boundary

A course/qualification catalogue entry does not establish current local
provider operation, admission availability, seats, fees, eligibility for a
specific applicant, placement, earnings, job security or workplace safety.
The UI does not infer any of these facts. Learners and families must confirm
delivery and admission details with the relevant awarding body or provider.

The catalogue is independent of the SIH dummy placement/earnings dataset
tracked in [issue #5](https://github.com/emtharva1047/PathSaathi-AI/issues/5).
Synthetic fixtures are test-only; no synthetic course or outcome record is
substituted when the API is empty or offline.

## Validation

```bash
pytest -q tests/test_course_explorer.py
ruff check app/course_explorer.py tests/test_course_explorer.py app/streamlit_app.py
```

Tests cover exact query construction, half-step and range validation,
pagination bounds, API-offline and invalid-URL behaviour, empty responses,
bilingual states, required source fields, verification labels and safe source
links. Real-user accessibility, Marathi language review and mobile/device
validation remain tracked separately in issue #14.
