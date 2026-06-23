import pytest

from ctf_toolkit.modules.encoding.url_tools import encode_url, decode_url


def test_encode_url_simple_text():
    result = encode_url("hello")
    assert result == "hello"


def test_decode_url_simple_text():
    result = decode_url("hello")
    assert result == "hello"


def test_encode_url_with_space():
    result = encode_url("hello world")
    assert result == "hello%20world"


def test_decode_url_with_space():
    result = decode_url("hello%20world")
    assert result == "hello world"


def test_encode_url_ctf_flag():
    result = encode_url("flag{hello_world}")
    assert result == "flag%7Bhello_world%7D"


def test_decode_url_ctf_flag():
    result = decode_url("flag%7Bhello_world%7D")
    assert result == "flag{hello_world}"


def test_encode_url_special_characters():
    result = encode_url("?id=1&admin=true")
    assert result == "%3Fid%3D1%26admin%3Dtrue"


def test_decode_url_special_characters():
    result = decode_url("%3Fid%3D1%26admin%3Dtrue")
    assert result == "?id=1&admin=true"


def test_encode_requires_string():
    with pytest.raises(TypeError):
        encode_url(123)


def test_decode_requires_string():
    with pytest.raises(TypeError):
        decode_url(123)