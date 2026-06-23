from typing import Any

from ctf_toolkit.core.console import print_error
from ctf_toolkit.core.output import print_list, print_result, print_section

from ctf_toolkit.modules.extraction.regex_extractor import (
    find_ctf_flags,
    extract_all_indicators,
    extract_all_indicators_from_file,
)


def _format_title(key: str) -> str:
    return key.replace("_", " ").title()


def _print_indicator_results(title: str, results: dict[str, Any]) -> None:
    print_section(title)

    found_anything = False

    for key, values in results.items():
        if values:
            found_anything = True
            print_list(_format_title(key), values)

    if not found_anything:
        print_result(title, "No indicators found.")


def handle_find_ctf_flags_in_text() -> None:
    text = input("Enter text to search for CTF flags: ")

    try:
        flags = find_ctf_flags(text)

        if not flags:
            print_result("CTF Flags", "No CTF flags found.")
            return

        print_list("CTF Flags", flags)

    except Exception as error:
        print_error(str(error))


def handle_extract_indicators_from_text() -> None:
    text = input("Enter text to analyze: ")

    try:
        results = extract_all_indicators(text)
        _print_indicator_results("Extracted Indicators From Text", results)

    except Exception as error:
        print_error(str(error))


def handle_extract_indicators_from_file() -> None:
    file_path = input("Enter file path: ")
    min_length_text = input("Enter minimum string length, default is 4: ").strip()

    try:
        if min_length_text == "":
            min_length = 4
        else:
            min_length = int(min_length_text)

        results = extract_all_indicators_from_file(
            file_path=file_path,
            min_string_length=min_length,
        )

        _print_indicator_results("Extracted Indicators From File", results)

    except ValueError:
        print_error("Minimum string length must be a valid positive number.")

    except Exception as error:
        print_error(str(error))