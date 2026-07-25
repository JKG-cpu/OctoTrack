from rich.console import Console
from rich.progress import Progress
from rich.status import Status


__all__ = ["CHECKMARK", "TOKEN_NAME", "CONFIG_SETTINGS", "CLI_NAME", "Text"]


# ASCII Characters
CHECKMARK = "✓"


# Consts
TOKEN_NAME = "GITHUB_TOKEN"
CONFIG_SETTINGS = {
    "default_owner": None,
    "default_pr_state": "open",
    "api_base_url": "https://api.github.com",
}
CLI_NAME = "octotrack"


# Custom Text Output
_console: Console = Console()
_console.style = "bold white"


class Text:
    @staticmethod
    def text(text: str, style: str, end="\n") -> None:
        _console.print(f"[{style}]{text}[/{style}]", end=end)

    @staticmethod
    def get_input(text: str, style: str, ending: str = " > ") -> str:
        _console.print(f"[{style}]{text}[/{style}]", end=ending)
        return input()

    @staticmethod
    def success(text: str) -> None:
        _console.print(f"[bold green]{CHECKMARK} {text}[/bold green]")

    @staticmethod
    def error(text: str) -> None:
        _console.print(f"[bold red]{text}[/bold red]")

    @staticmethod
    def warning(text: str) -> None:
        _console.print(f"[bold yellow]{text}[/bold yellow]")

    @staticmethod
    def info(text: str) -> None:
        _console.print(f"[bold cyan]{text}[/bold cyan]")

    @staticmethod
    def progress() -> Progress:
        return Progress(console=_console)

    @staticmethod
    def status(text: str, style: str) -> Status:
        return _console.status(f"[{style}]{text}[/{style}]")
