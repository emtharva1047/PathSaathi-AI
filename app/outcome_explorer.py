"""Bilingual, read-only outcome evidence explorer for Streamlit."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"
API_TIMEOUT_SECONDS = 3.0
PAGE_SIZE = 50
GEOGRAPHY_LEVELS = ("national", "state", "district", "provider")
VERIFICATION_STATUSES = ("verified", "needs_review", "stale", "synthetic_demo")


class OutcomeApiError(RuntimeError):
    """Safe, user-displayable error raised while reading outcome evidence."""

    def __init__(self, message: str, *, kind: str = "api") -> None:
        super().__init__(message)
        self.kind = kind


@dataclass(frozen=True, slots=True)
class ComparisonAssessment:
    """Compatibility decision; period differences are disclosed, never pooled."""

    compatible: bool
    mismatches: tuple[str, ...]
    period_differences: tuple[str, ...]


OUTCOME_EXPLORER_COPY: dict[str, dict[str, str]] = {
    "English": {
        "heading": "Explore outcome evidence",
        "description": (
            "Search the read-only evidence catalogue. Filters are exact matches; a broader "
            "result is never substituted for the scope you requested."
        ),
        "warning": (
            "Historical group evidence is not a promise of admission, placement, employment, "
            "earnings, job security or safety. The current SIH dummy dataset has not been supplied."
        ),
        "metric_code": "Metric code",
        "geography_level": "Geography level",
        "any_geography": "Any level",
        "geography_name": "Geography name",
        "trade": "Trade / job role",
        "provider": "Provider ID (provider-level evidence only)",
        "cohort": "Cohort period",
        "observation": "Observation period",
        "verification": "Evidence status",
        "any_status": "Any status",
        "apply": "Apply filters",
        "filters_heading": "Evidence filters",
        "unknown": "Not supplied — unknown",
        "offline": "Outcome API is offline or unreachable. No local or synthetic outcomes are substituted.",
        "api_error": "The outcome API could not complete this request: {detail}",
        "empty": (
            "No records match these exact filters in the currently available catalogue. "
            "This does not establish that no outcomes exist elsewhere."
        ),
        "page": "Page offset: {offset} · {count} records returned (maximum {limit} per request).",
        "evidence": "Evidence record",
        "metric": "Metric",
        "definition": "Metric definition",
        "value": "Published numeric value",
        "withheld": "A numeric value exists in storage but is withheld because verified provenance is incomplete.",
        "unknown_value": "No numeric outcome value is available. Unknown is not zero.",
        "status": "Verification status",
        "status_verified": "Verified in the current data-review workflow (not an independent audit claim)",
        "status_needs_review": "Needs review — not verified",
        "status_stale": "Stale — not current evidence",
        "status_synthetic_demo": "Synthetic demo — not a real outcome",
        "geography": "Geography",
        "trade_role": "Trade / job role",
        "provider_id": "Provider ID",
        "state": "State",
        "district": "District",
        "cohort_label": "Cohort period",
        "observation_label": "Observation period",
        "follow_up": "Follow-up period",
        "counts": "Numerator / denominator",
        "sample_size": "Sample size",
        "earnings_semantics": "Currency / unit / statistic",
        "source_publisher": "Source publisher",
        "source_url": "Source URL",
        "source_publication": "Source publication date",
        "source_reference": "Source page / table",
        "methodology": "Methodology and caveats",
        "last_verified": "Last verified date",
        "open_source": "Open source",
        "numeric_metadata_withheld": "Numeric counts and sample size are withheld until source verification is complete.",
        "provenance_caveat": (
            "A verified status records the current review label and provenance fields; it does "
            "not mean PathSaathi independently audited the source."
        ),
        "compare_heading": "Compare two observations",
        "compare_help": "Select exactly two records from this page. Comparisons are side-by-side only.",
        "select_two": "Select exactly two evidence records to compare.",
        "compatible": "These observations meet the current comparison compatibility rules.",
        "incompatible": "These observations are not comparable under the current rules: {reasons}",
        "period_differences": "Disclose these scope differences; no pooling or adjustment is performed:",
        "no_period_differences": "Cohort, observation and follow-up periods match.",
        "comparison_values": "Verified values side by side",
        "comparison_numeric_blocked": "Metadata can be compared, but at least one numeric value is unknown or withheld.",
        "mismatch_metric": "metric code or definition",
        "mismatch_kind": "metric kind",
        "mismatch_unit": "currency, unit or statistic semantics",
        "mismatch_geography": "geography granularity",
        "mismatch_trade": "trade / job role",
        "mismatch_provider": "provider identity is missing for provider-level evidence",
        "previous": "Previous page",
        "next": "Next page",
    },
    "मराठी": {
        "heading": "रोजगारविषयक पुरावे पाहा",
        "description": (
            "फक्त-वाचन पुरावा सूची शोधा. फिल्टर अचूक जुळणी वापरतात; मागितलेल्या स्तराऐवजी "
            "मोठ्या क्षेत्राचा निकाल दाखवला जात नाही."
        ),
        "warning": (
            "गटांचा ऐतिहासिक पुरावा प्रवेश, प्लेसमेंट, नोकरी, उत्पन्न, नोकरीची सुरक्षितता "
            "किंवा कामाच्या सुरक्षिततेची हमी देत नाही. SIH नमुना डेटासेट अद्याप मिळालेला नाही."
        ),
        "metric_code": "मोजमाप संकेतांक",
        "geography_level": "भौगोलिक स्तर",
        "any_geography": "कोणताही स्तर",
        "geography_name": "भौगोलिक नाव",
        "trade": "व्यवसाय / कामाची भूमिका",
        "provider": "प्रशिक्षण संस्था संकेतांक (फक्त संस्था-स्तरीय पुरावा)",
        "cohort": "प्रशिक्षण गटाचा कालावधी",
        "observation": "निरीक्षण कालावधी",
        "verification": "पुराव्याची स्थिती",
        "any_status": "कोणतीही स्थिती",
        "apply": "फिल्टर लागू करा",
        "filters_heading": "पुरावा फिल्टर",
        "unknown": "दिलेली नाही — अज्ञात",
        "offline": "रोजगार पुरावा API उपलब्ध नाही. त्याऐवजी स्थानिक किंवा कृत्रिम आकडे दाखवले जाणार नाहीत.",
        "api_error": "रोजगार पुरावा API विनंती पूर्ण करू शकली नाही: {detail}",
        "empty": (
            "सध्या उपलब्ध सूचीमध्ये या अचूक फिल्टरशी जुळणारी नोंद नाही. "
            "याचा अर्थ इतरत्र पुरावा नाही असा होत नाही."
        ),
        "page": "पानाचा प्रारंभ: {offset} · मिळालेल्या नोंदी: {count} (प्रति विनंती कमाल {limit}).",
        "evidence": "पुरावा नोंद",
        "metric": "मोजमाप",
        "definition": "मोजमापाची व्याख्या",
        "value": "प्रकाशित संख्यात्मक मूल्य",
        "withheld": "मूल्य साठवलेले आहे; पूर्ण पडताळलेला स्रोत नसल्यामुळे ते दाखवलेले नाही.",
        "unknown_value": "संख्यात्मक रोजगार मूल्य उपलब्ध नाही. अज्ञात म्हणजे शून्य नव्हे.",
        "status": "पडताळणी स्थिती",
        "status_verified": "सध्याच्या डेटा-पुनरावलोकन प्रक्रियेत पडताळलेले (स्वतंत्र लेखापरीक्षण नव्हे)",
        "status_needs_review": "पुनरावलोकन आवश्यक — पडताळलेले नाही",
        "status_stale": "कालबाह्य — सध्याचा पुरावा नाही",
        "status_synthetic_demo": "कृत्रिम डेमो — वास्तविक निकाल नाही",
        "geography": "भौगोलिक स्तर",
        "trade_role": "व्यवसाय / कामाची भूमिका",
        "provider_id": "प्रशिक्षण संस्था संकेतांक",
        "state": "राज्य",
        "district": "जिल्हा",
        "cohort_label": "प्रशिक्षण गटाचा कालावधी",
        "observation_label": "निरीक्षण कालावधी",
        "follow_up": "पाठपुरावा कालावधी",
        "counts": "संख्या / एकूण",
        "sample_size": "नमुना आकार",
        "earnings_semantics": "चलन / एकक / सांख्यिकी प्रकार",
        "source_publisher": "स्रोत प्रकाशित करणारी संस्था",
        "source_url": "स्रोत दुवा",
        "source_publication": "स्रोत प्रकाशन दिनांक",
        "source_reference": "स्रोत पृष्ठ / तक्ता",
        "methodology": "पद्धत आणि मर्यादा",
        "last_verified": "शेवटची पडताळणी तारीख",
        "open_source": "स्रोत उघडा",
        "numeric_metadata_withheld": "स्रोत पडताळणी पूर्ण होईपर्यंत संख्या आणि नमुना आकार लपवले आहेत.",
        "provenance_caveat": (
            "पडताळलेली स्थिती सध्याचे पुनरावलोकन लेबल आणि स्रोत माहिती दर्शवते; "
            "PathSaathi ने स्वतंत्र लेखापरीक्षण केले आहे असा अर्थ नाही."
        ),
        "compare_heading": "दोन निरीक्षणांची तुलना",
        "compare_help": "या पानावरील नेमक्या दोन नोंदी निवडा. तुलना बाजूबाजूनेच दाखवली जाते.",
        "select_two": "तुलनेसाठी नेमक्या दोन पुरावा नोंदी निवडा.",
        "compatible": "या निरीक्षणांची सध्याच्या तुलना नियमांनुसार तुलना करता येते.",
        "incompatible": "सध्याच्या नियमांनुसार ही निरीक्षणे तुलनीय नाहीत: {reasons}",
        "period_differences": "खालील व्याप्तीतील फरक स्पष्ट दाखवले आहेत; एकत्रीकरण किंवा समायोजन केलेले नाही:",
        "no_period_differences": "गट, निरीक्षण आणि पाठपुरावा कालावधी जुळतात.",
        "comparison_values": "पडताळलेली मूल्ये बाजूबाजूने",
        "comparison_numeric_blocked": "माहितीची तुलना करता येते; परंतु किमान एक संख्यात्मक मूल्य अज्ञात किंवा लपवलेले आहे.",
        "mismatch_metric": "मोजमाप संकेतांक किंवा व्याख्या",
        "mismatch_kind": "मोजमापाचा प्रकार",
        "mismatch_unit": "चलन, एकक किंवा सांख्यिकी अर्थ",
        "mismatch_geography": "भौगोलिक स्तर",
        "mismatch_trade": "व्यवसाय / कामाची भूमिका",
        "mismatch_provider": "संस्था-स्तरीय पुराव्यासाठी संस्था ओळख उपलब्ध नाही",
        "previous": "मागील पान",
        "next": "पुढील पान",
    },
}


def build_outcome_params(
    filters: Mapping[str, Any],
    *,
    limit: int = PAGE_SIZE,
    offset: int = 0,
) -> dict[str, str]:
    """Build exact API query parameters; provider IDs are scoped to provider geography."""
    if not 1 <= limit <= 100 or offset < 0:
        raise ValueError("Outcome pagination must use limit 1–100 and a non-negative offset.")

    params = {"limit": str(limit), "offset": str(offset)}
    for field in (
        "metric_code",
        "geography_name",
        "trade",
        "cohort_period",
        "observation_period",
        "verification_status",
    ):
        value = filters.get(field)
        if isinstance(value, str) and value.strip():
            params[field] = value.strip()

    geography_level = filters.get("geography_level")
    if geography_level in GEOGRAPHY_LEVELS:
        params["geography_level"] = geography_level

    provider_id = filters.get("provider_id")
    if geography_level == "provider" and isinstance(provider_id, str) and provider_id.strip():
        params["provider_id"] = provider_id.strip()

    return params


def _resolve_api_base_url(api_base_url: str | None) -> str:
    configured = api_base_url if api_base_url is not None else os.getenv(
        "PATHSAATHI_API_URL", DEFAULT_API_BASE_URL
    )
    base_url = configured.strip().rstrip("/")
    try:
        parsed = urlsplit(base_url)
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError
        _ = parsed.port
    except ValueError as exc:
        raise OutcomeApiError("The configured API base URL is invalid.", kind="configuration") from exc
    return base_url


def fetch_outcome_page(
    filters: Mapping[str, Any],
    *,
    offset: int = 0,
    api_base_url: str | None = None,
    timeout: float = API_TIMEOUT_SECONDS,
) -> list[dict[str, Any]]:
    """Fetch one bounded, stable API page; never fall back to fabricated local records."""
    base_url = _resolve_api_base_url(api_base_url)
    params = build_outcome_params(filters, offset=offset)
    url = f"{base_url}/api/v1/outcomes?{urlencode(params)}"
    request = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = "The API rejected one or more filters (HTTP 422)." if exc.code == 422 else (
            f"The API returned HTTP {exc.code}."
        )
        raise OutcomeApiError(detail, kind="http") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise OutcomeApiError("The outcome API is offline or unreachable.", kind="offline") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise OutcomeApiError("The outcome API returned an invalid response.", kind="response") from exc

    if not isinstance(payload, list) or any(not isinstance(item, dict) for item in payload):
        raise OutcomeApiError("The outcome API returned an unexpected response shape.", kind="response")
    return payload


def is_numeric_value_displayable(record: Mapping[str, Any]) -> bool:
    """Apply the API's verified-value contract again at the UI boundary."""
    return (
        record.get("verification_status") == "verified"
        and record.get("value_status") == "verified"
        and record.get("source_verified") is True
        and record.get("displayable") is True
        and record.get("value") is not None
    )


def format_outcome_value(record: Mapping[str, Any]) -> str:
    """Format a value only after the caller has checked its displayability."""
    value = record.get("value")
    number = f"{float(value):,.2f}".rstrip("0").rstrip(".")
    metric_kind = record.get("metric_kind")
    unit = record.get("unit")
    if metric_kind == "rate" and not unit:
        unit = "%"
    currency = record.get("currency")
    return " ".join(part for part in (str(currency) if currency else "", number, str(unit) if unit else "") if part)


def comparison_assessment(
    first: Mapping[str, Any],
    second: Mapping[str, Any],
) -> ComparisonAssessment:
    """Reject unlike metrics/units/granularity; disclose period differences explicitly."""
    mismatches: list[str] = []
    if (
        str(first.get("metric_code") or "").casefold()
        != str(second.get("metric_code") or "").casefold()
        or " ".join(str(first.get("definition") or "").split()).casefold()
        != " ".join(str(second.get("definition") or "").split()).casefold()
    ):
        mismatches.append("metric")
    if first.get("metric_kind") != second.get("metric_kind"):
        mismatches.append("kind")
    semantics = ("currency", "unit", "statistic_type")
    if any(
        str(first.get(field) or "").casefold() != str(second.get(field) or "").casefold()
        for field in semantics
    ):
        mismatches.append("unit")
    if first.get("geography_level") != second.get("geography_level"):
        mismatches.append("geography")
    if str(first.get("trade_or_job_role") or "").casefold() != str(
        second.get("trade_or_job_role") or ""
    ).casefold():
        mismatches.append("trade")
    if first.get("geography_level") == "provider" and (
        not first.get("provider_id") or not second.get("provider_id")
    ):
        mismatches.append("provider")

    differences: list[str] = []
    for field, label in (
        ("geography_name", "geography"),
        ("provider_id", "provider"),
        ("cohort_period", "cohort"),
        ("observation_period", "observation"),
        ("follow_up_period", "follow-up"),
    ):
        left = first.get(field) or "unknown"
        right = second.get(field) or "unknown"
        if left != right:
            differences.append(f"{label}: {left} ↔ {right}")

    return ComparisonAssessment(
        compatible=not mismatches,
        mismatches=tuple(mismatches),
        period_differences=tuple(differences),
    )


def _safe_source_url(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = urlsplit(value)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            return None
        if parsed.username is not None or parsed.password is not None:
            return None
        _ = parsed.port
    except ValueError:
        return None
    return value


def _display_text(st: Any, label: str, value: Any, unknown: str) -> None:
    st.text(f"{label}: {value if value not in (None, '') else unknown}")


def _status_label(status: Any, copy: Mapping[str, str]) -> str:
    labels = {
        "verified": copy["status_verified"],
        "needs_review": copy["status_needs_review"],
        "stale": copy["status_stale"],
        "synthetic_demo": copy["status_synthetic_demo"],
    }
    return labels.get(str(status), copy["unknown"])


def _render_record(st: Any, record: Mapping[str, Any], copy: Mapping[str, str]) -> None:
    evidence_id = str(record.get("evidence_id") or "unknown")
    with st.expander(f"{copy['evidence']}: {evidence_id}", expanded=False):
        _display_text(st, copy["metric"], record.get("metric_label"), copy["unknown"])
        _display_text(st, copy["definition"], record.get("definition"), copy["unknown"])
        _display_text(
            st,
            copy["geography"],
            f"{record.get('geography_level') or copy['unknown']}: {record.get('geography_name') or copy['unknown']}",
            copy["unknown"],
        )
        _display_text(st, copy["trade_role"], record.get("trade_or_job_role"), copy["unknown"])
        _display_text(st, copy["provider_id"], record.get("provider_id"), copy["unknown"])
        _display_text(st, copy["state"], record.get("state"), copy["unknown"])
        _display_text(st, copy["district"], record.get("district"), copy["unknown"])
        _display_text(st, copy["cohort_label"], record.get("cohort_period"), copy["unknown"])
        _display_text(st, copy["observation_label"], record.get("observation_period"), copy["unknown"])
        _display_text(st, copy["follow_up"], record.get("follow_up_period"), copy["unknown"])
        _display_text(
            st,
            copy["earnings_semantics"],
            " / ".join(
                str(record.get(field) or copy["unknown"])
                for field in ("currency", "unit", "statistic_type")
            ),
            copy["unknown"],
        )
        if is_numeric_value_displayable(record):
            st.success(f"{copy['value']}: {format_outcome_value(record)}")
        elif record.get("value_status") == "withheld" or record.get("value_withheld") is True:
            st.warning(copy["withheld"])
        else:
            st.info(copy["unknown_value"])

        if record.get("source_verified") is True and record.get("numeric_metadata_withheld") is not True:
            numerator = record.get("numerator")
            denominator = record.get("denominator")
            if numerator is not None and denominator is not None:
                _display_text(st, copy["counts"], f"{numerator} / {denominator}", copy["unknown"])
            if record.get("sample_size") is not None:
                _display_text(st, copy["sample_size"], record.get("sample_size"), copy["unknown"])
        elif record.get("numeric_metadata_withheld") is True:
            st.caption(copy["numeric_metadata_withheld"])

        _display_text(st, copy["status"], _status_label(record.get("verification_status"), copy), copy["unknown"])
        _display_text(st, copy["source_publisher"], record.get("source_publisher"), copy["unknown"])
        _display_text(st, copy["source_publication"], record.get("source_publication_date"), copy["unknown"])
        _display_text(st, copy["source_reference"], record.get("source_page_or_table"), copy["unknown"])
        _display_text(st, copy["last_verified"], record.get("last_verified_at"), copy["unknown"])
        _display_text(st, copy["methodology"], record.get("methodology"), copy["unknown"])
        source_url = _safe_source_url(record.get("source_url"))
        if source_url:
            _display_text(st, copy["source_url"], source_url, copy["unknown"])
            st.link_button(copy["open_source"], source_url)
        else:
            _display_text(st, copy["source_url"], record.get("source_url"), copy["unknown"])
        st.caption(copy["provenance_caveat"])


def render_outcome_explorer(
    st: Any,
    locale: str,
    *,
    api_base_url: str | None = None,
) -> None:
    """Render bilingual filters, provenance-first results and conservative comparisons."""
    copy = OUTCOME_EXPLORER_COPY.get(locale, OUTCOME_EXPLORER_COPY["English"])
    st.subheader(copy["heading"])
    st.write(copy["description"])
    st.warning(copy["warning"])

    state = st.session_state
    active_filters = state.get("outcome_explorer_filters", {})
    if not isinstance(active_filters, dict):
        active_filters = {}
    geography_options = ("", *GEOGRAPHY_LEVELS)
    status_options = ("", *VERIFICATION_STATUSES)
    geography_index = (
        geography_options.index(active_filters.get("geography_level"))
        if active_filters.get("geography_level") in geography_options
        else 0
    )
    status_index = (
        status_options.index(active_filters.get("verification_status"))
        if active_filters.get("verification_status") in status_options
        else 0
    )

    st.markdown(f"**{copy['filters_heading']}**")
    with st.form("outcome_explorer_filters"):
        metric_code = st.text_input(
            copy["metric_code"], value=active_filters.get("metric_code", ""), key="outcome_metric_filter"
        )
        geography_level = st.selectbox(
            copy["geography_level"],
            geography_options,
            index=geography_index,
            format_func=lambda value: copy["any_geography"] if not value else value.title(),
            key="outcome_geography_level_filter",
        )
        geography_name = st.text_input(
            copy["geography_name"],
            value=active_filters.get("geography_name", ""),
            key="outcome_geography_name_filter",
        )
        trade = st.text_input(
            copy["trade"], value=active_filters.get("trade", ""), key="outcome_trade_filter"
        )
        provider_id = ""
        if geography_level == "provider":
            provider_id = st.text_input(
                copy["provider"], value=active_filters.get("provider_id", ""), key="outcome_provider_filter"
            )
        cohort_period = st.text_input(
            copy["cohort"], value=active_filters.get("cohort_period", ""), key="outcome_cohort_filter"
        )
        observation_period = st.text_input(
            copy["observation"],
            value=active_filters.get("observation_period", ""),
            key="outcome_observation_filter",
        )
        verification_status = st.selectbox(
            copy["verification"],
            status_options,
            index=status_index,
            format_func=lambda value: copy["any_status"] if not value else _status_label(value, copy),
            key="outcome_status_filter",
        )
        submitted = st.form_submit_button(copy["apply"])

    if submitted:
        state["outcome_explorer_filters"] = {
            "metric_code": metric_code,
            "geography_level": geography_level,
            "geography_name": geography_name,
            "trade": trade,
            "provider_id": provider_id,
            "cohort_period": cohort_period,
            "observation_period": observation_period,
            "verification_status": verification_status,
        }
        state["outcome_explorer_offset"] = 0

    filters = state.get("outcome_explorer_filters", {})
    offset = int(state.get("outcome_explorer_offset", 0))
    try:
        records = fetch_outcome_page(filters, offset=offset, api_base_url=api_base_url)
    except OutcomeApiError as exc:
        if exc.kind == "offline":
            st.warning(copy["offline"])
        else:
            st.error(copy["api_error"].format(detail=str(exc)))
        return

    if not records:
        st.info(copy["empty"])
        return

    st.caption(copy["page"].format(offset=offset, count=len(records), limit=PAGE_SIZE))
    for record in records:
        _render_record(st, record, copy)

    st.subheader(copy["compare_heading"])
    st.caption(copy["compare_help"])
    record_by_id = {str(record.get("evidence_id") or ""): record for record in records}
    selected_ids = st.multiselect(
        copy["compare_heading"],
        options=list(record_by_id),
        default=[],
        format_func=lambda evidence_id: evidence_id,
        key="outcome_comparison_selection",
    )
    if len(selected_ids) == 2:
        assessment = comparison_assessment(
            record_by_id[selected_ids[0]],
            record_by_id[selected_ids[1]],
        )
        if not assessment.compatible:
            reason_labels = {
                "metric": copy["mismatch_metric"],
                "kind": copy["mismatch_kind"],
                "unit": copy["mismatch_unit"],
                "geography": copy["mismatch_geography"],
                "trade": copy["mismatch_trade"],
                "provider": copy["mismatch_provider"],
            }
            reasons = "; ".join(reason_labels[item] for item in assessment.mismatches)
            st.warning(copy["incompatible"].format(reasons=reasons))
        else:
            st.success(copy["compatible"])
            if assessment.period_differences:
                st.info(
                    copy["period_differences"]
                    + " "
                    + "; ".join(assessment.period_differences)
                )
            else:
                st.caption(copy["no_period_differences"])
            first = record_by_id[selected_ids[0]]
            second = record_by_id[selected_ids[1]]
            if is_numeric_value_displayable(first) and is_numeric_value_displayable(second):
                st.text(
                    f"{copy['comparison_values']}: "
                    f"{selected_ids[0]} = {format_outcome_value(first)} · "
                    f"{selected_ids[1]} = {format_outcome_value(second)}"
                )
            else:
                st.warning(copy["comparison_numeric_blocked"])
    elif selected_ids:
        st.warning(copy["select_two"])

    if offset > 0 and st.button(copy["previous"], key="outcome_previous_page"):
        state["outcome_explorer_offset"] = max(0, offset - PAGE_SIZE)
    if len(records) == PAGE_SIZE and st.button(copy["next"], key="outcome_next_page"):
        state["outcome_explorer_offset"] = offset + PAGE_SIZE
