"""Contract tests for the documented SIH26241 project requirements.

These tests validate the Phase 1 requirements baseline. They do not claim that
application functionality has been implemented yet.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_doc(relative_path: str) -> str:
    """Read a UTF-8 project document from the repository root."""
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_eligibility_is_a_hard_gate() -> None:
    srs = read_doc("docs/SRS.md").lower()
    assert "eligible, ineligible or unknown" in srs
    assert "eligibility is a hard filter" in srs


def test_sih_language_and_human_escalation_requirements_are_documented() -> None:
    srs = read_doc("docs/SRS.md").lower()
    assert "english and marathi" in srs
    assert "human-counsellor escalation request" in srs


def test_outcome_evidence_requires_provenance_and_scope() -> None:
    model = read_doc("docs/OUTCOME_DATA_MODEL.md").lower()
    for required_field in (
        "definition",
        "numerator",
        "denominator",
        "sample_size",
        "geography_level",
        "cohort_period",
        "source_url",
        "publication_date",
        "methodology",
    ):
        assert required_field in model


def test_provider_level_outcomes_are_not_extrapolated() -> None:
    policy = read_doc("docs/DATA_SOURCE_POLICY.md").lower()
    model = read_doc("docs/OUTCOME_DATA_MODEL.md").lower()
    assert "do not derive provider-level outcomes from state-level" in policy
    assert "provider-level evidence requires a provider-specific source sample" in model


def test_official_problem_statement_is_mapped() -> None:
    mapping = read_doc("docs/PROBLEM_STATEMENT_MAPPING.md").lower()
    for requirement in (
        "joint learner-parent counselling",
        "regional language + english",
        "human counsellor escalation",
        "admin engagement and sentiment-shift dashboard",
        "low-literacy",
    ):
        assert requirement in mapping
