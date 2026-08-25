import os
from datetime import datetime
from typing import Literal

from readchar import readkey
from rich import box
from rich.console import Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from ..models import (
    Branch,
    Commit,
    Issues,
    Releases,
    RepositoryContent,
    RepositoryInfo,
    RepositoryReadme,
    SimpleBranch,
    Tag,
)
from ..utils import _console, cc

__all__ = ["DisplayManager", "RepoInfoRenderer"]

_TYPE_INDICATOR = {
    "dir": "d",
    "file": "-",
    "symlink": "l",
    "submodule": "m",
}


class DisplayManager:
    def __init__(self) -> None:
        self.console = _console

    # Helpers
    # Commits
    # region
    def _format_date(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M")

    def _commit_summary(self, message: str) -> str:
        return message.splitlines()[0] if message else ""

    # endregion

    # Repository
    # region
    def _format_size(self, size: int) -> str:
        if size >= 1_000_000:
            return f"{size / 1_000_000:.1f} MB"
        if size >= 1_000:
            return f"{size / 1_000:.1f} KB"
        return f"{size} B"

    def _display_ls(self, repo_contents: list[RepositoryContent]) -> None:
        table = Table(box=None, show_header=True, header_style="label", padding=(0, 2))
        table.add_column("", width=1)
        table.add_column("Size", justify="right", style="value")
        table.add_column("Name", style="value")

        def add_rows(items: list[RepositoryContent], depth: int = 0) -> None:
            sorted_items = sorted(
                items, key=lambda i: (i.type != "dir", i.name.lower())
            )
            for item in sorted_items:
                indicator = Text(
                    _TYPE_INDICATOR.get(item.type, "?"), style="repo.stats"
                )
                size_str = "—" if item.type == "dir" else self._format_size(item.size)
                name_style = "repo.title" if item.type == "dir" else "value"

                name_text = Text("  " * depth, style="bold")
                name_text.append(
                    item.name if item.type != "dir" else f"{item.name}/",
                    style=name_style,
                )

                table.add_row(indicator, size_str, name_text)
                if item.type == "dir" and item.content:
                    add_rows(item.content, depth + 1)

        add_rows(repo_contents)
        self.console.print(table)

    def _tree_label(self, item: RepositoryContent) -> Text:
        label = Text()
        if item.type == "dir":
            label.append(item.name, style="repo.title")
        else:
            label.append(item.name, style="value")
            label.append(f"  {self._format_size(item.size)}", style="muted")
        return label

    def _add_tree_nodes(self, node: Tree, items: list[RepositoryContent]) -> None:
        for item in sorted(items, key=lambda i: (i.type != "dir", i.name.lower())):
            child = node.add(self._tree_label(item))
            if item.type == "dir" and item.content:
                self._add_tree_nodes(child, item.content)

    def _build_tree(self, repo_contents: list[RepositoryContent]) -> Tree:
        root = Tree(Text("Contents", style="repo.title"))
        self._add_tree_nodes(root, repo_contents)
        return root

    def _flatten(self, items: list[RepositoryContent]) -> list[RepositoryContent]:
        flat: list[RepositoryContent] = []
        for item in items:
            flat.append(item)
            if item.type == "dir" and item.content:
                flat.extend(self._flatten(item.content))
        return flat

    def _display_stats(self, repo_contents: list[RepositoryContent]) -> None:
        all_items = self._flatten(repo_contents)

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
            stat("▣", self._format_size(total_size), "total size"),
            stat("✦", largest.name if largest else "—", "largest file"),
            stat("#", str(len(ext_stats)), "file types"),
        )

        breakdown = Table.grid(padding=(0, 2))
        breakdown.add_column(style="label", justify="right")
        breakdown.add_column(style="value")
        for ext, (count, size) in sorted(ext_stats.items(), key=lambda kv: -kv[1][1]):
            label = f".{ext}" if ext != "no ext" else ext
            breakdown.add_row(label, f"{count} files · {self._format_size(size)}")

        body = Group(
            header,
            Text(),
            stat_bar,
            Rule(style="muted"),
            breakdown,
            Rule(style="muted"),
            self._build_tree(repo_contents),
        )
        self.console.print(Panel(body, border_style="repo.owner", padding=(1, 2)))

    # endregion

    # Branches
    # region
    def _latest_commit(self, branch_name: str, commit_data: Commit) -> Group:
        commit_details = commit_data.commit
        commiter = commit_details.committer

        heading = Text("Latest Commit for ", style="bold italic white") + Text(
            f"{branch_name}", style="bold italic cyan"
        )

        grid = Table(box=box.SIMPLE_HEAD, show_edge=False, padding=(0, 1))
        grid.add_column("Committer", style="repo.owner", justify="center", ratio=1)
        grid.add_column(
            "Commit Message", style="bold italic yellow", justify="center", ratio=3
        )
        grid.add_column("Commit Date", style="muted", justify="center", ratio=1)

        grid.add_row(
            Text(commiter.name),
            Text(self._commit_summary(commit_details.message)),
            Text(self._format_date(commiter.date)),
        )

        return Group(heading, Text(), grid)

    # endregion

    # Releases
    # region
    def generate_release_page(self, release_data: Releases) -> Panel:
        group = Group(
            Text(f"Title: {release_data.name}", style="repo.title"),
            Text(f"Tag: {release_data.tag_name}"),
            Rule(),
            Markdown(release_data.body, justify="left"),
            Rule(),
            Text.from_markup(
                f"[link={release_data.html_url.strip('"')}]Visit Release Page[/link]"
            ),
            Text(
                "Press A / D to scroll\nPress C to exit",
                style="text.keybind",
                justify="right",
            ),
        )

        return Panel(group, padding=(0, 2), border_style="repo.owner")

    # endregion

    # Issues
    # region
    def get_issue_status_grid(self, issue: Issues) -> Table.grid:
        grid = Table.grid(expand=False, padding=(0, 2))

        grid.add_column(justify="left")

        grid.add_row(f"Created at: {self._format_date(issue.created_at)}")
        grid.add_row(f"Updated at: {self._format_date(issue.updated_at)}")

        if issue.closed_at:
            grid.add_row(f"Closed at: {self._format_date(issue.closed_at)}")
            grid.add_row(
                Text("Closed by: ")
                + Text.from_markup(
                    f"[link={issue.closed_by.html_url}]{issue.closed_by.login}[/link]"
                )
            )

        else:
            grid.add_row("Not closed")

        return grid

    def generate_issues_page(
        self, issue: Issues, state: Literal["all", "open", "closed"]
    ) -> Panel:
        group = Group(
            Text(f"Issue Title: {issue.title}", style="repo.title"),
            Text.from_markup(
                f"[link={issue.user.html_url}]{issue.user.login}[/link]",
                style="repo.title",
            ),
            Rule(),
            Markdown(issue.body),
            Rule(),
            Text(f"State: {issue.state}\nIssue Number: {issue.number}"),
            self.get_issue_status_grid(issue),
            Text(
                "Press A / D to scroll\nPress C to exit",
                style="text.keybind",
                justify="right",
            ),
        )

        return Panel(group, border_style="repo.owner", padding=(0, 2))

    # endregion

    # Callables
    # Commits
    # region
    def display_commits(self, commits: list[Commit], show_all: bool) -> None:
        if not commits:
            self.console.print(Text("No commits found.", style="muted"))
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
                self._format_date(details.committer.date),
                details.committer.name,
                self._commit_summary(details.message),
            )

        self.console.print(table)

        if not show_all and total > 10:
            footer = Text()
            footer.append(f"Showing 10 of {total} commits", style="muted")
            footer.append("  ·  use --all to see the rest", style="muted italic")
            self.console.print(footer)

    # endregion

    # Repository
    # region
    def display_contents(
        self, repo_contents: list[RepositoryContent], ls: bool
    ) -> None:
        if not repo_contents:
            self.console.print(Text("No contents found.", style="muted"))
            return

        if ls:
            self._display_ls(repo_contents)
        else:
            self._display_stats(repo_contents)

    def display_readme(self, repo_info: RepositoryReadme) -> None:
        self.console.print(
            Panel(
                Markdown(repo_info.content),
                title=repo_info.name,
                border_style="repo.owner",
                padding=(1, 2),
            )
        )

    # endregion

    # Branches
    # region
    def display_branches(self, branches: list[SimpleBranch]) -> None:
        if not branches:
            self.console.print(Text("No branches found.", style="muted"))
            return

        table = Table(box=None, show_header=True, header_style="label", padding=(0, 2))
        table.add_column("Name", style="repo.stats")
        table.add_column("Latest Commit", style="value")
        table.add_column("Protected", style="value")

        for branch in branches:
            table.add_row(branch.name, branch.commit_message, str(branch.protected))

        self.console.print(table)
        self.console.print(
            Text(
                "To view branch information, run `octotrack branches -b branch_name'",
                style="muted",
            )
        )

    def display_branch(self, branch: Branch) -> None:
        group = Group(
            Text("Branch ", style="text.base_text")
            + Text(branch.name, style="bold italic cyan")
            + Text("  ·  ", style="text.base_text")
            + Text(
                "Protected" if branch.protected else "Not Protected",
                style="repo.permissions",
            ),
            self._latest_commit(branch.name, branch.commit),
        )

        self.console.print(Panel(group, border_style="repo.owner", padding=(1, 2)))

    # endregion

    # Tags
    # region
    def display_tags(self, tags: list[Tag], owner: str, repo: str) -> None:
        if not tags:
            self.console.print(Text("No tags for the current repository.", style=""))
            return

        self.console.print(Text(f"Latest Tags for {repo}", style="repo.title"))

        tags_to_render = tags[:5]

        grid = Table.grid(padding=(0, 2))

        for t in tags_to_render:
            grid.add_row(Text(f" - {t.name}", style="bold italic yellow"))

        self.console.print(grid)

    # endregion

    # Releases
    # region
    def display_releases(self, releases: list[Releases]) -> None:
        if not releases:
            self.console.print("No Releases!")
            return

        page_index = 0
        rendering = True

        pages = [self.generate_release_page(page) for page in releases]

        while rendering:
            cc()
            page = pages[page_index]

            self.console.print(page)

            key = readkey()

            if key.title() == "A" and page_index != 0:
                page_index -= 1

            elif key.title() == "D" and page_index != len(releases) - 1:
                page_index += 1

            elif key.title() == "C":
                rendering = False

    # endregion

    # Issues
    # region
    def display_issues(
        self, issues: list[Issues], state: Literal["all", "open", "closed"]
    ) -> None:
        if not issues:
            self.console.print(
                "No Issues!" if state == "all" else f"No Issues that are {state}!"
            )
            return

        page_index = 0
        rendering = True

        pages = [self.generate_issues_page(issue, state) for issue in issues]

        while rendering:
            cc()
            page = pages[page_index]

            self.console.print(page)

            key = readkey()

            if key.title() == "A":
                if page_index == 0:
                    page_index = len(issues) - 1

                else:
                    page_index -= 1

            elif key.title() == "D":
                if page_index == len(issues) - 1:
                    page_index = 0

                else:
                    page_index += 1

            elif key.title() == "C":
                rendering = False

    # endregion


class RepoInfoRenderer:
    def __init__(self, repo_info: RepositoryInfo) -> None:
        self.repo_info: RepositoryInfo = repo_info
        self.console = _console

    # Helpers
    def _format_size(self, size: int) -> str:
        if size >= 1_000_000:
            return f"{size / 1_000_000:.1f} MB"
        if size >= 1_000:
            return f"{size / 1_000:.1f} KB"
        return f"{size} B"

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

    # Callable
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
