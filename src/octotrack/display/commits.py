from datetime import datetime

from rich.text import Text
from rich.table import Table

from ..utils import _console as c
from ..models import Commit


__all__ = ["display_commits"]


def _format_commit_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")


def _commit_summary(message: str) -> str:
    return message.splitlines()[0] if message else ""


def display_commits(commits: list[Commit], show_all: bool) -> None:
    if not commits:
        c.print(Text("No commits found.", style="muted"))
        return

    total = len(commits)
    visible = commits if show_all else commits[:10]

    table = Table(box=None, show_header=True, header_style="label", padding=(0, 2))
    table.add_column("SHA", style="repo.stats")
    table.add_column("Date", style="muted")
    table.add_column("Committer", style="value")
    table.add_column("Message", style="value", overflow="ellipsis", max_width=60)

    for commit in visible:
        details = commit.commit
        table.add_row(
            commit.sha[:7],
            _format_commit_date(details.committer.date),
            details.committer.name,
            _commit_summary(details.message),
        )

    c.print(table)

    if not show_all and total > 10:
        footer = Text()
        footer.append(f"Showing 10 of {total} commits", style="muted")
        footer.append("  ·  use --all to see the rest", style="muted italic")
        c.print(footer)