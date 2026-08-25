import asyncio

import typer

from ..client import Client
from ..display import DisplayManager
from ..models import Tag
from ..utils import Text, _parse_owner_repo, load_config

__all__ = ["app"]


app = typer.Typer()


async def get_tags(owner: str, repo: str) -> None:
    c = Client()
    d = DisplayManager()

    with Text.status("Finding Tags...", style="bold white"):
        response = await c.get_tags(owner, repo)
        tags: list[Tag] = [Tag.model_validate(data) for data in response.json()]

    d.display_tags(tags, owner, repo)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    owner_repo: str = typer.Argument(
        None, metavar="OWNER/REPO", help="e.g 'JKG-cpu/OctoTrack'"
    ),
) -> None:
    if ctx.invoked_subcommand is None:
        owner, repo = _parse_owner_repo(owner_repo, load_config())
        asyncio.run(get_tags(owner, repo))
