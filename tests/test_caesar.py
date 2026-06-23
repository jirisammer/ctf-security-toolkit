import pytest

from ctf_toolkit.modules.crypto.caesar import (
    encrypt_caesar,
    decrypt_caesar,
    brute_force_caesar,
)


def test_encrypt_caesar_hello_shift_3():
    result = encrypt_caesar("hello", 3)
    assert result == "khoor"


def test_decrypt_caesar_hello_shift_3():
    result = decrypt_caesar("khoor", 3)
    assert result == "hello"


def test_encrypt_caesar_uppercase():
    result = encrypt_caesar("HELLO", 3)
    assert result == "KHOOR"


def test_encrypt_caesar_mixed_text():
    result = encrypt_caesar("flag{hello_world}", 13)
    assert result == "synt{uryyb_jbeyq}"


def test_caesar_preserves_numbers_and_symbols():
    result = encrypt_caesar("abc123!?", 3)
    assert result == "def123!?"


def test_encrypt_caesar_negative_shift():
    result = encrypt_caesar("def", -3)
    assert result == "abc"


def test_encrypt_caesar_large_shift():
    result = encrypt_caesar("abc", 29)
    assert result == "def"


def test_brute_force_caesar_contains_original_text():
    results = brute_force_caesar("khoor")
    assert results[3] == "hello"


def test_encrypt_requires_string():
    with pytest.raises(TypeError):
        encrypt_caesar(123, 3)


def test_decrypt_requires_string():
    with pytest.raises(TypeError):
        decrypt_caesar(123, 3)


def test_encrypt_requires_integer_shift():
    with pytest.raises(TypeError):
        encrypt_caesar("hello", "3")


def test_decrypt_requires_integer_shift():
    with pytest.raises(TypeError):
        decrypt_caesar("hello", "3")


def test_brute_force_requires_string():
    with pytest.raises(TypeError):
        brute_force_caesar(123)