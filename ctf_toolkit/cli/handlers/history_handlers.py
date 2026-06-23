from ctf_toolkit.core.console import print_error, print_success
from ctf_toolkit.core.history import clear_history, read_history
from ctf_toolkit.core.output import print_list, print_result
from ctf_toolkit.core.settings import get_setting


def handle_show_history() -> None:
    default_limit = int(get_setting("history_default_limit"))

    limit_text = input(
        f"How many latest history records to show, default {default_limit}: "
    ).strip()

    try:
        if limit_text == "":
            limit = default_limit
        else:
            limit = int(limit_text)

        events = read_history(limit=limit)

        if not events:
            print_result(
                "Operation History",
                "History is empty.",
                record_history=False,
            )
            return

        formatted_events = []

        for event in events:
            timestamp = event.get("timestamp", "unknown time")
            event_type = event.get("event_type", "unknown")
            title = event.get("title", "unknown")
            value = event.get("value", "")

            formatted_events.append(
                f"{timestamp} | {event_type} | {title} | {value}"
            )

        print_list(
            "Latest Operation History",
            formatted_events,
            record_history=False,
        )

    except ValueError:
        print_error("Limit must be a number.")

    except Exception as error:
        print_error(str(error))


def handle_clear_history() -> None:
    confirmation = input("Do you really want to clear history? Type YES: ")

    if confirmation != "YES":
        print_error("History was not cleared.")
        return

    try:
        clear_history()
        print_success("History cleared.")

    except Exception as error:
        print_error(str(error))