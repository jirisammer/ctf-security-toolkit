import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_HISTORY_FILE = Path("data") / "history.jsonl"
MAX_STORED_VALUE_LENGTH = 5000


def _get_history_path(history_file: str | Path | None = None) -> Path:
    if history_file is None:
        return DEFAULT_HISTORY_FILE

    return Path(history_file)


def _shorten_value(value: Any) -> str:
    text = str(value)

    if len(text) <= MAX_STORED_VALUE_LENGTH:
        return text

    return text[:MAX_STORED_VALUE_LENGTH] + "... [truncated]"


def add_history_event(
    event_type: str,
    title: str,
    value: Any,
    history_file: str | Path | None = None,
) -> None:
    """
    Stores one operation result into history as JSONL.

    JSONL = one JSON object per line.
    """
    if not isinstance(event_type, str):
        raise TypeError("Event type must be a string.")

    if not isinstance(title, str):
        raise TypeError("Title must be a string.")

    path = _get_history_path(history_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "title": title,
        "value": _shorten_value(value),
    }

    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")


def read_history(
    limit: int = 20,
    history_file: str | Path | None = None,
) -> list[dict[str, Any]]:
    """
    Reads the latest history events.
    """
    if not isinstance(limit, int):
        raise TypeError("Limit must be an integer.")

    if limit <= 0:
        raise ValueError("Limit must be greater than zero.")

    path = _get_history_path(history_file)

    if not path.exists():
        return []

    events = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            cleaned_line = line.strip()

            if cleaned_line == "":
                continue

            try:
                event = json.loads(cleaned_line)

            except json.JSONDecodeError:
                continue

            if isinstance(event, dict):
                events.append(event)

    return events[-limit:]


def clear_history(history_file: str | Path | None = None) -> None:
    """
    Clears operation history.
    """
    path = _get_history_path(history_file)

    if path.exists():
        path.unlink()


def history_exists(history_file: str | Path | None = None) -> bool:
    """
    Checks whether history file exists.
    """
    path = _get_history_path(history_file)
    return path.exists()