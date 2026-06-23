import pytest

from ctf_toolkit.modules.crypto.rot13 import rot13


def test_rot13_hello():
    result = rot13("hello")
    assert result == "uryyb"


def test_rot13_back_to_original():
    encoded = rot13("hello")
    decoded = rot13(encoded)

    assert decoded == "hello"


def test_rot13_uppercase():
    result = rot13("HELLO")
    assert result == "URYYB"


def test_rot13_mixed_text():
    result = rot13("flag{hello_world}")
    assert result == "synt{uryyb_jbeyq}"


def test_rot13_preserves_numbers_and_symbols():
    result = rot13("abc123!?")
    assert result == "nop123!?"


def test_rot13_requires_string():
    with pytest.raises(TypeError):
        rot13(123)