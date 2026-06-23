from ctf_toolkit.core.console import print_error
from ctf_toolkit.core.output import print_key_value_table, print_section

from ctf_toolkit.modules.detection.input_detector import analyze_input


def handle_analyze_input() -> None:
    text = input("Enter text to analyze: ")

    try:
        results = analyze_input(text)

        print_section("Input Analysis Result")

        for index, result in enumerate(results, start=1):
            print_key_value_table(
                f"Detection #{index}",
                {
                    "Type": result["type"],
                    "Confidence": result["confidence"],
                    "Details": result["details"],
                },
            )

    except Exception as error:
        print_error(str(error))