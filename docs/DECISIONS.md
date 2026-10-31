# Architecture Decision Records

## ADR-001: Python-first modular application
**Status:** Accepted for MVP

**Decision:** Use Streamlit for UI and FastAPI for backend API. Keep domain logic in reusable Python services.

**Rationale:** Rapid UI development without coupling core eligibility/recommendation logic to UI widgets; independently testable API and services.

**Trade-offs:** Two application processes and API integration work. Worthwhile for a portfolio demonstrating API design and modularity.

## ADR-002: Eligibility is a hard filter
**Status:** Accepted

**Decision:** Model eligibility as eligible, ineligible or unknown. Preference scores cannot compensate for unmet required eligibility.

**Rationale:** A high preference match must not imply admission eligibility.

## ADR-003: Deterministic recommendations before LLM
**Status:** Accepted

**Decision:** Recommendation ranking is computed by deterministic, testable code. LLM use is limited to grounded explanation and counselling.

**Rationale:** Reproducibility, explainability, reduced hallucination risk and easier evaluation.
