from ctf_toolkit.core.console import print_error
from ctf_toolkit.core.output import print_key_value_table, print_list, print_result

from ctf_toolkit.modules.files.file_analyzer import (
    get_file_info,
    calculate_file_hash,
    extract_printable_strings,
)


def handle_file_info() -> None:
    file_path = input("Enter file path: ")

    try:
        info = get_file_info(file_path)
        print_key_value_table("File Information", info)

    except Exception as error:
        print_error(str(error))


def handle_file_hash() -> None:
    file_path = input("Enter file path: ")
    algorithm = input("Enter algorithm, for example md5, sha1, sha256, sha512: ")

    try:
        result = calculate_file_hash(file_path, algorithm)
        print_result("File Hash", result)

    except Exception as error:
        print_error(str(error))


def handle_extract_strings_from_file() -> None:
    file_path = input("Enter file path: ")
    min_length_text = input("Enter minimum string length, default is 4: ")

    try:
        if min_length_text.strip() == "":
            min_length = 4
        else:
            min_length = int(min_length_text)

        strings = extract_printable_strings(file_path, min_length)

        if not strings:
            print_result("Extracted Strings", "No printable strings found.")
            return

        print_list("Extracted Strings From File", strings)

    except ValueError:
        print_error("Minimum length must be a number.")

    except Exception as error:
        print_error(str(error))