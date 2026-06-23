import sys

from ctf_toolkit.cli.command_runner import run_cli_command
from ctf_toolkit.cli.menu import run_menu


def main() -> None:
    if len(sys.argv) > 1:
        exit_code = run_cli_command(sys.argv[1:])
        raise SystemExit(exit_code)

    run_menu()


if __name__ == "__main__":
    main()