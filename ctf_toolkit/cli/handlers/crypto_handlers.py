from ctf_toolkit.core.console import print_error
from ctf_toolkit.core.output import print_result, print_list

from ctf_toolkit.modules.crypto.rot13 import rot13
from ctf_toolkit.modules.crypto.caesar import (
    encrypt_caesar,
    decrypt_caesar,
    brute_force_caesar,
)
from ctf_toolkit.modules.crypto.xor_tools import (
    xor_text_with_key_to_hex,
    xor_hex_with_key_to_text,
    brute_force_single_byte_xor,
)


def handle_rot13() -> None:
    text = input("Enter text for ROT13: ")

    try:
        result = rot13(text)
        print_result("ROT13 Result", result)

    except Exception as error:
        print_error(str(error))


def handle_caesar_encrypt() -> None:
    text = input("Enter text to encrypt: ")
    shift_text = input("Enter shift number: ")

    try:
        shift = int(shift_text)

    except ValueError:
        print_error("Shift must be a number.")
        return

    try:
        result = encrypt_caesar(text, shift)
        print_result("Caesar Encrypted Result", result)

    except Exception as error:
        print_error(str(error))


def handle_caesar_decrypt() -> None:
    text = input("Enter text to decrypt: ")
    shift_text = input("Enter shift number: ")

    try:
        shift = int(shift_text)

    except ValueError:
        print_error("Shift must be a number.")
        return

    try:
        result = decrypt_caesar(text, shift)
        print_result("Caesar Decrypted Result", result)

    except Exception as error:
        print_error(str(error))


def handle_caesar_brute_force() -> None:
    text = input("Enter Caesar encrypted text: ")

    try:
        results = brute_force_caesar(text)

        formatted_results = []

        for shift, decoded_text in results.items():
            formatted_results.append(f"Shift {shift:2}: {decoded_text}")

        print_list("Caesar Brute Force Results", formatted_results)

    except Exception as error:
        print_error(str(error))


def handle_xor_text_with_key_to_hex() -> None:
    text = input("Enter text: ")
    key = input("Enter key: ")

    try:
        result = xor_text_with_key_to_hex(text, key)
        print_result("XOR Hex Result", result)

    except Exception as error:
        print_error(str(error))


def handle_xor_hex_with_key_to_text() -> None:
    hex_text = input("Enter hex text: ")
    key = input("Enter key: ")

    try:
        result = xor_hex_with_key_to_text(hex_text, key)
        print_result("XOR Decoded Text", result)

    except Exception as error:
        print_error(str(error))


def handle_single_byte_xor_brute_force() -> None:
    hex_text = input("Enter XOR encrypted hex text: ")

    try:
        results = brute_force_single_byte_xor(hex_text)

        formatted_results = []

        for key, decoded_text, score in results:
            printable_key = chr(key) if chr(key).isprintable() else "non-printable"
            formatted_results.append(
                f"Key {key:3} ({printable_key}) | Score {score:3} | {decoded_text}"
            )

        print_list("Best Single-byte XOR Candidates", formatted_results)

    except Exception as error:
        print_error(str(error))