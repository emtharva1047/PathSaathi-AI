"""Contract tests for the SIH26241 requirements baseline.

These checks validate project documentation and data contracts. They do not
claim that application features have been implemented.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_doc(relative_path: str) -> str:
    """Read a UTF-8 project document from the repository root."""
    return (ROOT / relative_path).read_text(encoding="utf-8").lower()


def test_problem_statement_requires_joint_family_counselling() -> None:
    srs = read_doc("docs/SRS.md")
    assert "joint learner-parent conversational counselling" in srs
    assert "learner and parent/guardian in the same counselling journey" in srs


def test_bilingual_and_accessibility_requirements_are_documented() -> None:
    srs = read_doc("docs/SRS.md")
    accessibility = read_doc("docs/LOCALIZATION_AND_ACCESSIBILITY.md")
    assert "english and at least one regional language" in srs
    assert "marathi" in accessibility
    assert "large buttons and touch targets" in accessibility


def test_human_escalation_has_truthful_request_workflow() -> None:
    srs = read_doc("docs/SRS.md")
    escalation = read_doc("docs/ADMIN_ANALYTICS_AND_ESCALATION.md")
    assert "human counsellor" in srs
    assert "request reference and status" in srs
    assert "callback/follow-up request" in escalation


def test_outcome_contract_preserves_denominators_and_provenance() -> None:
    contract = read_doc("docs/OUTCOME_DATA_CONTRACT.md")
    for required_field in (
        "placement_denominator",
        "placed_count",
        "earnings_currency",
        "earnings_period",
        "source_reference",
        "last_verified_at",
    ):
        assert required_field in contract


def test_synthetic_outcomes_are_never_presented_as_real() -> None:
    contract = read_doc("docs/OUTCOME_DATA_CONTRACT.md")
    policy = read_doc("docs/DATA_SOURCE_POLICY.md")
    assert "data_quality_status=synthetic" in contract
    assert "do not report synthetic figures as indian labour-market facts" in policy


def test_admin_analytics_are_aggregate_and_privacy_aware() -> None:
    analytics = read_doc("docs/ADMIN_ANALYTICS_AND_ESCALATION.md")
    assert "aggregate data only" in analytics
    assert "suppress cohorts below a configurable minimum group size" in analytics
    assert "do not covertly infer emotion" in analytics


def test_official_sih_requirements_are_mapped() -> None:
    mapping = read_doc("docs/PROBLEM_STATEMENT_MAPPING.md")
    for requirement in (
        "joint learner-parent counselling",
        "regional language + english",
        "human counsellor escalation",
        "admin engagement and sentiment-shift dashboard",
        "low-literacy",
    ):
        assert requirement in mapping


def test_pathway_shortlisting_is_advisory_and_eligibility_safe() -> None:
    srs = read_doc("docs/SRS.md")
    assert "eligible, ineligible and unknown eligibility" in srs
    assert "not a validated aptitude test" in srs
