from rich.console import Console


console = Console()


def print_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    console.print(f"[bold green]{message}[/bold green]")


def print_info(message: str) -> None:
    console.print(f"[cyan]{message}[/cyan]")