# SIH26241 Requirements-to-Product Traceability

**Source:** Official SIH problem-statement listing, https://www.sih.gov.in/sih2026PS  
**Problem ID:** SIH26241  
**Review date:** 1 November 2026

| SIH requirement | PathSaathi AI response | Evidence / acceptance test | MVP priority |
|---|---|---|---|
| Joint learner-parent counselling | Shared family conversation with distinct learner/parent roles and separately stored preferences | Both roles can ask questions and see the same sourced response; preference records remain separate | Must |
| Regional language + English | English + Marathi pilot; locale-aware content and reviewed translations | Main onboarding, assessment and counselling journey available in both languages | Must |
| Address income, job security and social perception concerns | Concern taxonomy and evidence cards for outcomes, safety information where sourced, recognition and progression | Each factual response links to evidence or says evidence is unavailable | Must |
| Verified trade/provider earnings and placement outcomes | OutcomeEvidence data model with definitions, cohort, geography, provider/trade scope, sample/denominator and source | Metric semantics and provenance tests; no provider-level claim from state-level source | Must |
| NSQF and further education progression | Qualification and pathway graph based on NQR/official qualification files | Pathway nodes link to source and qualification level | Must |
| Low-jargon, context-tailored explanation | Plain-language mode; optional broad location, income band and education context | Usability checklist; no exact income or address required | Must |
| Human counsellor escalation | Escalation request and status workflow | Request can be created, reviewed and marked; demo is not represented as live service | Must |
| Admin engagement and sentiment-shift dashboard | Aggregate event counts, optional concern categories and self-reported confidence before/after | Aggregation suppresses small groups; no covert emotion inference | Must |
| Low-literacy / low-digital familiarity | Guided one-question-at-a-time flow, large controls, labels/icons, simple summaries | Mobile usability review; optional audio read-out is stretch | Must |
| Localised credible data | Maharashtra pilot scope, with data records scoped to source geography and cohort | UI labels geographic mismatch and stale evidence | Must |
| Live provider integration / nationwide coverage | Deferred until authorised APIs/data access exist | Document integration boundary and data gaps | Stretch |

## Data note from official SIH listing

The official SIH listing displays no public dataset link for SIH26241 and states that dummy placement/earnings datasets will be provided for hackathon evaluation. The implementation must support an importer for the official evaluation files once supplied. Until then, use synthetic fixtures only and label them clearly.

## Release rule

A feature is not considered complete merely because a screen exists. Each must have a working flow, appropriate data, validation and a test or documented manual acceptance check.
