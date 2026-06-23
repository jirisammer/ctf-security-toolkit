import pytest

from ctf_toolkit.modules.hashing.hash_tools import (
    generate_hash,
    verify_hash,
    list_supported_hashes,
    normalize_algorithm,
)


def test_generate_md5_hash():
    result = generate_hash("hello", "md5")
    assert result == "5d41402abc4b2a76b9719d911017c592"


def test_generate_sha1_hash():
    result = generate_hash("hello", "sha1")
    assert result == "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"


def test_generate_sha256_hash():
    result = generate_hash("hello", "sha256")
    assert result == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_generate_sha512_hash_length():
    result = generate_hash("hello", "sha512")
    assert len(result) == 128


def test_normalize_algorithm_uppercase():
    result = normalize_algorithm("SHA256")
    assert result == "sha256"


def test_normalize_algorithm_with_dash():
    result = normalize_algorithm("sha-256")
    assert result == "sha256"


def test_normalize_algorithm_with_underscore():
    result = normalize_algorithm("sha_256")
    assert result == "sha256"


def test_verify_hash_true():
    result = verify_hash(
        "hello",
        "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        "sha256",
    )

    assert result is True


def test_verify_hash_false():
    result = verify_hash("hello", "wronghash", "sha256")
    assert result is False


def test_list_supported_hashes_contains_sha256():
    result = list_supported_hashes()
    assert "sha256" in result


def test_unsupported_hash_algorithm():
    with pytest.raises(ValueError):
        generate_hash("hello", "unknown")


def test_generate_hash_requires_string_text():
    with pytest.raises(TypeError):
        generate_hash(123, "sha256")


def test_algorithm_requires_string():
    with pytest.raises(TypeError):
        generate_hash("hello", 123)


def test_verify_hash_expected_hash_requires_string():
    with pytest.raises(TypeError):
        verify_hash("hello", 123, "sha256")