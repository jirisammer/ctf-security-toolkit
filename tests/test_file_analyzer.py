import pytest

from ctf_toolkit.modules.files.file_analyzer import (
    get_file_info,
    calculate_file_hash,
    extract_printable_strings,
)


def test_get_file_info(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("hello", encoding="utf-8")

    result = get_file_info(str(test_file))

    assert result["name"] == "sample.txt"
    assert result["extension"] == ".txt"
    assert result["size_bytes"] == 5
    assert result["mime_type"] == "text/plain"


def test_calculate_file_sha256_hash(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("hello", encoding="utf-8")

    result = calculate_file_hash(str(test_file), "sha256")

    assert result == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_calculate_file_md5_hash(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("hello", encoding="utf-8")

    result = calculate_file_hash(str(test_file), "md5")

    assert result == "5d41402abc4b2a76b9719d911017c592"


def test_extract_printable_strings(tmp_path):
    test_file = tmp_path / "sample.bin"
    test_file.write_bytes(b"\x00\x01flag{test_flag}\x00\x02hello_world\x00")

    result = extract_printable_strings(str(test_file), min_length=4)

    assert "flag{test_flag}" in result
    assert "hello_world" in result


def test_extract_printable_strings_with_min_length(tmp_path):
    test_file = tmp_path / "sample.bin"
    test_file.write_bytes(b"\x00abc\x00abcdef\x00")

    result = extract_printable_strings(str(test_file), min_length=4)

    assert "abc" not in result
    assert "abcdef" in result


def test_file_does_not_exist():
    with pytest.raises(FileNotFoundError):
        get_file_info("missing_file.txt")


def test_path_requires_string():
    with pytest.raises(TypeError):
        get_file_info(123)


def test_hash_unsupported_algorithm(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError):
        calculate_file_hash(str(test_file), "unknown")


def test_extract_strings_min_length_requires_integer(tmp_path):
    test_file = tmp_path / "sample.bin"
    test_file.write_bytes(b"hello")

    with pytest.raises(TypeError):
        extract_printable_strings(str(test_file), min_length="4")


def test_extract_strings_min_length_must_be_positive(tmp_path):
    test_file = tmp_path / "sample.bin"
    test_file.write_bytes(b"hello")

    with pytest.raises(ValueError):
        extract_printable_strings(str(test_file), min_length=0)