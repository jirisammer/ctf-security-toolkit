import pytest

from ctf_toolkit.cli.command_runner import build_argument_parser, run_cli_command
from ctf_toolkit.core import output as output_module


@pytest.fixture(autouse=True)
def disable_history(monkeypatch):
    monkeypatch.setattr(
        output_module,
        "add_history_event",
        lambda *args, **kwargs: None,
    )


def test_parser_base64_encode_args():
    parser = build_argument_parser()

    args = parser.parse_args(["base64-encode", "hello"])

    assert args.command == "base64-encode"
    assert args.text == "hello"
    assert args.output == "rich"


def test_parser_json_output_args():
    parser = build_argument_parser()

    args = parser.parse_args(["--output", "json", "base64-encode", "hello"])

    assert args.command == "base64-encode"
    assert args.text == "hello"
    assert args.output == "json"


def test_run_base64_encode_command():
    exit_code = run_cli_command(["--output", "plain", "base64-encode", "hello"])

    assert exit_code == 0


def test_run_base64_decode_command():
    exit_code = run_cli_command(["--output", "plain", "base64-decode", "aGVsbG8="])

    assert exit_code == 0


def test_run_hex_encode_command():
    exit_code = run_cli_command(["--output", "plain", "hex-encode", "hello"])

    assert exit_code == 0


def test_run_rot13_command():
    exit_code = run_cli_command(["--output", "plain", "rot13", "hello"])

    assert exit_code == 0


def test_run_caesar_encrypt_command():
    exit_code = run_cli_command(["--output", "plain", "caesar-encrypt", "hello", "3"])

    assert exit_code == 0


def test_run_hash_command():
    exit_code = run_cli_command(["--output", "plain", "hash", "hello", "sha256"])

    assert exit_code == 0


def test_run_analyze_command():
    exit_code = run_cli_command(["--output", "plain", "analyze", "aGVsbG8="])

    assert exit_code == 0


def test_run_extract_command():
    exit_code = run_cli_command(
        [
            "--output",
            "plain",
            "extract",
            "flag{test} https://example.com admin@example.com 192.168.1.10",
        ]
    )

    assert exit_code == 0


def test_invalid_base64_decode_returns_error():
    exit_code = run_cli_command(
        ["--output", "plain", "base64-decode", "not-valid-base64!!!"]
    )

    assert exit_code == 1


def test_no_command_prints_help():
    exit_code = run_cli_command([])

    assert exit_code == 0