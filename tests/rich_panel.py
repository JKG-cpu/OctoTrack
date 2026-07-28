from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text

console = Console()

left_top = Panel("Repo Info\n[1] Show details", title="Info", border_style="cyan")
left_bottom = Panel(
    "Releases\n[2] List releases", title="Releases", border_style="green"
)

paragraph = Text(
    "OctoTrack lets you pull commits, pull requests, issues, and releases "
    "for any GitHub repository straight from your terminal. Use the menu "
    "on the left to jump into a category, or run a subcommand directly."
)
right_panel = Panel(paragraph, title="About", border_style="magenta")

layout = Layout()
layout.split_row(
    Layout(name="left", ratio=1),
    Layout(name="right", ratio=1),
)
layout["left"].split_column(
    Layout(left_top),
    Layout(left_bottom),
)
layout["right"].update(right_panel)

# Layout needs an explicit total height since it fills whatever space it's given
outer = Panel(layout, title="OctoTrack Menu", border_style="bold white", height=20)

console.print(outer)
