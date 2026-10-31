# Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Course facts become stale | High | High | Store source and verification date; flag stale records |
| Incorrect eligibility rules | Medium | High | Cite official source; unknown state; boundary tests; counsellor review |
| Scores appear scientifically validated | Medium | High | Label prototype weights; show factors; avoid psychometric claims |
| LLM invents facts | High | High | Retrieval grounding, source display, unknown responses |
| Student/parent conflict | Medium | Medium | Keep preferences separate; show trade-offs; preserve student agency |
| Sensitive data exposure | Medium | High | Minimise fields, role checks, hashing, synthetic tests, deletion |
| Under-18 consent requirements missed | Medium | High | Age-aware design and legal/privacy review before production |
| Scope exceeds 60 days | High | Medium | Protect end-to-end workflow; defer custom ML/mobile/live scraping |
| LLM outage/cost | Medium | Medium | Deterministic core works without LLM; configurable provider/limits |
| Deployment differences | Medium | Medium | Environment config, pinned dependencies, CI and smoke tests |
