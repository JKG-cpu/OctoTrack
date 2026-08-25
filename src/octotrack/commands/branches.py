import asyncio

import typer

from ..client import Client
from ..display import DisplayManager
from ..models import Branch, SimpleBranch
from ..utils import Text, _parse_owner_repo, load_config

__all__ = ["app"]


app = typer.Typer()


async def get_branches(owner: str, repo: str) -> None:
    c = Client()
    d = DisplayManager()

    with Text.status("Grabbing this repository's branches...", style="bold white"):
        response = await c.get_branches(owner, repo)
        branches: list[SimpleBranch] = []

        for json in response.json():
            branch = SimpleBranch.model_validate(json)
            full_branch = await c.get_branch(owner, repo, branch.name)
            b = Branch.model_validate(full_branch.json())
            branch.commit_message = b.commit.commit.message
            branches.append(branch)

    d.display_branches(branches)


async def get_branch(owner: str, repo: str, branch: str) -> None:
    c = Client()
    d = DisplayManager()

    with Text.status("Grabbing this repository's branches...", style="bold white"):
        response = await c.get_branch(owner, repo, branch)
        
    d.display_branch(Branch.model_validate(response.json()))


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    owner_repo: str = typer.Argument(
        None, metavar="OWNER/REPO", help="e.g 'JKG-cpu/OctoTrack'"
    ),
    branch: str = typer.Option(
        None, "--branch", "-b", help="Choose a branch to see (will output more text)"
    ),
) -> None:
    owner, repo = _parse_owner_repo(owner_repo, load_config())

    if ctx.invoked_subcommand is None:
        if branch:
            asyncio.run(get_branch(owner, repo, branch))
        else:
            asyncio.run(get_branches(owner, repo))
