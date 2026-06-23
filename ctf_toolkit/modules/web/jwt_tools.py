import base64
import json
import re
from typing import Any


BASE64URL_PATTERN = re.compile(r"^[A-Za-z0-9_-]+={0,2}$")


def _add_base64_padding(value: str) -> str:
    """
    Adds missing Base64 padding if needed.

    JWT uses Base64URL and often removes '=' padding.
    """
    missing_padding = len(value) % 4

    if missing_padding == 0:
        return value

    return value + ("=" * (4 - missing_padding))


def _decode_base64url_to_bytes(value: str) -> bytes:
    """
    Decodes one Base64URL JWT part into bytes.
    """
    if not isinstance(value, str):
        raise TypeError("JWT part must be a string.")

    cleaned = value.strip()

    if cleaned == "":
        raise ValueError("JWT part cannot be empty.")

    if not BASE64URL_PATTERN.fullmatch(cleaned):
        raise ValueError("JWT part contains invalid Base64URL characters.")

    padded_value = _add_base64_padding(cleaned)

    try:
        return base64.urlsafe_b64decode(padded_value.encode("utf-8"))

    except Exception:
        raise ValueError("Invalid Base64URL JWT part.")


def decode_jwt_part_to_text(value: str) -> str:
    """
    Decodes one JWT part into UTF-8 text.
    """
    decoded_bytes = _decode_base64url_to_bytes(value)

    try:
        return decoded_bytes.decode("utf-8")

    except UnicodeDecodeError:
        raise ValueError("Decoded JWT part is not valid UTF-8 text.")


def decode_jwt_part_to_json(value: str) -> dict[str, Any]:
    """
    Decodes one JWT part into JSON dictionary.
    """
    decoded_text = decode_jwt_part_to_text(value)

    try:
        decoded_json = json.loads(decoded_text)

    except json.JSONDecodeError:
        raise ValueError("Decoded JWT part is not valid JSON.")

    if not isinstance(decoded_json, dict):
        raise ValueError("Decoded JWT part must be a JSON object.")

    return decoded_json


def split_jwt(token: str) -> tuple[str, str, str]:
    """
    Splits JWT into header, payload and signature.
    """
    if not isinstance(token, str):
        raise TypeError("JWT token must be a string.")

    cleaned = token.strip()
    parts = cleaned.split(".")

    if len(parts) != 3:
        raise ValueError("JWT must have exactly three parts: header.payload.signature")

    header, payload, signature = parts

    if header == "" or payload == "" or signature == "":
        raise ValueError("JWT header, payload and signature cannot be empty.")

    return header, payload, signature


def decode_jwt(token: str) -> dict[str, Any]:
    """
    Decodes JWT header and payload.

    Important:
    This function only decodes the token.
    It does not verify the signature.
    """
    header_part, payload_part, signature_part = split_jwt(token)

    header = decode_jwt_part_to_json(header_part)
    payload = decode_jwt_part_to_json(payload_part)

    return {
        "header": header,
        "payload": payload,
        "signature": signature_part,
        "signature_length": len(signature_part),
        "algorithm": header.get("alg", "unknown"),
        "token_type": header.get("typ", "unknown"),
        "signature_verified": False,
        "note": "JWT was decoded only. Signature was not verified.",
    }