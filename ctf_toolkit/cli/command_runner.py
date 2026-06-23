import argparse
import json
from typing import Any

from ctf_toolkit.core.console import print_error
from ctf_toolkit.core.output import print_key_value_table, print_list, print_result

from ctf_toolkit.modules.encoding.base64_tools import encode_base64, decode_base64
from ctf_toolkit.modules.encoding.hex_tools import encode_hex, decode_hex
from ctf_toolkit.modules.encoding.url_tools import encode_url, decode_url

from ctf_toolkit.modules.crypto.rot13 import rot13
from ctf_toolkit.modules.crypto.caesar import (
    encrypt_caesar,
    decrypt_caesar,
    brute_force_caesar,
)

from ctf_toolkit.modules.hashing.hash_tools import generate_hash, verify_hash

from ctf_toolkit.modules.detection.input_detector import analyze_input

from ctf_toolkit.modules.extraction.regex_extractor import extract_all_indicators

from ctf_toolkit.modules.web.jwt_tools import decode_jwt

from ctf_toolkit.modules.files.file_analyzer import (
    get_file_info,
    calculate_file_hash,
    extract_printable_strings,
)


CommandResult = dict[str, Any]


def _success_result(title: str, data: Any, display_type: str = "result") -> CommandResult:
    return {
        "success": True,
        "title": title,
        "data": data,
        "display_type": display_type,
    }


def _error_result(message: str) -> CommandResult:
    return {
        "success": False,
        "error": message,
    }


def _print_detection_results(results: list[dict[str, str]]) -> None:
    for index, result in enumerate(results, start=1):
        print_key_value_table(
            f"Detection #{index}",
            {
                "Type": result["type"],
                "Confidence": result["confidence"],
                "Details": result["details"],
            },
        )


def _print_indicator_results(results: dict[str, Any]) -> None:
    found_anything = False

    for key, values in results.items():
        if values:
            found_anything = True
            title = key.replace("_", " ").title()
            print_list(title, values)

    if not found_anything:
        print_result("Extracted Indicators", "No indicators found.")


def _print_rich_result(result: CommandResult) -> None:
    if not result["success"]:
        print_error(result["error"])
        return

    title = result["title"]
    data = result["data"]
    display_type = result.get("display_type", "result")

    if display_type == "result":
        print_result(title, data)

    elif display_type == "list":
        print_list(title, data)

    elif display_type == "detection":
        _print_detection_results(data)

    elif display_type == "indicators":
        _print_indicator_results(data)

    elif display_type == "table":
        print_key_value_table(title, data)

    else:
        print_result(title, data)


def _print_plain_result(result: CommandResult) -> None:
    if not result["success"]:
        print(f"Error: {result['error']}")
        return

    data = result["data"]

    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=4, ensure_ascii=False))
    else:
        print(data)


def _print_json_result(result: CommandResult) -> None:
    output_data = {
        key: value
        for key, value in result.items()
        if key != "display_type"
    }

    print(json.dumps(output_data, indent=4, ensure_ascii=False))


def _print_command_result(result: CommandResult, output_format: str) -> None:
    if output_format == "json":
        _print_json_result(result)

    elif output_format == "plain":
        _print_plain_result(result)

    else:
        _print_rich_result(result)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ctf-toolkit",
        description="CTF Security Toolkit command-line mode",
    )

    parser.add_argument(
        "--output",
        choices=("rich", "plain", "json"),
        default="rich",
        help="Output format. Use json when calling the tool from C#.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
    )

    base64_encode = subparsers.add_parser(
        "base64-encode",
        help="Encode text to Base64",
    )
    base64_encode.add_argument("text")

    base64_decode = subparsers.add_parser(
        "base64-decode",
        help="Decode Base64 text",
    )
    base64_decode.add_argument("text")

    hex_encode = subparsers.add_parser(
        "hex-encode",
        help="Encode text to Hex",
    )
    hex_encode.add_argument("text")

    hex_decode = subparsers.add_parser(
        "hex-decode",
        help="Decode Hex text",
    )
    hex_decode.add_argument("text")

    url_encode = subparsers.add_parser(
        "url-encode",
        help="URL encode text",
    )
    url_encode.add_argument("text")

    url_decode = subparsers.add_parser(
        "url-decode",
        help="URL decode text",
    )
    url_decode.add_argument("text")

    rot13_parser = subparsers.add_parser(
        "rot13",
        help="Apply ROT13 to text",
    )
    rot13_parser.add_argument("text")

    caesar_encrypt = subparsers.add_parser(
        "caesar-encrypt",
        help="Encrypt text using Caesar cipher",
    )
    caesar_encrypt.add_argument("text")
    caesar_encrypt.add_argument("shift", type=int)

    caesar_decrypt = subparsers.add_parser(
        "caesar-decrypt",
        help="Decrypt text using Caesar cipher",
    )
    caesar_decrypt.add_argument("text")
    caesar_decrypt.add_argument("shift", type=int)

    caesar_bruteforce = subparsers.add_parser(
        "caesar-bruteforce",
        help="Brute force Caesar cipher",
    )
    caesar_bruteforce.add_argument("text")

    hash_parser = subparsers.add_parser(
        "hash",
        help="Generate hash from text",
    )
    hash_parser.add_argument("text")
    hash_parser.add_argument("algorithm")

    verify_hash_parser = subparsers.add_parser(
        "verify-hash",
        help="Verify text against expected hash",
    )
    verify_hash_parser.add_argument("text")
    verify_hash_parser.add_argument("expected_hash")
    verify_hash_parser.add_argument("algorithm")

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze input and detect possible encoding/hash type",
    )
    analyze_parser.add_argument("text")

    extract_parser = subparsers.add_parser(
        "extract",
        help="Extract CTF flags, URLs, e-mails, IPs and hashes from text",
    )
    extract_parser.add_argument("text")

    jwt_decode_parser = subparsers.add_parser(
        "jwt-decode",
        help="Decode JWT header and payload without verifying signature",
    )
    jwt_decode_parser.add_argument("token")

    file_info_parser = subparsers.add_parser(
        "file-info",
        help="Show basic file information",
    )
    file_info_parser.add_argument("file_path")

    file_hash_parser = subparsers.add_parser(
        "file-hash",
        help="Calculate file hash",
    )
    file_hash_parser.add_argument("file_path")
    file_hash_parser.add_argument("algorithm")

    file_strings_parser = subparsers.add_parser(
        "file-strings",
        help="Extract printable strings from file",
    )
    file_strings_parser.add_argument("file_path")
    file_strings_parser.add_argument("min_length", type=int, nargs="?", default=4)

    return parser


def execute_command(args: argparse.Namespace) -> CommandResult:
    if args.command == "base64-encode":
        result = encode_base64(args.text)
        return _success_result("Base64 Encoded Result", result)

    if args.command == "base64-decode":
        result = decode_base64(args.text)
        return _success_result("Base64 Decoded Result", result)

    if args.command == "hex-encode":
        result = encode_hex(args.text)
        return _success_result("Hex Encoded Result", result)

    if args.command == "hex-decode":
        result = decode_hex(args.text)
        return _success_result("Hex Decoded Result", result)

    if args.command == "url-encode":
        result = encode_url(args.text)
        return _success_result("URL Encoded Result", result)

    if args.command == "url-decode":
        result = decode_url(args.text)
        return _success_result("URL Decoded Result", result)

    if args.command == "rot13":
        result = rot13(args.text)
        return _success_result("ROT13 Result", result)

    if args.command == "caesar-encrypt":
        result = encrypt_caesar(args.text, args.shift)
        return _success_result("Caesar Encrypted Result", result)

    if args.command == "caesar-decrypt":
        result = decrypt_caesar(args.text, args.shift)
        return _success_result("Caesar Decrypted Result", result)

    if args.command == "caesar-bruteforce":
        results = brute_force_caesar(args.text)

        formatted_results = [
            f"Shift {shift:2}: {decoded_text}"
            for shift, decoded_text in results.items()
        ]

        return _success_result(
            "Caesar Brute Force Results",
            formatted_results,
            display_type="list",
        )

    if args.command == "hash":
        result = generate_hash(args.text, args.algorithm)
        return _success_result("Hash Result", result)

    if args.command == "verify-hash":
        result = verify_hash(
            text=args.text,
            expected_hash=args.expected_hash,
            algorithm=args.algorithm,
        )

        if result:
            message = "Hash matches."
        else:
            message = "Hash does not match."

        return _success_result("Hash Verification", message)

    if args.command == "analyze":
        results = analyze_input(args.text)

        return _success_result(
            "Input Analysis",
            results,
            display_type="detection",
        )

    if args.command == "extract":
        results = extract_all_indicators(args.text)

        return _success_result(
            "Extracted Indicators",
            results,
            display_type="indicators",
        )

    if args.command == "jwt-decode":
        result = decode_jwt(args.token)

        return _success_result(
            "JWT Decoded Result",
            result,
            display_type="table",
        )

    if args.command == "file-info":
        result = get_file_info(args.file_path)

        return _success_result(
            "File Information",
            result,
            display_type="table",
        )

    if args.command == "file-hash":
        result = calculate_file_hash(args.file_path, args.algorithm)

        return _success_result(
            "File Hash",
            result,
        )

    if args.command == "file-strings":
        result = extract_printable_strings(
            args.file_path,
            min_length=args.min_length,
        )

        return _success_result(
            "Extracted Strings From File",
            result,
            display_type="list",
        )

    return _error_result(f"Unknown command: {args.command}")


def run_cli_command(argv: list[str]) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    try:
        result = execute_command(args)
        _print_command_result(result, args.output)

        if result["success"]:
            return 0

        return 1

    except Exception as error:
        result = _error_result(str(error))
        _print_command_result(result, args.output)
        return 1