from typing import Any

from rich.panel import Panel
from rich.table import Table

from ctf_toolkit.core.console import console
from ctf_toolkit.core.history import add_history_event


def print_result(title: str, value: Any, record_history: bool = True) -> None:
    """
    Prints one main result in a styled panel.
    """
    console.print()
    console.print(
        Panel(
            str(value),
            title=f"[bold green]{title}[/bold green]",
            border_style="green",
        )
    )

    if record_history:
        add_history_event(
            event_type="result",
            title=title,
            value=value,
        )


def print_key_value_table(
    title: str,
    data: dict[str, Any],
    record_history: bool = True,
) -> None:
    """
    Prints dictionary data as a simple key-value table.
    """
    table = Table(title=title, show_header=True, header_style="bold cyan")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    for key, value in data.items():
        table.add_row(str(key), str(value))

    console.print()
    console.print(table)

    if record_history:
        add_history_event(
            event_type="table",
            title=title,
            value=data,
        )


def print_list(title: str, items: list[Any], record_history: bool = True) -> None:
    """
    Prints list values as a table.
    """
    table = Table(title=title, show_header=True, header_style="bold cyan")
    table.add_column("#", justify="right", style="cyan")
    table.add_column("Value", style="white")

    for index, item in enumerate(items, start=1):
        table.add_row(str(index), str(item))

    console.print()
    console.print(table)

    if record_history:
        add_history_event(
            event_type="list",
            title=title,
            value=items,
        )


def print_section(title: str) -> None:
    """
    Prints a small section title.
    """
    console.print()
    console.print(f"[bold cyan]{title}[/bold cyan]")