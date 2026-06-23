import pytest

from ctf_toolkit.modules.extraction.regex_extractor import (
    find_ctf_flags,
    extract_urls,
    extract_emails,
    extract_ipv4_addresses,
    extract_hashes,
    extract_all_indicators,
    extract_all_indicators_from_file,
)


def test_find_ctf_flags():
    text = "Here is flag{test_flag} and picoCTF{another_flag}."

    result = find_ctf_flags(text)

    assert "flag{test_flag}" in result
    assert "picoCTF{another_flag}" in result


def test_find_ctf_flags_removes_duplicates():
    text = "flag{same} flag{same}"

    result = find_ctf_flags(text)

    assert result == ["flag{same}"]


def test_extract_urls():
    text = "Visit https://example.com and http://test.local/page."

    result = extract_urls(text)

    assert "https://example.com" in result
    assert "http://test.local/page" in result


def test_extract_emails():
    text = "Contact admin@example.com or test.user@domain.cz."

    result = extract_emails(text)

    assert "admin@example.com" in result
    assert "test.user@domain.cz" in result


def test_extract_ipv4_addresses():
    text = "Valid IP: 192.168.1.10, invalid IP: 999.999.999.999"

    result = extract_ipv4_addresses(text)

    assert "192.168.1.10" in result
    assert "999.999.999.999" not in result


def test_extract_hashes_md5_sha256():
    md5_hash = "5d41402abc4b2a76b9719d911017c592"
    sha256_hash = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

    text = f"MD5: {md5_hash} SHA256: {sha256_hash}"

    result = extract_hashes(text)

    assert md5_hash in result["md5_hashes"]
    assert sha256_hash in result["sha256_hashes"]


def test_extract_all_indicators():
    text = (
        "flag{test} "
        "https://example.com "
        "admin@example.com "
        "10.0.0.1 "
        "5d41402abc4b2a76b9719d911017c592"
    )

    result = extract_all_indicators(text)

    assert "flag{test}" in result["ctf_flags"]
    assert "https://example.com" in result["urls"]
    assert "admin@example.com" in result["emails"]
    assert "10.0.0.1" in result["ipv4_addresses"]
    assert "5d41402abc4b2a76b9719d911017c592" in result["md5_hashes"]


def test_extract_all_indicators_from_file(tmp_path):
    test_file = tmp_path / "sample.bin"
    test_file.write_bytes(
        b"\x00\x01flag{file_flag}\x00"
        b"https://example.com\x00"
        b"admin@example.com\x00"
        b"192.168.0.1\x00"
    )

    result = extract_all_indicators_from_file(str(test_file))

    assert "flag{file_flag}" in result["ctf_flags"]
    assert "https://example.com" in result["urls"]
    assert "admin@example.com" in result["emails"]
    assert "192.168.0.1" in result["ipv4_addresses"]


def test_text_input_requires_string():
    with pytest.raises(TypeError):
        find_ctf_flags(123)


def test_file_path_requires_string():
    with pytest.raises(TypeError):
        extract_all_indicators_from_file(123)


def test_file_must_exist():
    with pytest.raises(FileNotFoundError):
        extract_all_indicators_from_file("missing_file.bin")


def test_min_string_length_must_be_positive(tmp_path):
    test_file = tmp_path / "sample.bin"
    test_file.write_bytes(b"hello")

    with pytest.raises(ValueError):
        extract_all_indicators_from_file(str(test_file), min_string_length=0)