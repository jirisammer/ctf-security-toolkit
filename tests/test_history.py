from ctf_toolkit.core.history import (
    add_history_event,
    clear_history,
    history_exists,
    read_history,
)


def test_add_and_read_history_event(tmp_path):
    history_file = tmp_path / "history.jsonl"

    add_history_event(
        event_type="result",
        title="Test Result",
        value="hello",
        history_file=history_file,
    )

    events = read_history(
        limit=10,
        history_file=history_file,
    )

    assert len(events) == 1
    assert events[0]["event_type"] == "result"
    assert events[0]["title"] == "Test Result"
    assert events[0]["value"] == "hello"


def test_read_history_returns_latest_events(tmp_path):
    history_file = tmp_path / "history.jsonl"

    add_history_event("result", "First", "1", history_file)
    add_history_event("result", "Second", "2", history_file)
    add_history_event("result", "Third", "3", history_file)

    events = read_history(
        limit=2,
        history_file=history_file,
    )

    assert len(events) == 2
    assert events[0]["title"] == "Second"
    assert events[1]["title"] == "Third"


def test_read_history_empty_file(tmp_path):
    history_file = tmp_path / "missing_history.jsonl"

    events = read_history(
        limit=10,
        history_file=history_file,
    )

    assert events == []


def test_clear_history(tmp_path):
    history_file = tmp_path / "history.jsonl"

    add_history_event(
        event_type="result",
        title="Test",
        value="hello",
        history_file=history_file,
    )

    assert history_exists(history_file) is True

    clear_history(history_file)

    assert history_exists(history_file) is False