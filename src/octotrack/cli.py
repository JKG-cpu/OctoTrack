from importlib.metadata import version

import typer
from rich.console import Console, Text

from .commands import (
    branch_app,
    commit_app,
    config_app,
    issues_app,
    pr_app,
    release_app,
    repo_app,
    setup_app,
    tag_app,
)

__all__ = ["app"]

app = typer.Typer()
app.add_typer(
    branch_app,
    name="branches",
    help="Get one or all the branches of a commit repository",
)
app.add_typer(commit_app, name="commits", help="Get the commits for a repository")
app.add_typer(config_app, name="config", help="Run config commands")
app.add_typer(issues_app, name="issues", help="View Issues for a repository")
app.add_typer(pr_app, name="pr", help="View Pull Requests for a repository")
app.add_typer(release_app, name="releases", help="Get the releases for a repository")
app.add_typer(repo_app, name="repo", help="Run repository related commands")
app.add_typer(setup_app, name="setup")
app.add_typer(tag_app, name="tags", help="View the latest tags for a repository")


def get_version() -> str:
    return version("octotrack")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version", "-v", help="Display your current OctoTrack version"
    ),
) -> None:
    if ctx.invoked_subcommand is None:
        if version:
            Console().print(
                Text(f"OctoTrack {get_version()}", style="italic bold cyan")
            )
        else:
            print(ctx.get_help())
