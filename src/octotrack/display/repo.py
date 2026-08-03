import os
from datetime import datetime

from rich.markdown import Markdown
from rich.tree import Tree
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.console import Group
from rich.rule import Rule

from ..utils import _console as c
from ..models import RepositoryInfo, RepositoryReadme, RepositoryContent


__all__ = ["RepoInfoRenderer", "display_readme", "display_contents"]


_TYPE_INDICATOR = {
    "dir": "d",
    "file": "-",
    "symlink": "l",
    "submodule": "m",
}


def _format_size(size: int) -> str:
    if size >= 1_000_000:
        return f"{size / 1_000_000:.1f} MB"
    if size >= 1_000:
        return f"{size / 1_000:.1f} KB"
    return f"{size} B"


def _display_ls(repo_contents: list[RepositoryContent]) -> None:
    table = Table(box=None, show_header=True, header_style="label", padding=(0, 2))
    table.add_column("", width=1)
    table.add_column("Size", justify="right", style="value")
    table.add_column("Name", style="value")

    def add_rows(items: list[RepositoryContent], depth: int = 0) -> None:
        sorted_items = sorted(items, key=lambda i: (i.type != "dir", i.name.lower()))
        for item in sorted_items:
            indicator = Text(_TYPE_INDICATOR.get(item.type, "?"), style="repo.stats")
            size_str = "—" if item.type == "dir" else _format_size(item.size)
            name_style = "repo.title" if item.type == "dir" else "value"

            name_text = Text("  " * depth, style="bold")
            name_text.append(
                item.name if item.type != "dir" else f"{item.name}/", style=name_style
            )

            table.add_row(indicator, size_str, name_text)
            if item.type == "dir" and item.content:
                add_rows(item.content, depth + 1)

    add_rows(repo_contents)
    c.print(table)


def _tree_label(item: RepositoryContent) -> Text:
    label = Text()
    if item.type == "dir":
        label.append(item.name, style="repo.title")
    else:
        label.append(item.name, style="value")
        label.append(f"  {_format_size(item.size)}", style="muted")
    return label


def _add_tree_nodes(node: Tree, items: list[RepositoryContent]) -> None:
    for item in sorted(items, key=lambda i: (i.type != "dir", i.name.lower())):
        child = node.add(_tree_label(item))
        if item.type == "dir" and item.content:
            _add_tree_nodes(child, item.content)


def _build_tree(repo_contents: list[RepositoryContent]) -> Tree:
    root = Tree(Text("Contents", style="repo.title"))
    _add_tree_nodes(root, repo_contents)
    return root


def _flatten(items: list[RepositoryContent]) -> list[RepositoryContent]:
    flat: list[RepositoryContent] = []
    for item in items:
        flat.append(item)
        if item.type == "dir" and item.content:
            flat.extend(_flatten(item.content))
    return flat


def _display_stats(repo_contents: list[RepositoryContent]) -> None:
    all_items = _flatten(repo_contents)

    files = [i for i in all_items if i.type == "file"]
    dirs = [i for i in all_items if i.type == "dir"]
    others = [i for i in all_items if i.type not in ("file", "dir")]

    total_size = sum(f.size for f in files)
    largest = max(files, key=lambda f: f.size, default=None)

    ext_stats: dict[str, list[int]] = {}
    for f in files:
        ext = os.path.splitext(f.name)[1].lstrip(".") or "no ext"
        count, size = ext_stats.get(ext, [0, 0])
        ext_stats[ext] = [count + 1, size + f.size]

    header = Text()
    header.append(f"{len(all_items)} items", style="repo.title")
    header.append("  ·  ", style="muted")
    header.append(f"{len(dirs)} directories", style="value")
    header.append("  ·  ", style="muted")
    header.append(f"{len(files)} files", style="value")
    if others:
        header.append("  ·  ", style="muted")
        header.append(f"{len(others)} other", style="value")

    stat_bar = Table.grid(padding=(0, 3), expand=False)
    for _ in range(3):
        stat_bar.add_column(justify="left")

    def stat(icon: str, value: str, label: str) -> Text:
        t = Text()
        t.append(f"{icon} ", style="repo.stats")
        t.append(f"{value} ", style="text.base_text")
        t.append(label, style="label")
        return t

    stat_bar.add_row(
        stat("▣", _format_size(total_size), "total size"),
        stat("✦", largest.name if largest else "—", "largest file"),
        stat("#", str(len(ext_stats)), "file types"),
    )

    breakdown = Table.grid(padding=(0, 2))
    breakdown.add_column(style="label", justify="right")
    breakdown.add_column(style="value")
    for ext, (count, size) in sorted(ext_stats.items(), key=lambda kv: -kv[1][1]):
        label = f".{ext}" if ext != "no ext" else ext
        breakdown.add_row(label, f"{count} files · {_format_size(size)}")

    body = Group(
        header,
        Text(),
        stat_bar,
        Rule(style="muted"),
        breakdown,
        Rule(style="muted"),
        _build_tree(repo_contents),
    )
    c.print(Panel(body, border_style="repo.owner", padding=(1, 2)))


def display_contents(repo_contents: list[RepositoryContent], ls: bool) -> None:
    if not repo_contents:
        c.print(Text("No contents found.", style="muted"))
        return

    if ls:
        _display_ls(repo_contents)
    else:
        _display_stats(repo_contents)


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
            stat("▣", _format_size(self.repo_info.size), "size"),
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
