from ctf_toolkit.core.console import print_error, print_success
from ctf_toolkit.core.output import print_result, print_list

from ctf_toolkit.modules.hashing.hash_tools import (
    generate_hash,
    verify_hash,
    list_supported_hashes,
)


def handle_generate_hash() -> None:
    text = input("Enter text to hash: ")
    algorithm = input("Enter algorithm, for example md5, sha1, sha256, sha512: ")

    try:
        result = generate_hash(text, algorithm)
        print_result("Hash Result", result)

    except Exception as error:
        print_error(str(error))


def handle_verify_hash() -> None:
    text = input("Enter original text: ")
    expected_hash = input("Enter expected hash: ")
    algorithm = input("Enter algorithm, for example md5, sha1, sha256, sha512: ")

    try:
        result = verify_hash(text, expected_hash, algorithm)

        if result:
            print_success("Hash matches.")
        else:
            print_error("Hash does not match.")

    except Exception as error:
        print_error(str(error))


def handle_show_supported_hashes() -> None:
    try:
        algorithms = list_supported_hashes()
        print_list("Supported Hash Algorithms", algorithms)

    except Exception as error:
        print_error(str(error))