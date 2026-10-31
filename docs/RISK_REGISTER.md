# Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Course facts become stale | High | High | Store source and verification date; flag stale records |
| Incorrect eligibility rules | Medium | High | Cite official qualification file; unknown state; boundary tests; counsellor review |
| Outcome metric is mislabelled | High | High | Preserve exact definition, denominator and cohort; distinguish placement from employment |
| Provider-level outcome data is unavailable | High | High | Show unavailable; never infer from state/trade aggregates; seek authorised data |
| Historical/small-sample data is overgeneralised | High | High | Display cohort, sample, geography and publication date; warn on small samples |
| SIH evaluation dataset is not yet received | Medium | High | Build validated importer; use synthetic fixtures only until authorised dataset arrives |
| Matching scores appear scientifically validated | Medium | High | Label prototype weights; show factors; avoid psychometric claims |
| AI invents outcome or safety facts | High | High | Retrieval grounding, source display, unknown responses, deterministic evidence cards |
| Regional-language translation is inaccurate | Medium | High | Human-review key Marathi strings; version translations; allow English fallback |
| Low-literacy users struggle with UI | Medium | Medium | Guided steps, plain language, large controls, mobile usability review |
| Escalation implies a live counsellor service that does not exist | Medium | High | Clearly label prototype queue; do not promise response times without a partner |
| Student/parent conflict | Medium | Medium | Keep preferences separate; show trade-offs; preserve learner agency |
| Family data is exposed to an unauthorised user | Medium | High | Minimise fields, role checks, password hashing, synthetic tests, deletion and consent |
| Feedback analytics become intrusive | Medium | High | Use optional self-report; no covert emotion inference; aggregate and suppress small groups |
| Consent requirements for minors are missed | Medium | High | Age-aware design and legal/privacy review before production |
| Scope exceeds 60 days | High | Medium | Protect end-to-end workflow; defer custom ML, live integrations and nationwide feeds |
| AI provider outage or cost | Medium | Medium | Deterministic core works without LLM; configurable provider and usage limits |
| Deployment differs from local setup | Medium | Medium | Environment config, pinned dependencies, CI and smoke tests |
