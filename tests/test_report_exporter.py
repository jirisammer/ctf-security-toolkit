import json

from ctf_toolkit.core.history import add_history_event
from ctf_toolkit.modules.reporting.report_exporter import (
    export_history_to_txt,
    export_history_to_json,
)


def test_export_history_to_txt(tmp_path):
    history_file = tmp_path / "history.jsonl"
    report_file = tmp_path / "report.txt"

    add_history_event(
        event_type="result",
        title="Base64 Encoded Result",
        value="aGVsbG8=",
        history_file=history_file,
    )

    result_path = export_history_to_txt(
        limit=10,
        output_path=report_file,
        history_file=history_file,
    )

    assert result_path == report_file
    assert report_file.exists()

    content = report_file.read_text(encoding="utf-8")

    assert "CTF Security Toolkit Report" in content
    assert "Base64 Encoded Result" in content
    assert "aGVsbG8=" in content


def test_export_history_to_json(tmp_path):
    history_file = tmp_path / "history.jsonl"
    report_file = tmp_path / "report.json"

    add_history_event(
        event_type="result",
        title="Hash Result",
        value="abc123",
        history_file=history_file,
    )

    result_path = export_history_to_json(
        limit=10,
        output_path=report_file,
        history_file=history_file,
    )

    assert result_path == report_file
    assert report_file.exists()

    content = json.loads(report_file.read_text(encoding="utf-8"))

    assert content["tool"] == "CTF Security Toolkit"
    assert content["included_events"] == 1
    assert content["events"][0]["title"] == "Hash Result"
    assert content["events"][0]["value"] == "abc123"


def test_export_history_to_txt_with_empty_history(tmp_path):
    history_file = tmp_path / "missing_history.jsonl"
    report_file = tmp_path / "empty_report.txt"

    export_history_to_txt(
        limit=10,
        output_path=report_file,
        history_file=history_file,
    )

    content = report_file.read_text(encoding="utf-8")

    assert "No history events found." in content


def test_export_history_to_json_with_empty_history(tmp_path):
    history_file = tmp_path / "missing_history.jsonl"
    report_file = tmp_path / "empty_report.json"

    export_history_to_json(
        limit=10,
        output_path=report_file,
        history_file=history_file,
    )

    content = json.loads(report_file.read_text(encoding="utf-8"))

    assert content["included_events"] == 0
    assert content["events"] == []