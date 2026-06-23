from ctf_toolkit.core.console import print_error
from ctf_toolkit.core.output import print_result
from ctf_toolkit.core.settings import get_setting

from ctf_toolkit.modules.reporting.report_exporter import (
    export_history_to_txt,
    export_history_to_json,
)


def _ask_limit() -> int:
    default_limit = int(get_setting("report_default_limit"))

    limit_text = input(
        f"How many latest history records to export, default {default_limit}: "
    ).strip()

    if limit_text == "":
        return default_limit

    return int(limit_text)


def handle_export_history_to_txt() -> None:
    try:
        limit = _ask_limit()
        report_path = export_history_to_txt(limit=limit)

        print_result(
            "TXT Report Exported",
            f"Report saved to: {report_path}",
            record_history=False,
        )

    except ValueError:
        print_error("Limit must be a valid positive number.")

    except Exception as error:
        print_error(str(error))


def handle_export_history_to_json() -> None:
    try:
        limit = _ask_limit()
        report_path = export_history_to_json(limit=limit)

        print_result(
            "JSON Report Exported",
            f"Report saved to: {report_path}",
            record_history=False,
        )

    except ValueError:
        print_error("Limit must be a valid positive number.")

    except Exception as error:
        print_error(str(error))