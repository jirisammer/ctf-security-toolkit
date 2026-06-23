import pytest

from ctf_toolkit.modules.encoding.hex_tools import encode_hex, decode_hex


def test_encode_hex_hello():
    result = encode_hex("hello")
    assert result == "68656c6c6f"


def test_decode_hex_hello():
    result = decode_hex("68656c6c6f")
    assert result == "hello"


def test_encode_hex_czech_text():
    result = encode_hex("ahoj")
    assert result == "61686f6a"


def test_decode_hex_czech_text():
    result = decode_hex("61686f6a")
    assert result == "ahoj"


def test_decode_hex_with_spaces():
    result = decode_hex("68 65 6c 6c 6f")
    assert result == "hello"


def test_decode_hex_with_0x_prefix():
    result = decode_hex("0x68 0x65 0x6c 0x6c 0x6f")
    assert result == "hello"


def test_decode_hex_with_backslash_x_prefix():
    result = decode_hex("\\x68\\x65\\x6c\\x6c\\x6f")
    assert result == "hello"


def test_invalid_hex_input():
    with pytest.raises(ValueError):
        decode_hex("zzzz")


def test_hex_odd_number_of_characters():
    with pytest.raises(ValueError):
        decode_hex("abc")


def test_encode_requires_string():
    with pytest.raises(TypeError):
        encode_hex(123)


def test_decode_requires_string():
    with pytest.raises(TypeError):
        decode_hex(123)