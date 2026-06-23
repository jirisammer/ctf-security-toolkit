from ctf_toolkit.core.console import print_error
from ctf_toolkit.core.output import print_result

from ctf_toolkit.modules.encoding.base64_tools import encode_base64, decode_base64
from ctf_toolkit.modules.encoding.hex_tools import encode_hex, decode_hex
from ctf_toolkit.modules.encoding.url_tools import encode_url, decode_url


def handle_base64_encode() -> None:
    text = input("Enter text to encode: ")

    try:
        result = encode_base64(text)
        print_result("Base64 Encoded Result", result)

    except Exception as error:
        print_error(str(error))


def handle_base64_decode() -> None:
    encoded_text = input("Enter Base64 text to decode: ")

    try:
        result = decode_base64(encoded_text)
        print_result("Base64 Decoded Result", result)

    except Exception as error:
        print_error(str(error))


def handle_hex_encode() -> None:
    text = input("Enter text to encode: ")

    try:
        result = encode_hex(text)
        print_result("Hex Encoded Result", result)

    except Exception as error:
        print_error(str(error))


def handle_hex_decode() -> None:
    hex_text = input("Enter Hex text to decode: ")

    try:
        result = decode_hex(hex_text)
        print_result("Hex Decoded Result", result)

    except Exception as error:
        print_error(str(error))


def handle_url_encode() -> None:
    text = input("Enter text to URL encode: ")

    try:
        result = encode_url(text)
        print_result("URL Encoded Result", result)

    except Exception as error:
        print_error(str(error))


def handle_url_decode() -> None:
    encoded_text = input("Enter URL encoded text to decode: ")

    try:
        result = decode_url(encoded_text)
        print_result("URL Decoded Result", result)

    except Exception as error:
        print_error(str(error))