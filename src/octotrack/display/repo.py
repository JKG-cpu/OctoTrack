from datetime import datetime

from rich.markdown import Markdown
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.console import Group
from rich.rule import Rule

from ..utils import _console as c
from ..models import RepositoryInfo, RepositoryReadme


__all__ = ["RepoInfoRenderer", "display_readme"]


def display_readme(repo_info: RepositoryReadme) -> None:
    c.print(
        Panel(
            Markdown(repo_info.content),
            title=repo_info.name,
            border_style="repo.owner",
            padding=(1, 2),
        )
    )


class RepoInfoRenderer:
    def __init__(self, repo_info: RepositoryInfo) -> None:
        self.repo_info: RepositoryInfo = repo_info
        self.console = c

    def _format_size(self, size_kb: int) -> str:
        if size_kb >= 1_000_000:
            return f"{size_kb / 1_000_000:.1f} GB"
        if size_kb >= 1_000:
            return f"{size_kb / 1_000:.1f} MB"
        return f"{size_kb} KB"

    def _format_date(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d")

    def _build_badges(self) -> Text:
        badges = Text()
        badges.append(
            f" {self.repo_info.visibility.upper()} ", style="status.visibility"
        )
        if self.repo_info.archived:
            badges.append("  ")
            badges.append(" ARCHIVED ", style="status.archived")
        badges.append("  ")
        badges.append(self.repo_info.language, style="repo.stats")
        if self.repo_info.license:
            badges.append("  ·  ")
            badges.append(self.repo_info.license.name, style="muted")
        if self.repo_info.readme:
            badges.append("  ·  ")
            badges.append(self.repo_info.readme.name, style="muted")
        return badges

    def _build_header(self) -> Group:
        title = Text(self.repo_info.full_name, style="repo.title")
        badges = self._build_badges()
        description = Text(
            self.repo_info.description or "No description provided",
            style="value" if self.repo_info.description else "muted",
        )
        return Group(title, badges, Text(), description)

    def _build_stat_bar(self) -> Table:
        stats = Table.grid(padding=(0, 3), expand=False)
        for _ in range(4):
            stats.add_column(justify="left")

        def stat(icon: str, value: str, label: str) -> Text:
            t = Text()
            t.append(f"{icon} ", style="repo.stats")
            t.append(f"{value} ", style="text.base_text")
            t.append(label, style="label")
            return t

        stats.add_row(
            stat("★", str(self.repo_info.stargazers_count), "stars"),
            stat("⑂", str(self.repo_info.forks), "forks"),
            stat("◎", str(self.repo_info.watchers), "watchers"),
            stat("▣", self._format_size(self.repo_info.size), "size"),
        )
        return stats

    def _build_permissions_line(self) -> Text:
        perms = self.repo_info.permissions
        line = Text()
        line.append("Access  ", style="label")
        entries = [
            ("Admin", perms.admin),
            ("Maintain", perms.maintain),
            ("Push", perms.push),
            ("Pull", perms.pull),
        ]
        for i, (name, granted) in enumerate(entries):
            if i:
                line.append("  ")
            line.append(
                "✓ " if granted else "✗ ", style="perm.yes" if granted else "perm.no"
            )
            line.append(name, style="value" if granted else "muted")
        return line

    def _build_body(self) -> Table:
        owner = self.repo_info.owner
        grid = Table.grid(padding=(0, 2))
        grid.add_column(style="label", justify="right")
        grid.add_column(style="value")

        grid.add_row("Owner", f"{owner.login} ({owner.type})")
        grid.add_row("URL", self.repo_info.html_url)
        grid.add_row("Default branch", self.repo_info.default_branch)
        grid.add_row("Homepage", self.repo_info.homepage or "—")
        grid.add_row(
            "Timeline",
            f"created {self._format_date(self.repo_info.created_at)}   ·   "
            f"pushed {self._format_date(self.repo_info.pushed_at)}   ·   "
            f"updated {self._format_date(self.repo_info.updated_at)}",
        )
        return grid

    def render(self) -> None:
        body = Group(
            self._build_header(),
            Text(),
            self._build_stat_bar(),
            Rule(style="muted"),
            self._build_body(),
            Text(),
            self._build_permissions_line(),
        )

        self.console.print(Panel(body, border_style="repo.owner", padding=(1, 2)))
