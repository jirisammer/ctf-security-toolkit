import pytest

from ctf_toolkit.modules.web.jwt_tools import (
    decode_jwt,
    split_jwt,
    decode_jwt_part_to_json,
)


VALID_JWT = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9."
    "TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"
)


def test_split_jwt():
    header, payload, signature = split_jwt(VALID_JWT)

    assert header == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    assert payload == "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9"
    assert signature == "TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"


def test_decode_jwt_header():
    result = decode_jwt(VALID_JWT)

    assert result["header"]["alg"] == "HS256"
    assert result["header"]["typ"] == "JWT"


def test_decode_jwt_payload():
    result = decode_jwt(VALID_JWT)

    assert result["payload"]["sub"] == "1234567890"
    assert result["payload"]["name"] == "John Doe"
    assert result["payload"]["admin"] is True


def test_decode_jwt_metadata():
    result = decode_jwt(VALID_JWT)

    assert result["algorithm"] == "HS256"
    assert result["token_type"] == "JWT"
    assert result["signature_verified"] is False


def test_decode_jwt_part_to_json():
    result = decode_jwt_part_to_json("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")

    assert result["alg"] == "HS256"
    assert result["typ"] == "JWT"


def test_jwt_must_have_three_parts():
    with pytest.raises(ValueError):
        decode_jwt("abc.def")


def test_jwt_parts_cannot_be_empty():
    with pytest.raises(ValueError):
        decode_jwt("abc..def")


def test_jwt_requires_string():
    with pytest.raises(TypeError):
        decode_jwt(123)


def test_invalid_base64url_part():
    with pytest.raises(ValueError):
        decode_jwt("###.abc.def")


def test_invalid_json_part():
    with pytest.raises(ValueError):
        decode_jwt("YWJj.YWJj.signature")