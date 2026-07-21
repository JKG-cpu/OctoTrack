import typer
import asyncio

from ..client import GitHubClient

app = typer.Typer()

# Async commands
#region
async def _repo(user: str | None, repo: str) -> None:
    g = GitHubClient()
    response = await g.get_repo(repo, user)
    print(response)
#endregion

@app.command()
def repo(
    repo: str, user: str | None = typer.Option(None, help="Specify the user's repo")
) -> None:
    asyncio.run(_repo(user, repo))
