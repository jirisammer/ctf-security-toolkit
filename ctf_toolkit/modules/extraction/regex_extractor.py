import re
from pathlib import Path
from typing import Any

from ctf_toolkit.modules.files.file_analyzer import extract_printable_strings


FLAG_PATTERN = re.compile(
    r"\b(?:flag|ctf|picoctf|htb|thm)\{[^}\r\n]{1,200}\}",
    re.IGNORECASE,
)

URL_PATTERN = re.compile(
    r"\bhttps?://[^\s<>'\"]+",
    re.IGNORECASE,
)

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

IPV4_PATTERN = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
)

HASH_PATTERNS = {
    "md5_hashes": re.compile(r"\b[a-fA-F0-9]{32}\b"),
    "sha1_hashes": re.compile(r"\b[a-fA-F0-9]{40}\b"),
    "sha256_hashes": re.compile(r"\b[a-fA-F0-9]{64}\b"),
    "sha512_hashes": re.compile(r"\b[a-fA-F0-9]{128}\b"),
}


def _ensure_text(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("Input must be a string.")

    return value


def _unique_preserve_order(values: list[str]) -> list[str]:
    seen = set()
    unique_values = []

    for value in values:
        if value not in seen:
            seen.add(value)
            unique_values.append(value)

    return unique_values


def _clean_url(url: str) -> str:
    return url.rstrip(".,);]}>\"'")


def find_ctf_flags(text: str) -> list[str]:
    """
    Finds common CTF flag formats.

    Examples:
        flag{example}
        ctf{example}
        picoCTF{example}
        HTB{example}
        THM{example}
    """
    text = _ensure_text(text)

    flags = FLAG_PATTERN.findall(text)

    return _unique_preserve_order(flags)


def extract_urls(text: str) -> list[str]:
    """
    Extracts HTTP and HTTPS URLs from text.
    """
    text = _ensure_text(text)

    urls = [_clean_url(url) for url in URL_PATTERN.findall(text)]

    return _unique_preserve_order(urls)


def extract_emails(text: str) -> list[str]:
    """
    Extracts e-mail addresses from text.
    """
    text = _ensure_text(text)

    emails = EMAIL_PATTERN.findall(text)

    return _unique_preserve_order(emails)


def extract_ipv4_addresses(text: str) -> list[str]:
    """
    Extracts valid IPv4 addresses from text.
    """
    text = _ensure_text(text)

    addresses = IPV4_PATTERN.findall(text)

    return _unique_preserve_order(addresses)


def extract_hashes(text: str) -> dict[str, list[str]]:
    """
    Extracts common hash formats from text.
    """
    text = _ensure_text(text)

    results = {}

    for hash_type, pattern in HASH_PATTERNS.items():
        matches = pattern.findall(text)
        results[hash_type] = _unique_preserve_order(matches)

    return results


def extract_all_indicators(text: str) -> dict[str, Any]:
    """
    Extracts common CTF/security indicators from text.
    """
    text = _ensure_text(text)

    hash_results = extract_hashes(text)

    return {
        "ctf_flags": find_ctf_flags(text),
        "urls": extract_urls(text),
        "emails": extract_emails(text),
        "ipv4_addresses": extract_ipv4_addresses(text),
        "md5_hashes": hash_results["md5_hashes"],
        "sha1_hashes": hash_results["sha1_hashes"],
        "sha256_hashes": hash_results["sha256_hashes"],
        "sha512_hashes": hash_results["sha512_hashes"],
    }


def extract_all_indicators_from_file(
    file_path: str,
    min_string_length: int = 4,
) -> dict[str, Any]:
    """
    Extracts printable strings from a file and then extracts indicators from them.
    """
    if not isinstance(file_path, str):
        raise TypeError("File path must be a string.")

    if not isinstance(min_string_length, int):
        raise TypeError("Minimum string length must be an integer.")

    if min_string_length <= 0:
        raise ValueError("Minimum string length must be greater than zero.")

    path = Path(file_path.strip().strip('"').strip("'"))

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    printable_strings = extract_printable_strings(
        str(path),
        min_length=min_string_length,
    )

    joined_text = "\n".join(printable_strings)

    return extract_all_indicators(joined_text)