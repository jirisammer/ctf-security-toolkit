from ctf_toolkit.core.console import print_error, print_success
from ctf_toolkit.core.output import print_key_value_table
from ctf_toolkit.core.settings import (
    load_settings,
    update_setting,
    reset_settings,
)


def handle_show_settings() -> None:
    try:
        settings = load_settings()
        print_key_value_table(
            "Current Settings",
            settings,
            record_history=False,
        )

    except Exception as error:
        print_error(str(error))


def handle_update_setting() -> None:
    try:
        settings = load_settings()

        print_key_value_table(
            "Available Settings",
            settings,
            record_history=False,
        )

        key = input("Enter setting name: ").strip()
        value = input("Enter new value: ").strip()

        updated_settings = update_setting(key, value)

        print_success("Setting updated.")
        print_key_value_table(
            "Updated Settings",
            updated_settings,
            record_history=False,
        )

    except Exception as error:
        print_error(str(error))


def handle_reset_settings() -> None:
    confirmation = input("Do you really want to reset settings? Type YES: ")

    if confirmation != "YES":
        print_error("Settings were not reset.")
        return

    try:
        settings = reset_settings()

        print_success("Settings reset to default values.")
        print_key_value_table(
            "Default Settings",
            settings,
            record_history=False,
        )

    except Exception as error:
        print_error(str(error))