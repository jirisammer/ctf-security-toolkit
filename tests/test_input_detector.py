import pytest

from ctf_toolkit.modules.detection.input_detector import analyze_input


def _get_types(results: list[dict[str, str]]) -> list[str]:
    return [result["type"] for result in results]


def test_detect_base64():
    results = analyze_input("aGVsbG8=")
    detected_types = _get_types(results)

    assert "Base64" in detected_types


def test_detect_hex():
    results = analyze_input("68656c6c6f")
    detected_types = _get_types(results)

    assert "Hex" in detected_types


def test_detect_url_encoding():
    results = analyze_input("flag%7Bhello%20world%7D")
    detected_types = _get_types(results)

    assert "URL Encoding" in detected_types


def test_detect_md5_hash():
    results = analyze_input("5d41402abc4b2a76b9719d911017c592")
    detected_types = _get_types(results)

    assert "Hash" in detected_types
    assert "MD5" in results[0]["details"]


def test_detect_sha256_hash():
    results = analyze_input(
        "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    )
    detected_types = _get_types(results)

    assert "Hash" in detected_types
    assert "SHA256" in results[0]["details"]


def test_detect_jwt():
    token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.signature"
    results = analyze_input(token)
    detected_types = _get_types(results)

    assert "JWT" in detected_types


def test_unknown_plain_text():
    results = analyze_input("hello world this is normal text")
    detected_types = _get_types(results)

    assert "Unknown / Plain text" in detected_types


def test_empty_input():
    results = analyze_input("")
    detected_types = _get_types(results)

    assert "Empty input" in detected_types


def test_input_requires_string():
    with pytest.raises(TypeError):
        analyze_input(123)