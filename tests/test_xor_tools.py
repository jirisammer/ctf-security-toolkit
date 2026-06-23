import pytest

from ctf_toolkit.modules.crypto.xor_tools import (
    xor_bytes,
    xor_text_with_key_to_hex,
    xor_hex_with_key_to_text,
    brute_force_single_byte_xor,
)


def test_xor_bytes_with_single_byte_key():
    result = xor_bytes(b"abc", b"\x01")
    assert result == b"`cb"


def test_xor_text_with_key_to_hex():
    result = xor_text_with_key_to_hex("hello", "key")
    assert result == "030015070a"


def test_xor_hex_with_key_to_text():
    result = xor_hex_with_key_to_text("030015070a", "key")
    assert result == "hello"


def test_xor_hex_with_spaces():
    result = xor_hex_with_key_to_text("03 00 15 07 0a", "key")
    assert result == "hello"


def test_xor_hex_with_0x_prefix():
    result = xor_hex_with_key_to_text("0x03 0x00 0x15 0x07 0x0a", "key")
    assert result == "hello"


def test_xor_hex_with_backslash_x_prefix():
    result = xor_hex_with_key_to_text("\\x03\\x00\\x15\\x07\\x0a", "key")
    assert result == "hello"


def test_single_byte_xor_brute_force_contains_original_text():
    encrypted_hex = xor_text_with_key_to_hex("hello", "A")
    results = brute_force_single_byte_xor(encrypted_hex, limit=20)

    decoded_texts = [decoded_text for _, decoded_text, _ in results]

    assert "hello" in decoded_texts


def test_xor_bytes_requires_bytes_data():
    with pytest.raises(TypeError):
        xor_bytes("abc", b"key")


def test_xor_bytes_requires_bytes_key():
    with pytest.raises(TypeError):
        xor_bytes(b"abc", "key")


def test_xor_bytes_key_cannot_be_empty():
    with pytest.raises(ValueError):
        xor_bytes(b"abc", b"")


def test_xor_text_requires_string_text():
    with pytest.raises(TypeError):
        xor_text_with_key_to_hex(123, "key")


def test_xor_text_requires_string_key():
    with pytest.raises(TypeError):
        xor_text_with_key_to_hex("hello", 123)


def test_xor_text_key_cannot_be_empty():
    with pytest.raises(ValueError):
        xor_text_with_key_to_hex("hello", "")


def test_xor_hex_requires_string_hex():
    with pytest.raises(TypeError):
        xor_hex_with_key_to_text(123, "key")


def test_xor_hex_requires_string_key():
    with pytest.raises(TypeError):
        xor_hex_with_key_to_text("030015070a", 123)


def test_xor_hex_key_cannot_be_empty():
    with pytest.raises(ValueError):
        xor_hex_with_key_to_text("030015070a", "")


def test_invalid_hex_input():
    with pytest.raises(ValueError):
        xor_hex_with_key_to_text("zzzz", "key")


def test_brute_force_limit_must_be_positive():
    with pytest.raises(ValueError):
        brute_force_single_byte_xor("030015070a", limit=0)