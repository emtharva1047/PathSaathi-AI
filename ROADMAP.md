# PathSaathi AI — 60-Day Roadmap

**Mode:** Solo developer  
**Time budget:** Up to 4 focused hours per day (approximately 240 planned hours)  
**Priority:** Resume-quality portfolio product  
**Stack:** Python, Streamlit, FastAPI, SQLAlchemy, SQLite/PostgreSQL-ready, Pytest, Ruff, GitHub Actions

Day numbers are planning windows, not claims that work has already been completed. Update status only after evidence exists in the repository.

| Phase | Days | Objective | Exit evidence | Status |
|---|---:|---|---|---|
| 1. Research & requirements | 1–5 | Define users, scope, SRS, risks and data strategy | Reviewed SRS, use cases, scope and acceptance criteria | In progress |
| 2. Application foundation | 6–12 | Build app/API skeleton, config, DB and CI | App starts, API health check, DB smoke test, CI green | Not started |
| 3. Assessment & recommendations | 13–22 | Build assessment and explainable matching | Eligibility-safe recommendations with tests | Not started |
| 4. Course explorer & pathways | 23–29 | Curate sourced data and exploration UI | Search/filter/detail/compare workflow | Not started |
| 5. Family decision room | 30–36 | Link student-parent preferences and compare | Separate preferences and decision summary | Not started |
| 6. AI counsellor & reporting | 37–41 | Grounded Q&A and PDF report | Source-grounded responses and report export | Not started |
| 7. Quality, privacy & evaluation | 42–47 | Test, review security and improve usability | Test report, limitations, privacy review checklist | Not started |
| 8. Portfolio release | 48–60 | Deploy, document and demonstrate product | Live demo, CI, screenshots, final README and resume summary | Not started |

## Daily execution protocol

Each daily iteration should:
1. Inspect repository state, open issues, recent commits and CI.
2. Select the highest-priority incomplete task.
3. Deliver one cohesive, substantive increment.
4. Run relevant checks and record exact results.
5. Update documentation and this roadmap.
6. Commit only validated work.

A daily target of four hours is a planning allocation; automation runs do not prove four hours of continuous execution.

## Definition of done

The project is ready for portfolio release when the end-to-end flow works:

**profile → assessment → eligibility filter → ranked recommendations → source-linked course comparison → family decision room → report**

Required quality evidence:
- Tests for recommendation logic, eligibility and access control.
- Reproducible local setup.
- CI workflow for tests and lint.
- No secrets or real student personal data committed.
- Source provenance and verification dates for factual course records.
- Documented limitations and production-readiness gaps.
- Deployed demonstration and screenshots.

## Phase 1 progress
- [x] Initial project charter and scope drafted.
- [x] Initial SRS and user journeys drafted.
- [x] Initial architecture, risk register and data-source policy drafted.
- [x] Four actionable Phase 1 issues created.
- [ ] Full official SIH problem statement and sponsor constraints reviewed.
- [ ] Personas/scope validated against the brief.
- [ ] Data-source and eligibility assumptions reviewed.
- [ ] Phase 1 acceptance checklist signed off.

## Progress log

| Date | Phase / planned day | Increment | Checks | Commit |
|---|---|---|---|---|
| 2026-11-01 | Phase 1 / Day 1 | Initial requirements baseline and GitHub issue setup | Repository file read-back verified; app tests not applicable yet | Initial documentation commits |
| 2026-11-01 | Phase 1 / Day 1 | Added initial problem-framing research and clarified missing SIH brief dependency | GitHub file writes succeeded; complete SIH brief still outstanding | See commit history |
