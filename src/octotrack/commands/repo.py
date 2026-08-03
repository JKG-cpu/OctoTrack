import typer
import asyncio
import base64

from ..client import RepoClient
from ..core import ConfigKey, edit_config
from ..utils import load_config, Text
from ..models import RepositoryInfo, RepositoryReadme, RepositoryContent
from ..display import RepoInfoRenderer, display_readme, display_contents


app = typer.Typer()


# Helpers
def _parse_owner_repo(value: str | None, config: dict) -> tuple[str, str]:
    if value and "/" in value:
        return tuple(value.split("/", 1))

    owner = config["default_owner"]
    repo = value or config["default_repo"]

    if not owner:
        Text.error(
            "Specify 'owner/repo' OR set a default with 'octotrack repo default <owner/repo>'"
        )
        raise typer.Exit(1)

    if not repo:
        Text.error("Provide a repo, e.g 'octotrack repo info JKG-cpu/OctoTrack'")
        raise typer.Exit(1)

    return owner, repo


# Async Methods
async def _repo_info(owner: str, repo: str) -> None:
    client = RepoClient()
    base = await client.get_repo(repo, owner)
    readme = await client.get_readme(repo, owner)

    raw_bytes = base64.b64decode(readme.json()["content"])
    readme_text = raw_bytes.decode("utf-8")

    RepoInfoRenderer(
        RepositoryInfo.model_validate(
            {
                **base.json(),
                "readme": {"content": readme_text, "name": readme.json()["name"]},
            }
        )
    ).render()


async def _get_readme(owner: str, repo: str) -> None:
    client = RepoClient()

    response = await client.get_readme(repo, owner)

    raw_bytes = base64.b64decode(response.json()["content"])
    readme_text = raw_bytes.decode("utf-8")

    display_readme(
        RepositoryReadme.model_validate(
            {"content": readme_text, "name": response.json()["name"]}
        )
    )


async def _get_content(
    owner: str, repo: str, path: str, hidden: bool, depth: int
) -> list[RepositoryContent]:
    return await RepoClient().get_contents(repo, owner, path, hidden, depth)


# Commands
# region
@app.command(help="Get repository info")
def info(
    owner_repo: str = typer.Argument(
        None, metavar="OWNER/REPO", help="e.g 'JKG-cpu/OctoTrack'"
    ),
) -> None:
    owner, repo = _parse_owner_repo(owner_repo, load_config())
    with Text.status("Figuring out what this repo is about...", style="bold white"):
        asyncio.run(_repo_info(owner, repo))


@app.command(help="Set the default owner/repo")
def default(
    owner_repo: str = typer.Argument(
        ..., metavar="OWNER/REPO", help="Default owner/repo, e.g. 'JKG-cpu/OctoTrack'"
    ),
) -> None:
    owner, repo = (
        (owner_repo.split("/", 1) + [None])[:2]
        if "/" in owner_repo
        else (owner_repo, None)
    )

    edit_config(ConfigKey.default_owner, owner)
    if repo:
        edit_config(ConfigKey.default_repo, repo)


@app.command(help="Get a repository's [italic]README.md[/italic]")
def readme(
    owner_repo: str = typer.Argument(
        None, metavar="OWNER/REPO", help="Default owner/repo, e.g. 'JKG-cpu/OctoTrack'"
    ),
) -> None:
    owner, repo = _parse_owner_repo(owner_repo, load_config())
    with Text.status("Finding another README file...", style="bold white"):
        asyncio.run(_get_readme(owner, repo))


@app.command(help="Get the file contents of a repository")
def contents(
    owner_repo: str = typer.Argument(
        None, metavar="OWNER/REPO", help="Default owner/repo, e.g 'JKG-cpu/OctoTrack'"
    ),
    path: str = typer.Option(
        None, "-p", "--path", help="Specify a folder in the repository"
    ),
    hidden: bool = typer.Option(False, "-h", "--hidden", help="Show hidden files"),
    ls: bool = typer.Option(False, "-l", "--list", help="List files & folders"),
    depth: int = typer.Option(3, help="The depth of which to go to."),
) -> None:
    owner, repo = _parse_owner_repo(owner_repo, load_config())
    with Text.status("Fetching Repo Contents...", style="bold white"):
        repo_content = asyncio.run(_get_content(owner, repo, path, hidden, depth))

    display_contents(repo_content, ls)


# endregion
