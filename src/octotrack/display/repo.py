from datetime import datetime

from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.console import Group

from ..utils import _console as c
from ..models import RepositoryInfo


__all__ = ["RenderRepoInfo"]


class RenderRepoInfo:
    def __init__(self, repo_info: RepositoryInfo) -> None:
        self.repo_info = repo_info
        self.console = c

    def _format_size(self, size_kb: int) -> str:
        if size_kb >= 1_000_000:
            return f"{size_kb / 1_000_000:.1f} GB"
        if size_kb >= 1_000:
            return f"{size_kb / 1_000:.1f} MB"
        return f"{size_kb} KB"

    def _format_date(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M")

    def _build_owner_panel(self, height: int) -> Panel:
        owner = self.repo_info.owner
        table = Table.grid(padding=(0, 1))
        table.add_column(style="label")
        table.add_column(style="value")
        table.add_row("Login", owner.login)
        table.add_row("Type", owner.type)
        table.add_row("URL", owner.html_url)
        return Panel(table, title="Owner", border_style="repo.owner", height=height)

    def _build_stats_panel(self, height: int) -> Panel:
        table = Table.grid(padding=(0, 1))
        table.add_column(style="label")
        table.add_column(style="value", justify="right")
        table.add_row("Stars", str(self.repo_info.stargazers_count))
        table.add_row("Forks", str(self.repo_info.forks))
        table.add_row("Watchers", str(self.repo_info.watchers))
        table.add_row("Size", self._format_size(self.repo_info.size))
        return Panel(table, title="Stats", border_style="repo.stats", height=height)

    def _build_metadata_panel(self, height: int) -> Panel:
        table = Table.grid(padding=(0, 1))
        table.add_column(style="label")
        table.add_column(style="value")
        table.add_row("Default branch", self.repo_info.default_branch)
        table.add_row("Homepage", self.repo_info.homepage or "—")
        table.add_row("Created", self._format_date(self.repo_info.created_at))
        table.add_row("Updated", self._format_date(self.repo_info.updated_at))
        table.add_row("Pushed", self._format_date(self.repo_info.pushed_at))
        return Panel(
            table, title="Metadata", border_style="repo.metadata", height=height
        )

    def _build_header(self) -> Text:
        header = Text(justify="center")
        header.append(f"{self.repo_info.visibility.upper()}", style="status.visibility")
        if self.repo_info.archived:
            header.append("  ARCHIVED", style="status.archived")
        header.append("\n")
        header.append(
            self.repo_info.description or "No description provided",
            style="value" if self.repo_info.description else "muted",
        )
        return header

    def render(self) -> None:
        header = self._build_header()

        top_row = Table.grid(expand=True)
        top_row.add_column(ratio=1)
        top_row.add_column(ratio=1)
        top_row.add_column(ratio=1)

        owner_lines = 3
        stats_lines = 4
        metadata_lines = 5
        target_height = max(owner_lines, stats_lines, metadata_lines) + 2

        top_row.add_row(
            self._build_owner_panel(height=target_height),
            self._build_stats_panel(height=target_height),
            self._build_metadata_panel(height=target_height),
        )

        body = Group(
            header,
            Text(),
            top_row,
        )

        self.console.print(
            Panel(body, title=self.repo_info.full_name, border_style="repo.title")
        )
