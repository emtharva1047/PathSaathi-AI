"""Bilingual, read-only course catalogue explorer for Streamlit."""

from __future__ import annotations

import json
import os
from contextlib import nullcontext
from decimal import Decimal
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

from core.domain import normalize_nsqf_level

DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"
API_TIMEOUT_SECONDS = 3.0
PAGE_SIZE = 50
MAX_PAGE_SIZE = 100


class CourseApiError(RuntimeError):
    """Safe, user-displayable error raised while reading the course catalogue."""

    def __init__(self, message: str, *, kind: str = "api") -> None:
        super().__init__(message)
        self.kind = kind


COURSE_EXPLORER_COPY: dict[str, dict[str, str]] = {
    "English": {
        "heading": "Explore the course catalogue",
        "description": (
            "Search course and qualification records returned by the read-only API. "
            "Filters use exact matches; no broader location or substitute record is shown."
        ),
        "warning": (
            "A catalogue record is not proof of current admission, provider availability, "
            "seats, fees, placement, earnings or job security. Confirm details with the "
            "awarding body or provider before making a decision."
        ),
        "filters_heading": "Course filters",
        "state": "State",
        "district": "District",
        "trade": "Trade / job role",
        "provider": "Provider ID",
        "min_nsqf": "Minimum NSQF level (whole or half steps)",
        "max_nsqf": "Maximum NSQF level (whole or half steps)",
        "apply": "Search courses",
        "unknown": "Not supplied — unknown",
        "offline": "Course catalogue API is offline or unreachable. No local or synthetic courses are substituted.",
        "api_error": "The course catalogue request failed: {detail}",
        "invalid_filter": "Check the course filters. NSQF levels must be from 1 to 10 in whole or half steps, and the minimum cannot exceed the maximum.",
        "empty": (
            "No course records match these exact filters in the currently available catalogue. "
            "This does not establish that no courses exist elsewhere."
        ),
        "page": "Page offset: {offset} · {count} records returned (maximum {limit} per request).",
        "course": "Course record",
        "title": "Title",
        "trade_label": "Trade",
        "qualification_code": "Qualification code",
        "awarding_body": "Awarding body",
        "nsqf": "NSQF level",
        "job_roles": "Job roles",
        "entry_requirements": "Published entry requirements",
        "state_label": "State",
        "district_label": "District",
        "provider_label": "Provider ID",
        "status": "Verification status",
        "verified": "Verified source metadata in the current review workflow (not an independent audit claim)",
        "verified_incomplete": "Marked verified, but source metadata is incomplete; it is not treated as verified here.",
        "needs_review": "Needs review — not verified",
        "stale": "Stale — not current evidence",
        "synthetic_demo": "Synthetic demo — not a real course offer",
        "source_publisher": "Source publisher",
        "source_url": "Source URL",
        "source_publication": "Source publication date",
        "last_verified": "Last verification date",
        "open_source": "Open source",
        "invalid_source": "The supplied source URL is not a safe HTTP(S) link and cannot be opened.",
        "provenance_caveat": (
            "The verification label reflects the current review workflow and supplied metadata; "
            "PathSaathi has not independently audited the source."
        ),
        "advisory": (
            "Use this catalogue to explore published qualification information only. "
            "Unknown fields remain unknown; verify local delivery and admission directly."
        ),
        "previous": "Previous page",
        "next": "Next page",
    },
    "मराठी": {
        "heading": "अभ्यासक्रम सूची पाहा",
        "description": (
            "फक्त-वाचन API मधून मिळालेल्या अभ्यासक्रम आणि पात्रता नोंदी शोधा. "
            "फिल्टर अचूक जुळणी वापरतात; मोठ्या क्षेत्राचा किंवा पर्यायी नोंदीचा निकाल दाखवला जात नाही."
        ),
        "warning": (
            "सूचीतील नोंद म्हणजे सध्या प्रवेश, प्रशिक्षण संस्था उपलब्धता, जागा, शुल्क, "
            "प्लेसमेंट, उत्पन्न किंवा नोकरीची हमी नव्हे. निर्णय घेण्यापूर्वी संबंधित संस्था किंवा "
            "प्रशिक्षण केंद्राकडून माहिती तपासा."
        ),
        "filters_heading": "अभ्यासक्रम फिल्टर",
        "state": "राज्य",
        "district": "जिल्हा",
        "trade": "व्यवसाय / कामाची भूमिका",
        "provider": "प्रशिक्षण संस्था संकेतांक",
        "min_nsqf": "किमान NSQF स्तर (पूर्ण किंवा अर्धे टप्पे)",
        "max_nsqf": "कमाल NSQF स्तर (पूर्ण किंवा अर्धे टप्पे)",
        "apply": "अभ्यासक्रम शोधा",
        "unknown": "दिलेली नाही — अज्ञात",
        "offline": "अभ्यासक्रम सूची API उपलब्ध नाही. त्याऐवजी स्थानिक किंवा कृत्रिम अभ्यासक्रम दाखवले जाणार नाहीत.",
        "api_error": "अभ्यासक्रम सूची विनंती पूर्ण झाली नाही: {detail}",
        "invalid_filter": "अभ्यासक्रम फिल्टर तपासा. NSQF स्तर 1 ते 10 दरम्यान पूर्ण किंवा अर्ध्या टप्प्यात असावा आणि किमान स्तर कमाल स्तरापेक्षा जास्त नसावा.",
        "empty": (
            "सध्या उपलब्ध सूचीमध्ये या अचूक फिल्टरशी जुळणारी अभ्यासक्रम नोंद नाही. "
            "याचा अर्थ इतरत्र अभ्यासक्रम नाही असा होत नाही."
        ),
        "page": "पानाचा प्रारंभ: {offset} · मिळालेल्या नोंदी: {count} (प्रति विनंती कमाल {limit}).",
        "course": "अभ्यासक्रम नोंद",
        "title": "शीर्षक",
        "trade_label": "व्यवसाय",
        "qualification_code": "पात्रता संकेतांक",
        "awarding_body": "प्रमाणपत्र देणारी संस्था",
        "nsqf": "NSQF स्तर",
        "job_roles": "कामाच्या भूमिका",
        "entry_requirements": "प्रकाशित प्रवेश अटी",
        "state_label": "राज्य",
        "district_label": "जिल्हा",
        "provider_label": "प्रशिक्षण संस्था संकेतांक",
        "status": "पडताळणी स्थिती",
        "verified": "सध्याच्या पुनरावलोकन प्रक्रियेत स्रोत माहिती पडताळलेली (स्वतंत्र लेखापरीक्षण नव्हे)",
        "verified_incomplete": "पडताळलेले असे चिन्हांकित आहे; परंतु स्रोत माहिती अपूर्ण असल्यामुळे येथे पडताळलेले मानलेले नाही.",
        "needs_review": "पुनरावलोकन आवश्यक — पडताळलेले नाही",
        "stale": "कालबाह्य — सध्याचा पुरावा नाही",
        "synthetic_demo": "कृत्रिम डेमो — वास्तविक अभ्यासक्रम ऑफर नाही",
        "source_publisher": "स्रोत प्रकाशित करणारी संस्था",
        "source_url": "स्रोत दुवा",
        "source_publication": "स्रोत प्रकाशन दिनांक",
        "last_verified": "शेवटची पडताळणी तारीख",
        "open_source": "स्रोत उघडा",
        "invalid_source": "दिलेला स्रोत दुवा सुरक्षित HTTP(S) दुवा नाही; तो उघडता येणार नाही.",
        "provenance_caveat": (
            "पडताळणी लेबल सध्याची पुनरावलोकन प्रक्रिया आणि दिलेली स्रोत माहिती दर्शवते; "
            "PathSaathi ने स्वतंत्र लेखापरीक्षण केलेले नाही."
        ),
        "advisory": (
            "ही सूची फक्त प्रकाशित पात्रता माहिती पाहण्यासाठी वापरा. अज्ञात माहिती अज्ञातच राहते; "
            "स्थानिक प्रशिक्षण आणि प्रवेशाची माहिती थेट तपासा."
        ),
        "previous": "मागील पान",
        "next": "पुढील पान",
    },
}


def _parse_nsqf_filter(value: Any, field: str) -> Decimal | None:
    """Parse an optional exact NSQF level while preserving half-step semantics."""
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    try:
        return normalize_nsqf_level(raw)
    except ValueError as exc:
        raise CourseApiError(
            f"{field} must be between 1 and 10 in whole or half-level increments.",
            kind="validation",
        ) from exc


def build_course_params(
    filters: Mapping[str, Any],
    *,
    limit: int = PAGE_SIZE,
    offset: int = 0,
) -> dict[str, str]:
    """Build exact course API filters and validate pagination and NSQF bounds."""
    if not 1 <= limit <= MAX_PAGE_SIZE or offset < 0:
        raise CourseApiError(
            "Course pagination must use limit 1–100 and a non-negative offset.",
            kind="validation",
        )

    params = {"limit": str(limit), "offset": str(offset)}
    for field in ("state", "district", "trade", "provider_id"):
        value = filters.get(field)
        if isinstance(value, str) and value.strip():
            params[field] = value.strip()

    minimum = _parse_nsqf_filter(filters.get("min_nsqf_level"), "Minimum NSQF level")
    maximum = _parse_nsqf_filter(filters.get("max_nsqf_level"), "Maximum NSQF level")
    if minimum is not None and maximum is not None and minimum > maximum:
        raise CourseApiError(
            "Minimum NSQF level cannot exceed maximum NSQF level.",
            kind="validation",
        )
    if minimum is not None:
        params["min_nsqf_level"] = format(minimum, "f")
    if maximum is not None:
        params["max_nsqf_level"] = format(maximum, "f")
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
        raise CourseApiError("The configured API base URL is invalid.", kind="configuration") from exc
    return base_url


def fetch_course_page(
    filters: Mapping[str, Any],
    *,
    offset: int = 0,
    api_base_url: str | None = None,
    timeout: float = API_TIMEOUT_SECONDS,
) -> list[dict[str, Any]]:
    """Fetch one bounded API page; never fall back to local or synthetic course records."""
    params = build_course_params(filters, offset=offset)
    base_url = _resolve_api_base_url(api_base_url)
    request = Request(
        f"{base_url}/api/v1/courses?{urlencode(params)}",
        headers={"Accept": "application/json"},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = (
            "The API rejected one or more filters (HTTP 422)."
            if exc.code == 422
            else f"The API returned HTTP {exc.code}."
        )
        raise CourseApiError(detail, kind="http") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise CourseApiError("The course catalogue API is offline or unreachable.", kind="offline") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CourseApiError("The course catalogue API returned an invalid response.", kind="response") from exc

    if not isinstance(payload, list) or any(not isinstance(item, dict) for item in payload):
        raise CourseApiError("The course catalogue API returned an unexpected response shape.", kind="response")
    return payload


def safe_source_url(value: Any) -> str | None:
    """Return only credential-free HTTP(S) URLs suitable for a source link."""
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


def _display_value(st: Any, label: str, value: Any, unknown: str) -> None:
    st.text(f"{label}: {value if value not in (None, '') else unknown}")


def _status_label(record: Mapping[str, Any], copy: Mapping[str, str]) -> tuple[str, str]:
    """Return a label and presentation kind without trusting status alone."""
    status = record.get("verification_status")
    source_verified = record.get("source_verified") is True
    if status == "verified" and source_verified:
        return copy["verified"], "success"
    if status == "verified":
        return copy["verified_incomplete"], "warning"
    labels = {
        "needs_review": copy["needs_review"],
        "stale": copy["stale"],
        "synthetic_demo": copy["synthetic_demo"],
    }
    return labels.get(str(status), copy["unknown"]), "info"


def _format_nsqf(value: Any, unknown: str) -> str:
    if value is None:
        return unknown
    try:
        decimal_value = normalize_nsqf_level(value)
    except ValueError:
        return unknown
    return format(decimal_value, "f")


def _format_list(value: Any, unknown: str) -> str:
    if not isinstance(value, (list, tuple)):
        return unknown
    values = [str(item).strip() for item in value if isinstance(item, str) and item.strip()]
    return ", ".join(values) if values else unknown


def _render_course(st: Any, record: Mapping[str, Any], copy: Mapping[str, str]) -> None:
    course_id = str(record.get("course_id") or copy["unknown"])
    title = str(record.get("title") or copy["unknown"])
    with st.expander(f"{copy['course']}: {title} · {course_id}", expanded=False):
        _display_value(st, copy["title"], record.get("title"), copy["unknown"])
        _display_value(st, copy["trade_label"], record.get("trade"), copy["unknown"])
        _display_value(st, copy["qualification_code"], record.get("qualification_code"), copy["unknown"])
        _display_value(st, copy["awarding_body"], record.get("awarding_body"), copy["unknown"])
        _display_value(st, copy["nsqf"], _format_nsqf(record.get("nsqf_level"), copy["unknown"]), copy["unknown"])
        _display_value(st, copy["job_roles"], _format_list(record.get("job_roles"), copy["unknown"]), copy["unknown"])
        _display_value(
            st,
            copy["entry_requirements"],
            _format_list(record.get("entry_requirements"), copy["unknown"]),
            copy["unknown"],
        )
        _display_value(st, copy["state_label"], record.get("state"), copy["unknown"])
        _display_value(st, copy["district_label"], record.get("district"), copy["unknown"])
        _display_value(st, copy["provider_label"], record.get("provider_id"), copy["unknown"])

        status_text, status_kind = _status_label(record, copy)
        if status_kind == "success":
            st.success(f"{copy['status']}: {status_text}")
        elif status_kind == "warning":
            st.warning(f"{copy['status']}: {status_text}")
        else:
            st.info(f"{copy['status']}: {status_text}")

        _display_value(st, copy["source_publisher"], record.get("source_publisher"), copy["unknown"])
        _display_value(st, copy["source_publication"], record.get("source_publication_date"), copy["unknown"])
        _display_value(st, copy["last_verified"], record.get("last_verified_at"), copy["unknown"])
        source_value = record.get("source_url")
        source_url = safe_source_url(source_value)
        _display_value(st, copy["source_url"], source_value, copy["unknown"])
        if source_url:
            st.link_button(copy["open_source"], source_url)
        elif source_value not in (None, ""):
            st.caption(copy["invalid_source"])
        st.caption(copy["provenance_caveat"])


def render_course_explorer(
    st: Any,
    locale: str,
    *,
    api_base_url: str | None = None,
) -> None:
    """Render exact bilingual course filters and provenance-first API results."""
    copy = COURSE_EXPLORER_COPY.get(locale, COURSE_EXPLORER_COPY["English"])
    st.subheader(copy["heading"])
    st.write(copy["description"])
    st.warning(copy["warning"])
    st.caption(copy["advisory"])

    state = st.session_state
    active_filters = state.get("course_explorer_filters", {})
    if not isinstance(active_filters, dict):
        active_filters = {}

    st.markdown(f"**{copy['filters_heading']}**")
    form_factory = getattr(st, "form", None)
    form_context = form_factory("course_explorer_filters") if callable(form_factory) else None
    if form_context is None:
        form_context = nullcontext()
    with form_context:
        state_name = st.text_input(
            copy["state"], value=active_filters.get("state", ""), key="course_state_filter"
        )
        district = st.text_input(
            copy["district"], value=active_filters.get("district", ""), key="course_district_filter"
        )
        trade = st.text_input(
            copy["trade"], value=active_filters.get("trade", ""), key="course_trade_filter"
        )
        provider_id = st.text_input(
            copy["provider"], value=active_filters.get("provider_id", ""), key="course_provider_filter"
        )
        min_nsqf_level = st.text_input(
            copy["min_nsqf"], value=active_filters.get("min_nsqf_level", ""), key="course_min_nsqf_filter"
        )
        max_nsqf_level = st.text_input(
            copy["max_nsqf"], value=active_filters.get("max_nsqf_level", ""), key="course_max_nsqf_filter"
        )
        submitted = st.form_submit_button(copy["apply"])

    if submitted:
        state["course_explorer_filters"] = {
            "state": state_name,
            "district": district,
            "trade": trade,
            "provider_id": provider_id,
            "min_nsqf_level": min_nsqf_level,
            "max_nsqf_level": max_nsqf_level,
        }
        state["course_explorer_offset"] = 0

    filters = state.get("course_explorer_filters", {})
    try:
        offset = int(state.get("course_explorer_offset", 0))
        if offset < 0:
            raise ValueError
    except (TypeError, ValueError):
        offset = 0
        state["course_explorer_offset"] = 0

    try:
        records = fetch_course_page(filters, offset=offset, api_base_url=api_base_url)
    except CourseApiError as exc:
        if exc.kind == "offline":
            st.warning(copy["offline"])
        elif exc.kind == "validation":
            st.error(copy["invalid_filter"])
        else:
            st.error(copy["api_error"].format(detail=str(exc)))
        return

    if not records:
        st.info(copy["empty"])
        if offset > 0 and st.button(copy["previous"], key="course_previous_page"):
            state["course_explorer_offset"] = max(0, offset - PAGE_SIZE)
        return

    st.caption(copy["page"].format(offset=offset, count=len(records), limit=PAGE_SIZE))
    for record in records:
        _render_course(st, record, copy)

    if offset > 0 and st.button(copy["previous"], key="course_previous_page"):
        state["course_explorer_offset"] = max(0, offset - PAGE_SIZE)
    if len(records) == PAGE_SIZE and st.button(copy["next"], key="course_next_page"):
        state["course_explorer_offset"] = offset + PAGE_SIZE
