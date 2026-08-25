import asyncio
from typing import Literal

import typer

from ..client import Client
from ..display import DisplayManager
from ..models import Issues
from ..utils import _parse_owner_repo, load_config

__all__ = ["app"]


app = typer.Typer()


async def get_issues(
    owner: str, repo: str, state: Literal["open", "closed", "all"]
) -> None:
    c = Client()
    d = DisplayManager()

    raw_issues = await c.get_issues(owner, repo, state)
    issues = [
        Issues.model_validate(json) for json in raw_issues if "pull_request" not in json
    ]

    d.display_issues(issues, state)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    owner_repo: str = typer.Argument(
        None, metavar="OWNER/REPO", help="e.g 'JKG-cpu/OctoTrack'"
    ),
    state: Literal["all", "open", "closed"] = typer.Option(
        "all", "--state", help="Define a state to use to filter issues"
    ),
) -> None:
    if ctx.invoked_subcommand is None:
        owner, repo = _parse_owner_repo(owner_repo, load_config())
        asyncio.run(get_issues(owner, repo, state))
