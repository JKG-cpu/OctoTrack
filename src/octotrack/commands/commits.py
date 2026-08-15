import typer
import asyncio

from ..client import CommitClient
from ..utils import _parse_owner_repo, load_config
from ..models import Commit
from ..display import display_commits

app = typer.Typer()

async def _run(owner: str, repo: str, show_all: bool):
    c = CommitClient()
    rep = await c.get_commit(owner, repo)
    commits: list[Commit] = [Commit.model_validate(commit_json) for commit_json in rep.json()]
    display_commits(commits, show_all)

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    owner_repo: str = typer.Argument(
        None, metavar="OWNER/REPO", help="e.g 'JKG-cpu/OctoTrack'"
    ),
    show_all: bool = typer.Option(
        False, "-a", "--all", help="Show all the commits for this repository."
    )
) -> None:
    if ctx.invoked_subcommand is None:
        owner, repo = _parse_owner_repo(owner_repo, load_config())
        asyncio.run(_run(owner, repo, show_all))
