"""Bilingual, preview-only Streamlit UI for outcome CSV validation."""

from __future__ import annotations

from typing import Any

from services.outcome_import import MAX_IMPORT_BYTES, parse_outcome_csv


OUTCOME_IMPORT_COPY: dict[str, dict[str, str]] = {
    "English": {
        "heading": "Outcome data — CSV review preview",
        "description": (
            "Review a canonical outcome CSV before any future staging decision. "
            "This screen validates structure and provenance; it does not verify the source."
        ),
        "access_warning": (
            "Prototype only: there is no authenticated data-steward role. This screen cannot "
            "approve, import, or persist evidence."
        ),
        "dataset_id": "Dataset ID",
        "dataset_version": "Dataset version",
        "upload": "Choose an outcome CSV file",
        "upload_help": "UTF-8 CSV only. Maximum 10 MiB and 50,000 nonblank data rows.",
        "waiting": "Choose a CSV file to see its validation report.",
        "metadata_required": "Enter both a dataset ID and dataset version before reviewing the file.",
        "extension_error": "Unsupported file: the filename must end in .csv.",
        "mime_error": "Unsupported file type. Upload a CSV file, not a spreadsheet or other document.",
        "size_error": "File exceeds the 10 MiB upload limit. No parsing was attempted.",
        "read_error": "The uploaded file could not be read as bytes.",
        "parse_error": "The CSV could not be validated: {detail}",
        "audit_heading": "Import-attempt metadata",
        "filename": "Source filename",
        "sha256": "SHA-256",
        "imported_at": "Import timestamp (UTC)",
        "dataset": "Dataset",
        "rows": "Nonblank data rows",
        "accepted": "Rows passing row validation",
        "rejected": "Rows with blocking errors",
        "validation_heading": "Validation result",
        "ready": "Every nonblank row passed canonical validation. This is a preview only; nothing was imported.",
        "blocked": (
            "The file is not ready: at least one row failed or the file is empty. "
            "No rows are staged or presented as an importable dataset."
        ),
        "findings_heading": "All validation findings",
        "no_findings": "No row-level errors or warnings were reported.",
        "row": "CSV row",
        "file_level": "File-level",
        "preview_heading": "Validated-row preview",
        "preview_note": (
            "Rows appear here only when the entire file passes. Status labels are evidence "
            "qualifications, not approval; unverified values are not verified outcomes."
        ),
        "evidence_id": "Evidence ID",
        "metric": "Metric",
        "definition": "Definition",
        "geography": "Geography",
        "trade": "Trade / job role",
        "value": "Value",
        "counts": "Numerator / denominator",
        "sample_size": "Sample size",
        "cohort": "Cohort",
        "observation": "Observation period",
        "follow_up": "Follow-up",
        "source": "Source",
        "status": "Evidence status",
        "unknown": "Unknown — not supplied",
        "synthetic": "SYNTHETIC DEMO — not real outcomes",
        "needs_review": "Needs review — not verified",
        "stale": "Stale — not current evidence",
        "no_value": "Unknown — no numeric value supplied",
        "not_persisted": (
            "No database, API, or external service was contacted. Correct errors and review "
            "provenance outside this prototype before any authorised import workflow."
        ),
        "marathi_review": "Marathi wording is a draft and requires fluent human review.",
    },
    "मराठी": {
        "heading": "रोजगारविषयक माहिती — CSV तपासणी पूर्वदृश्य",
        "description": (
            "भविष्यात माहिती साठवण्याचा निर्णय घेण्यापूर्वी प्रमाणित CSV तपासा. "
            "ही स्क्रीन रचना आणि स्रोत तपासते; स्रोताची सत्यता प्रमाणित करत नाही."
        ),
        "access_warning": (
            "ही नमुना आवृत्ती आहे: अधिकृत डेटा-व्यवस्थापकाची ओळख पडताळणी नाही. "
            "या स्क्रीनवरून माहिती मंजूर, आयात किंवा साठवली जात नाही."
        ),
        "dataset_id": "डेटासेट संकेतांक",
        "dataset_version": "डेटासेट आवृत्ती",
        "upload": "रोजगारविषयक CSV फाइल निवडा",
        "upload_help": "फक्त UTF-8 CSV. कमाल 10 MiB आणि 50,000 रिकाम्या नसलेल्या नोंदी.",
        "waiting": "तपासणी अहवाल पाहण्यासाठी CSV फाइल निवडा.",
        "metadata_required": "फाइल तपासण्यापूर्वी डेटासेट संकेतांक आणि आवृत्ती भरा.",
        "extension_error": "असमर्थित फाइल: नावाचा शेवट .csv असा असणे आवश्यक आहे.",
        "mime_error": "फाइलचा प्रकार समर्थित नाही. CSV फाइल अपलोड करा.",
        "size_error": "फाइल 10 MiB मर्यादेपेक्षा मोठी आहे. तिचे विश्लेषण केलेले नाही.",
        "read_error": "अपलोड केलेली फाइल बाइट्स म्हणून वाचता आली नाही.",
        "parse_error": "CSV तपासता आली नाही: {detail}",
        "audit_heading": "आयात प्रयत्नाची माहिती",
        "filename": "मूळ फाइलचे नाव",
        "sha256": "SHA-256",
        "imported_at": "तपासणीची वेळ (UTC)",
        "dataset": "डेटासेट",
        "rows": "रिकाम्या नसलेल्या नोंदी",
        "accepted": "नोंद तपासणीत उत्तीर्ण",
        "rejected": "त्रुटी असलेल्या नोंदी",
        "validation_heading": "तपासणीचा निकाल",
        "ready": "प्रत्येक नोंद प्रमाणित रचना तपासणीत उत्तीर्ण झाली. हे फक्त पूर्वदृश्य आहे; माहिती आयात केलेली नाही.",
        "blocked": (
            "फाइल तयार नाही: किमान एका नोंदीत त्रुटी आहे किंवा फाइल रिकामी आहे. "
            "कोणतीही नोंद साठवलेली किंवा आयातयोग्य म्हणून दाखवलेली नाही."
        ),
        "findings_heading": "सर्व तपासणी निष्कर्ष",
        "no_findings": "नोंद-स्तरावर त्रुटी किंवा सूचना आढळल्या नाहीत.",
        "row": "CSV ओळ",
        "file_level": "फाइल स्तर",
        "preview_heading": "तपासलेली नोंद — पूर्वदृश्य",
        "preview_note": (
            "संपूर्ण फाइल उत्तीर्ण झाल्यावरच नोंदी येथे दिसतात. स्थितीचे लेबल म्हणजे "
            "पुराव्याची मर्यादा; मंजुरी किंवा पडताळणी नव्हे."
        ),
        "evidence_id": "पुरावा संकेतांक",
        "metric": "मोजमाप",
        "definition": "व्याख्या",
        "geography": "भौगोलिक स्तर",
        "trade": "व्यवसाय / कामाची भूमिका",
        "value": "मूल्य",
        "counts": "संख्या / एकूण",
        "sample_size": "नमुना आकार",
        "cohort": "गट कालावधी",
        "observation": "निरीक्षण कालावधी",
        "follow_up": "पाठपुरावा",
        "source": "स्रोत",
        "status": "पुराव्याची स्थिती",
        "unknown": "अज्ञात — माहिती दिलेली नाही",
        "synthetic": "कृत्रिम डेमो — वास्तविक रोजगार निकाल नाहीत",
        "needs_review": "पुनरावलोकन आवश्यक — पडताळलेले नाही",
        "stale": "कालबाह्य — सध्याचा पुरावा नाही",
        "no_value": "अज्ञात — संख्यात्मक मूल्य दिलेले नाही",
        "not_persisted": (
            "कोणताही डेटाबेस, API किंवा बाह्य सेवा वापरलेली नाही. अधिकृत आयात प्रक्रियेपूर्वी "
            "त्रुटी दुरुस्त करा आणि स्रोत स्वतंत्रपणे तपासा."
        ),
        "marathi_review": "मराठी मजकूर मसुदा आहे; भाषातज्ज्ञाकडून मानवी पुनरावलोकन आवश्यक आहे.",
    },
}

_ALLOWED_CSV_MIME_TYPES = {
    "text/csv",
    "application/csv",
    "application/vnd.ms-excel",
}


def _record_preview(record: Any, copy: dict[str, str]) -> dict[str, str]:
    """Build a display-only row while retaining explicit unknown and review states."""
    if record.verification_status == "synthetic_demo":
        status = copy["synthetic"]
    elif record.verification_status == "stale":
        status = copy["stale"]
    else:
        status = copy["needs_review"]

    value = copy["no_value"] if record.value is None else str(record.value)
    if record.value is not None and record.unit:
        value = f"{value} {record.unit}"
    if record.currency:
        value = f"{record.currency} {value}"

    counts = (
        copy["unknown"]
        if record.numerator is None or record.denominator is None
        else f"{record.numerator} / {record.denominator}"
    )
    source = record.source_url or record.source_page_or_table or copy["unknown"]
    return {
        copy["evidence_id"]: record.evidence_id,
        copy["metric"]: record.metric_label,
        copy["definition"]: record.definition,
        copy["geography"]: f"{record.geography_level}: {record.geography_name}",
        copy["trade"]: record.trade_or_job_role or copy["unknown"],
        copy["value"]: value,
        copy["counts"]: counts,
        copy["sample_size"]: (
            copy["unknown"] if record.sample_size is None else str(record.sample_size)
        ),
        copy["cohort"]: record.cohort_period or copy["unknown"],
        copy["observation"]: record.observation_period or copy["unknown"],
        copy["follow_up"]: record.follow_up_period or copy["unknown"],
        copy["source"]: source,
        copy["status"]: status,
    }


def render_outcome_import(st: Any, locale: str) -> None:
    """Render a safe bilingual CSV review; never persist or approve uploaded evidence."""
    copy = OUTCOME_IMPORT_COPY.get(locale, OUTCOME_IMPORT_COPY["English"])
    st.subheader(copy["heading"])
    st.write(copy["description"])
    st.warning(copy["access_warning"])

    dataset_id = st.text_input(copy["dataset_id"], value="", key="outcome_dataset_id")
    dataset_version = st.text_input(
        copy["dataset_version"], value="", key="outcome_dataset_version"
    )
    upload = st.file_uploader(
        copy["upload"],
        type=["csv"],
        accept_multiple_files=False,
        help=copy["upload_help"],
        key="outcome_csv_upload",
    )
    if upload is None:
        st.caption(copy["waiting"])
        if locale == "मराठी":
            st.caption(copy["marathi_review"])
        return

    filename = str(getattr(upload, "name", "upload"))
    if not filename.casefold().endswith(".csv"):
        st.error(copy["extension_error"])
        return

    mime_type = str(getattr(upload, "type", "") or "").split(";", 1)[0].strip().casefold()
    if mime_type and mime_type not in _ALLOWED_CSV_MIME_TYPES:
        st.error(copy["mime_error"])
        return

    try:
        payload = upload.getvalue()
    except (AttributeError, OSError, TypeError, ValueError):
        st.error(copy["read_error"])
        return
    if not isinstance(payload, bytes):
        try:
            payload = bytes(payload)
        except (TypeError, ValueError):
            st.error(copy["read_error"])
            return

    if len(payload) > MAX_IMPORT_BYTES:
        st.error(copy["size_error"])
        return
    if not dataset_id.strip() or not dataset_version.strip():
        st.error(copy["metadata_required"])
        return

    try:
        report = parse_outcome_csv(
            payload,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            source_filename=filename,
        )
    except (ValueError, UnicodeError, OSError) as exc:
        st.error(copy["parse_error"].format(detail=str(exc)))
        return

    st.markdown(f"**{copy['audit_heading']}**")
    st.write(f"{copy['dataset']}: {report.dataset_id} · {report.dataset_version}")
    st.write(f"{copy['filename']}: {report.source_filename}")
    st.code(report.source_sha256, language="text")
    st.write(f"{copy['imported_at']}: {report.imported_at.isoformat()}")
    st.write(f"{copy['rows']}: {report.row_count}")
    st.write(f"{copy['accepted']}: {report.accepted_row_count}")
    st.write(f"{copy['rejected']}: {report.rejected_row_count}")

    st.markdown(f"**{copy['validation_heading']}**")
    if report.ready_to_import:
        st.success(copy["ready"])
    else:
        st.error(copy["blocked"])

    st.markdown(f"**{copy['findings_heading']}**")
    if not report.findings:
        st.write(copy["no_findings"])
    for finding in report.findings:
        row_label = (
            copy["file_level"]
            if finding.row_number <= 0
            else f"{copy['row']} {finding.row_number}"
        )
        field = f" · {finding.field_name}" if finding.field_name else ""
        message = f"{row_label} · {finding.code}{field}: {finding.message}"
        if finding.severity == "error":
            st.error(message)
        else:
            st.warning(message)

    if report.ready_to_import:
        st.markdown(f"**{copy['preview_heading']}**")
        st.caption(copy["preview_note"])
        st.table([_record_preview(record, copy) for record in report.records])
    st.info(copy["not_persisted"])
    if locale == "मराठी":
        st.caption(copy["marathi_review"])
