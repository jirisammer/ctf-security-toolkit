import json

from rich.panel import Panel
from rich.syntax import Syntax

from ctf_toolkit.core.console import console, print_error, print_info
from ctf_toolkit.core.output import print_key_value_table, print_result
from ctf_toolkit.core.settings import get_setting

from ctf_toolkit.modules.web.jwt_tools import decode_jwt
from ctf_toolkit.modules.web.http_tools import make_http_request, parse_headers


def _print_json_panel(title: str, data: dict) -> None:
    json_text = json.dumps(data, indent=4, ensure_ascii=False)
    syntax = Syntax(json_text, "json", theme="monokai", line_numbers=False)

    console.print()
    console.print(
        Panel(
            syntax,
            title=f"[bold green]{title}[/bold green]",
            border_style="green",
        )
    )


def handle_decode_jwt() -> None:
    token = input("Enter JWT token: ")

    try:
        result = decode_jwt(token)

        _print_json_panel("JWT Header", result["header"])
        _print_json_panel("JWT Payload", result["payload"])

        print_key_value_table(
            "JWT Metadata",
            {
                "Algorithm": result["algorithm"],
                "Token type": result["token_type"],
                "Signature length": result["signature_length"],
                "Signature verified": result["signature_verified"],
                "Note": result["note"],
            },
        )

    except Exception as error:
        print_error(str(error))


def handle_http_request() -> None:
    print_info(
        "Use only with legal CTF labs, your own local server, "
        "or systems where you have permission."
    )

    url = input("Enter URL, for example https://example.com: ")
    method = input("Enter HTTP method, default GET: ").strip()

    if method == "":
        method = "GET"

    headers_text = input(
        "Enter headers, for example User-Agent: CTF Toolkit; Accept: application/json, or leave empty: "
    )

    body = ""

    if method.strip().upper() in ("POST", "PUT", "PATCH"):
        body = input("Enter request body, or leave empty: ")

    try:
        headers = parse_headers(headers_text)

        timeout = int(get_setting("http_timeout_seconds"))
        preview_limit = int(get_setting("http_response_preview_limit"))

        result = make_http_request(
            url=url,
            method=method,
            headers=headers,
            body=body,
            timeout=timeout,
            preview_limit=preview_limit,
        )

        print_key_value_table(
            "HTTP Response",
            {
                "Method": result["method"],
                "Requested URL": result["requested_url"],
                "Final URL": result["final_url"],
                "Status": f"{result['status_code']} {result['reason']}",
                "Content-Type": result["content_type"],
                "Response length": f"{result['response_length']} characters",
                "Elapsed": f"{result['elapsed_seconds']:.3f} seconds",
            },
        )

        print_result("Response Preview", result["response_preview"])

    except Exception as error:
        print_error(str(error))