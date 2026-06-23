import base64
import binascii
import re
from urllib.parse import unquote


HEX_PATTERN = re.compile(r"^[0-9a-fA-F]+$")
BASE64_PATTERN = re.compile(r"^[A-Za-z0-9+/]+={0,2}$")
BASE64_URL_PATTERN = re.compile(r"^[A-Za-z0-9_-]+={0,2}$")
URL_ENCODED_PATTERN = re.compile(r"%[0-9a-fA-F]{2}")

HASH_LENGTHS = {
    32: "MD5",
    40: "SHA1",
    56: "SHA224",
    64: "SHA256",
    96: "SHA384",
    128: "SHA512",
}


def _is_printable_text(text: str) -> bool:
    if text == "":
        return False

    printable_count = 0

    for char in text:
        if char.isprintable() or char in "\n\r\t":
            printable_count += 1

    return printable_count / len(text) >= 0.85


def _clean_hex(text: str) -> str:
    return (
        text.strip()
        .replace(" ", "")
        .replace("\n", "")
        .replace("\t", "")
        .replace("0x", "")
        .replace("0X", "")
        .replace("\\x", "")
        .replace("\\X", "")
    )


def detect_hash(text: str) -> dict[str, str] | None:
    cleaned = text.strip()

    if len(cleaned) not in HASH_LENGTHS:
        return None

    if not HEX_PATTERN.fullmatch(cleaned):
        return None

    return {
        "type": "Hash",
        "confidence": "high",
        "details": f"Looks like a {HASH_LENGTHS[len(cleaned)]} hash.",
    }


def detect_hex(text: str) -> dict[str, str] | None:
    cleaned = _clean_hex(text)

    if cleaned == "":
        return None

    if len(cleaned) % 2 != 0:
        return None

    if not HEX_PATTERN.fullmatch(cleaned):
        return None

    try:
        decoded_bytes = bytes.fromhex(cleaned)
        decoded_text = decoded_bytes.decode("utf-8", errors="replace")

    except ValueError:
        return None

    if not _is_printable_text(decoded_text):
        return {
            "type": "Hex",
            "confidence": "medium",
            "details": "Looks like hex data, but decoded output may not be readable text.",
        }

    preview = decoded_text[:80]

    return {
        "type": "Hex",
        "confidence": "high",
        "details": f"Looks like hex. Decoded preview: {preview}",
    }


def detect_base64(text: str) -> dict[str, str] | None:
    cleaned = text.strip()

    if cleaned == "":
        return None

    if len(cleaned) % 4 != 0:
        return None

    if not BASE64_PATTERN.fullmatch(cleaned):
        return None

    try:
        decoded_bytes = base64.b64decode(cleaned, validate=True)
        decoded_text = decoded_bytes.decode("utf-8", errors="replace")

    except (binascii.Error, UnicodeDecodeError):
        return None

    if not _is_printable_text(decoded_text):
        return {
            "type": "Base64",
            "confidence": "medium",
            "details": "Looks like Base64, but decoded output may not be readable text.",
        }

    preview = decoded_text[:80]

    return {
        "type": "Base64",
        "confidence": "high",
        "details": f"Looks like Base64. Decoded preview: {preview}",
    }


def detect_url_encoding(text: str) -> dict[str, str] | None:
    cleaned = text.strip()

    if not URL_ENCODED_PATTERN.search(cleaned):
        return None

    decoded = unquote(cleaned)

    if decoded == cleaned:
        return None

    preview = decoded[:80]

    return {
        "type": "URL Encoding",
        "confidence": "high",
        "details": f"Looks like URL encoded text. Decoded preview: {preview}",
    }


def detect_jwt(text: str) -> dict[str, str] | None:
    cleaned = text.strip()
    parts = cleaned.split(".")

    if len(parts) != 3:
        return None

    header, payload, signature = parts

    if header == "" or payload == "" or signature == "":
        return None

    if not BASE64_URL_PATTERN.fullmatch(header):
        return None

    if not BASE64_URL_PATTERN.fullmatch(payload):
        return None

    if not BASE64_URL_PATTERN.fullmatch(signature):
        return None

    return {
        "type": "JWT",
        "confidence": "medium",
        "details": "Looks like a JSON Web Token because it has three Base64URL-like parts separated by dots.",
    }


def analyze_input(text: str) -> list[dict[str, str]]:
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    if text.strip() == "":
        return [
            {
                "type": "Empty input",
                "confidence": "high",
                "details": "Input is empty.",
            }
        ]

    detectors = [
        detect_hash,
        detect_url_encoding,
        detect_jwt,
        detect_base64,
        detect_hex,
    ]

    results = []

    for detector in detectors:
        result = detector(text)

        if result is not None:
            results.append(result)

    if not results:
        results.append(
            {
                "type": "Unknown / Plain text",
                "confidence": "low",
                "details": "No known encoding or hash pattern was detected.",
            }
        )

    return results