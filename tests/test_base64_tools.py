import pytest

from ctf_toolkit.modules.encoding.base64_tools import encode_base64, decode_base64


def test_encode_base64_hello():
    result = encode_base64("hello")
    assert result == "aGVsbG8="


def test_decode_base64_hello():
    result = decode_base64("aGVsbG8=")
    assert result == "hello"


def test_encode_base64_czech_text():
    result = encode_base64("ahoj")
    assert result == "YWhvag=="


def test_decode_base64_czech_text():
    result = decode_base64("YWhvag==")
    assert result == "ahoj"


def test_invalid_base64_input():
    with pytest.raises(ValueError):
        decode_base64("this is not valid base64!!!")


def test_encode_requires_string():
    with pytest.raises(TypeError):
        encode_base64(123)


def test_decode_requires_string():
    with pytest.raises(TypeError):
        decode_base64(123)