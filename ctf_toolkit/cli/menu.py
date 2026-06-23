from collections.abc import Callable

from rich.panel import Panel
from rich.table import Table

from ctf_toolkit.core.console import console, print_error, print_success

from ctf_toolkit.cli.handlers.encoding_handlers import (
    handle_base64_encode,
    handle_base64_decode,
    handle_hex_encode,
    handle_hex_decode,
    handle_url_encode,
    handle_url_decode,
)

from ctf_toolkit.cli.handlers.crypto_handlers import (
    handle_rot13,
    handle_caesar_encrypt,
    handle_caesar_decrypt,
    handle_caesar_brute_force,
    handle_xor_text_with_key_to_hex,
    handle_xor_hex_with_key_to_text,
    handle_single_byte_xor_brute_force,
)

from ctf_toolkit.cli.handlers.hashing_handlers import (
    handle_generate_hash,
    handle_verify_hash,
    handle_show_supported_hashes,
)

from ctf_toolkit.cli.handlers.file_handlers import (
    handle_file_info,
    handle_file_hash,
    handle_extract_strings_from_file,
)

from ctf_toolkit.cli.handlers.detection_handlers import handle_analyze_input

from ctf_toolkit.cli.handlers.web_handlers import handle_decode_jwt, handle_http_request

from ctf_toolkit.cli.handlers.history_handlers import (
    handle_show_history,
    handle_clear_history,
)

from ctf_toolkit.cli.handlers.reporting_handlers import (
    handle_export_history_to_txt,
    handle_export_history_to_json,
)

from ctf_toolkit.cli.handlers.settings_handlers import (
    handle_show_settings,
    handle_update_setting,
    handle_reset_settings,
)

from ctf_toolkit.cli.handlers.extraction_handlers import (
    handle_find_ctf_flags_in_text,
    handle_extract_indicators_from_text,
    handle_extract_indicators_from_file,
)


MenuAction = Callable[[], None]
MenuOptions = dict[str, tuple[str, MenuAction]]
CategoryOptions = dict[str, tuple[str, MenuOptions]]


ENCODING_MENU: MenuOptions = {
    "1": ("Base64 Encode", handle_base64_encode),
    "2": ("Base64 Decode", handle_base64_decode),
    "3": ("Hex Encode", handle_hex_encode),
    "4": ("Hex Decode", handle_hex_decode),
    "5": ("URL Encode", handle_url_encode),
    "6": ("URL Decode", handle_url_decode),
}


CRYPTO_MENU: MenuOptions = {
    "1": ("ROT13", handle_rot13),
    "2": ("Caesar Encrypt", handle_caesar_encrypt),
    "3": ("Caesar Decrypt", handle_caesar_decrypt),
    "4": ("Caesar Brute Force", handle_caesar_brute_force),
    "5": ("XOR Text With Key To Hex", handle_xor_text_with_key_to_hex),
    "6": ("XOR Hex With Key To Text", handle_xor_hex_with_key_to_text),
    "7": ("Single-byte XOR Brute Force", handle_single_byte_xor_brute_force),
}


HASHING_MENU: MenuOptions = {
    "1": ("Generate Hash", handle_generate_hash),
    "2": ("Verify Hash", handle_verify_hash),
    "3": ("Show Supported Hashes", handle_show_supported_hashes),
}


FILES_MENU: MenuOptions = {
    "1": ("File Info", handle_file_info),
    "2": ("File Hash", handle_file_hash),
    "3": ("Extract Strings From File", handle_extract_strings_from_file),
}


DETECTION_MENU: MenuOptions = {
    "1": ("Analyze Input", handle_analyze_input),
}


WEB_MENU: MenuOptions = {
    "1": ("Decode JWT", handle_decode_jwt),
    "2": ("HTTP Request", handle_http_request),
}


HISTORY_REPORTS_MENU: MenuOptions = {
    "1": ("Show Operation History", handle_show_history),
    "2": ("Clear Operation History", handle_clear_history),
    "3": ("Export History To TXT Report", handle_export_history_to_txt),
    "4": ("Export History To JSON Report", handle_export_history_to_json),
}


SETTINGS_MENU: MenuOptions = {
    "1": ("Show Settings", handle_show_settings),
    "2": ("Update Setting", handle_update_setting),
    "3": ("Reset Settings", handle_reset_settings),
}


EXTRACTION_MENU: MenuOptions = {
    "1": ("Find CTF Flags In Text", handle_find_ctf_flags_in_text),
    "2": ("Extract Indicators From Text", handle_extract_indicators_from_text),
    "3": ("Extract Indicators From File", handle_extract_indicators_from_file),
}


CATEGORY_OPTIONS: CategoryOptions = {
    "1": ("Encoding / Decoding", ENCODING_MENU),
    "2": ("Crypto", CRYPTO_MENU),
    "3": ("Hashing", HASHING_MENU),
    "4": ("Files / Forensics", FILES_MENU),
    "5": ("Detection", DETECTION_MENU),
    "6": ("Web", WEB_MENU),
    "7": ("History / Reports", HISTORY_REPORTS_MENU),
    "8": ("Settings", SETTINGS_MENU),
    "9": ("Extraction", EXTRACTION_MENU),
}


def show_main_menu() -> None:
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]CTF Security Toolkit[/bold cyan]\n"
            "[white]Modular helper for legal CTF and cybersecurity lab tasks[/white]",
            border_style="cyan",
        )
    )

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Option", justify="right")
    table.add_column("Category")

    for option_number, option_data in CATEGORY_OPTIONS.items():
        category_name = option_data[0]
        table.add_row(option_number, category_name)

    table.add_row("0", "Exit")

    console.print(table)


def show_category_menu(category_name: str, menu_options: MenuOptions) -> None:
    console.print()
    console.print(
        Panel.fit(
            f"[bold cyan]{category_name}[/bold cyan]",
            border_style="cyan",
        )
    )

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Option", justify="right")
    table.add_column("Tool")

    for option_number, option_data in menu_options.items():
        tool_name = option_data[0]
        table.add_row(option_number, tool_name)

    table.add_row("0", "Back")

    console.print(table)


def run_category_menu(category_name: str, menu_options: MenuOptions) -> None:
    while True:
        show_category_menu(category_name, menu_options)
        choice = input("Choose option: ").strip()

        if choice == "0":
            break

        selected_option = menu_options.get(choice)

        if selected_option is None:
            print_error("Invalid option. Try again.")
            continue

        _, action = selected_option
        action()


def run_menu() -> None:
    while True:
        show_main_menu()
        choice = input("Choose category: ").strip()

        if choice == "0":
            print_success("Exiting program...")
            break

        selected_category = CATEGORY_OPTIONS.get(choice)

        if selected_category is None:
            print_error("Invalid category. Try again.")
            continue

        category_name, menu_options = selected_category
        run_category_menu(category_name, menu_options)