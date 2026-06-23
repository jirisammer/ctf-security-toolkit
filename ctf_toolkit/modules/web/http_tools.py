from typing import Any

import requests


SUPPORTED_HTTP_METHODS = (
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "HEAD",
    "OPTIONS",
)


def normalize_http_method(method: str) -> str:
    """
    Normalizes and validates HTTP method.
    """
    if not isinstance(method, str):
        raise TypeError("HTTP method must be a string.")

    normalized = method.strip().upper()

    if normalized not in SUPPORTED_HTTP_METHODS:
        raise ValueError(f"Unsupported HTTP method: {method}")

    return normalized


def validate_url(url: str) -> str:
    """
    Validates URL for HTTP requests.
    """
    if not isinstance(url, str):
        raise TypeError("URL must be a string.")

    cleaned_url = url.strip()

    if cleaned_url == "":
        raise ValueError("URL cannot be empty.")

    if not cleaned_url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")

    return cleaned_url


def parse_headers(headers_text: str) -> dict[str, str]:
    """
    Parses headers from text.

    Supported formats:
        User-Agent: CTF Toolkit
        Accept: application/json

    Or one-line format:
        User-Agent: CTF Toolkit; Accept: application/json
    """
    if not isinstance(headers_text, str):
        raise TypeError("Headers text must be a string.")

    cleaned_text = headers_text.strip()

    if cleaned_text == "":
        return {}

    lines = cleaned_text.replace(";", "\n").splitlines()
    headers = {}

    for line in lines:
        cleaned_line = line.strip()

        if cleaned_line == "":
            continue

        if ":" not in cleaned_line:
            raise ValueError(f"Invalid header format: {cleaned_line}")

        name, value = cleaned_line.split(":", 1)

        header_name = name.strip()
        header_value = value.strip()

        if header_name == "":
            raise ValueError("Header name cannot be empty.")

        headers[header_name] = header_value

    return headers


def make_http_request(
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: str = "",
    timeout: int | float = 10,
    preview_limit: int = 1000,
) -> dict[str, Any]:
    """
    Sends an HTTP request and returns basic response information.

    This is intended for legal CTF/lab usage.
    """
    cleaned_url = validate_url(url)
    normalized_method = normalize_http_method(method)

    if headers is not None and not isinstance(headers, dict):
        raise TypeError("Headers must be a dictionary or None.")

    if not isinstance(body, str):
        raise TypeError("Body must be a string.")

    if not isinstance(timeout, (int, float)):
        raise TypeError("Timeout must be a number.")

    if timeout <= 0:
        raise ValueError("Timeout must be greater than zero.")

    if not isinstance(preview_limit, int):
        raise TypeError("Preview limit must be an integer.")

    if preview_limit <= 0:
        raise ValueError("Preview limit must be greater than zero.")

    request_headers = headers if headers is not None else {}

    request_body = None
    if normalized_method in ("POST", "PUT", "PATCH"):
        request_body = body

    try:
        response = requests.request(
            method=normalized_method,
            url=cleaned_url,
            headers=request_headers,
            data=request_body,
            timeout=timeout,
            allow_redirects=True,
        )

    except requests.RequestException as error:
        raise ConnectionError(f"HTTP request failed: {error}")

    response_text = response.text

    return {
        "method": normalized_method,
        "requested_url": cleaned_url,
        "final_url": response.url,
        "status_code": response.status_code,
        "reason": response.reason,
        "content_type": response.headers.get("Content-Type", "unknown"),
        "response_headers": dict(response.headers),
        "response_length": len(response_text),
        "response_preview": response_text[:preview_limit],
        "elapsed_seconds": response.elapsed.total_seconds(),
    }