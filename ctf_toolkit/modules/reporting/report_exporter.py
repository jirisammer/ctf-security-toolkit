import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ctf_toolkit.core.history import read_history
from ctf_toolkit.core.settings import get_setting


def _create_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def _get_reports_directory() -> Path:
    return Path(str(get_setting("reports_directory")))


def _ensure_parent_directory(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _get_default_txt_report_path() -> Path:
    timestamp = _create_timestamp()
    return _get_reports_directory() / f"ctf_report_{timestamp}.txt"


def _get_default_json_report_path() -> Path:
    timestamp = _create_timestamp()
    return _get_reports_directory() / f"ctf_report_{timestamp}.json"


def _format_event_for_txt(index: int, event: dict[str, Any]) -> str:
    timestamp = event.get("timestamp", "unknown")
    event_type = event.get("event_type", "unknown")
    title = event.get("title", "unknown")
    value = event.get("value", "")

    return (
        f"#{index}\n"
        f"Timestamp: {timestamp}\n"
        f"Type:      {event_type}\n"
        f"Title:     {title}\n"
        f"Value:\n"
        f"{value}\n"
    )


def export_history_to_txt(
    limit: int = 50,
    output_path: str | Path | None = None,
    history_file: str | Path | None = None,
) -> Path:
    """
    Exports latest operation history to a TXT report.
    """
    if not isinstance(limit, int):
        raise TypeError("Limit must be an integer.")

    if limit <= 0:
        raise ValueError("Limit must be greater than zero.")

    events = read_history(limit=limit, history_file=history_file)

    if output_path is None:
        report_path = _get_default_txt_report_path()
    else:
        report_path = Path(output_path)

    _ensure_parent_directory(report_path)

    lines = [
        "CTF Security Toolkit Report",
        "=" * 28,
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        f"Included events: {len(events)}",
        "",
    ]

    if not events:
        lines.append("No history events found.")
    else:
        for index, event in enumerate(events, start=1):
            lines.append(_format_event_for_txt(index, event))
            lines.append("-" * 60)

    report_path.write_text("\n".join(lines), encoding="utf-8")

    return report_path


def export_history_to_json(
    limit: int = 50,
    output_path: str | Path | None = None,
    history_file: str | Path | None = None,
) -> Path:
    """
    Exports latest operation history to a JSON report.
    """
    if not isinstance(limit, int):
        raise TypeError("Limit must be an integer.")

    if limit <= 0:
        raise ValueError("Limit must be greater than zero.")

    events = read_history(limit=limit, history_file=history_file)

    if output_path is None:
        report_path = _get_default_json_report_path()
    else:
        report_path = Path(output_path)

    _ensure_parent_directory(report_path)

    report_data = {
        "tool": "CTF Security Toolkit",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "included_events": len(events),
        "events": events,
    }

    report_path.write_text(
        json.dumps(report_data, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )

    return report_path