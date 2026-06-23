import pytest

from ctf_toolkit.modules.web import http_tools
from ctf_toolkit.modules.web.http_tools import (
    normalize_http_method,
    validate_url,
    parse_headers,
    make_http_request,
)


class FakeElapsed:
    def total_seconds(self):
        return 0.123


class FakeResponse:
    status_code = 200
    reason = "OK"
    url = "https://example.com/final"
    text = "hello from test server"
    headers = {
        "Content-Type": "text/plain",
        "Server": "FakeServer",
    }
    elapsed = FakeElapsed()


def test_normalize_http_method_get():
    result = normalize_http_method("get")
    assert result == "GET"


def test_normalize_http_method_post_with_spaces():
    result = normalize_http_method(" post ")
    assert result == "POST"


def test_unsupported_http_method():
    with pytest.raises(ValueError):
        normalize_http_method("INVALID")


def test_method_requires_string():
    with pytest.raises(TypeError):
        normalize_http_method(123)


def test_validate_url_https():
    result = validate_url("https://example.com")
    assert result == "https://example.com"


def test_validate_url_requires_http_or_https():
    with pytest.raises(ValueError):
        validate_url("ftp://example.com")


def test_validate_url_cannot_be_empty():
    with pytest.raises(ValueError):
        validate_url("")


def test_validate_url_requires_string():
    with pytest.raises(TypeError):
        validate_url(123)


def test_parse_headers_empty():
    result = parse_headers("")
    assert result == {}


def test_parse_headers_multiline():
    result = parse_headers("User-Agent: CTF Toolkit\nAccept: application/json")

    assert result["User-Agent"] == "CTF Toolkit"
    assert result["Accept"] == "application/json"


def test_parse_headers_semicolon_format():
    result = parse_headers("User-Agent: CTF Toolkit; Accept: application/json")

    assert result["User-Agent"] == "CTF Toolkit"
    assert result["Accept"] == "application/json"


def test_parse_headers_invalid_format():
    with pytest.raises(ValueError):
        parse_headers("InvalidHeaderWithoutColon")


def test_make_http_request_get(monkeypatch):
    def fake_request(method, url, headers, data, timeout, allow_redirects):
        assert method == "GET"
        assert url == "https://example.com"
        assert headers == {"User-Agent": "Test"}
        assert data is None
        assert timeout == 10
        assert allow_redirects is True

        return FakeResponse()

    monkeypatch.setattr(http_tools.requests, "request", fake_request)

    result = make_http_request(
        url="https://example.com",
        method="GET",
        headers={"User-Agent": "Test"},
    )

    assert result["method"] == "GET"
    assert result["requested_url"] == "https://example.com"
    assert result["final_url"] == "https://example.com/final"
    assert result["status_code"] == 200
    assert result["reason"] == "OK"
    assert result["content_type"] == "text/plain"
    assert result["response_preview"] == "hello from test server"


def test_make_http_request_post(monkeypatch):
    def fake_request(method, url, headers, data, timeout, allow_redirects):
        assert method == "POST"
        assert data == "name=test"

        return FakeResponse()

    monkeypatch.setattr(http_tools.requests, "request", fake_request)

    result = make_http_request(
        url="https://example.com",
        method="POST",
        headers={},
        body="name=test",
    )

    assert result["method"] == "POST"
    assert result["status_code"] == 200


def test_make_http_request_timeout_must_be_positive():
    with pytest.raises(ValueError):
        make_http_request("https://example.com", timeout=0)


def test_make_http_request_body_requires_string():
    with pytest.raises(TypeError):
        make_http_request("https://example.com", body=123)