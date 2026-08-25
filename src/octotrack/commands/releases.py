import asyncio

import typer

from ..client import Client
from ..display import DisplayManager
from ..models import Releases
from ..utils import Text, _parse_owner_repo, load_config

__all__ = ["app"]


app = typer.Typer()


async def get_releases(owner: str, repo: str) -> None:
    c = Client()
    d = DisplayManager()

    with Text.status("Looking for releases...", style="bold white"):
        response = await c.get_releases(owner, repo)
        releases = [Releases.model_validate(json) for json in response.json()]

    d.display_releases(releases)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    owner_repo: str = typer.Argument(
        None, metavar="OWNER/REPO", help="e.g 'JKG-cpu/OctoTrack'"
    ),
) -> None:
    if ctx.invoked_subcommand is None:
        owner, repo = _parse_owner_repo(owner_repo, load_config())
        asyncio.run(get_releases(owner, repo))
