import httpx
import os
from pydantic import ValidationError

from ..utils import load_config, Text, TOKEN_NAME
from ..core import load_github_token, GitHubTokenStatus
from ..models import RepositoryContent


__all__ = ["RepoClient"]


class RepoClient:
    def __init__(self) -> None:
        self._load_token()
        self.config: dict = load_config()

        self.client = httpx.AsyncClient(
            base_url=self.config["api_base_url"], headers=self._load_headers()
        )

    def _load_token(self) -> None:
        status = load_github_token()

        if status == GitHubTokenStatus.INVALID_PATH:
            Text.error("Not all paths exist... some may have been moved or deleted.")
            Text.info("Please run 'octotrack setup' to complete the path setup.")
            exit(1)

        elif status == GitHubTokenStatus.TOKEN_NOT_SET:
            Text.warning(
                "[!] GitHub token not set. Run 'octotrack config set-token' to set a GitHub Auth Token."
            )
            exit(1)

    def _load_headers(self) -> dict:
        return {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {os.environ.get(TOKEN_NAME)}",
            "User-Agent": "OctoTrack",
        }

    async def _get_content(
        self, owner: str, repo: str, path: str, hidden: bool, depth: int
    ) -> list[RepositoryContent]:
        content = []
        response = await self._get(f"repos/{owner}/{repo}/contents/{path}")
        json = response.json()

        for item in json:
            n_item = RepositoryContent.model_validate(item)

            if not hidden and n_item.name.startswith("."):
                continue

            if n_item.type == "dir" and depth != 0:
                n_item.content = await self._get_content(
                    owner, repo, n_item.path, hidden, depth - 1
                )

            content.append(n_item)

        return content

    # Base Get Method
    async def _get(self, path: str, **params) -> httpx.Response:
        response = await self.client.get(path, params=params)

        self.rate_remaining = int(response.headers.get("x-ratelimit-remaining", 0))
        self.rate_reset = int(response.headers.get("x-ratelimit-reset", 0))

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            Text.error(f"Error when getting path: {path}. Error: \n{e}")
            exit(1)

        return response

    async def get_repo(self, repo: str, owner: str | None) -> httpx.Response:
        if not owner:
            if not self.config["default_owner"]:
                Text.error(
                    "You must specify a user OR set a default user with 'octotrack config set default_owner OWNERNAME' or 'octotrack repo default <owner/repo>"
                )
                exit(1)

            owner = self.config["default_owner"]

        return await self._get(f"/repos/{owner}/{repo}")

    async def get_readme(self, repo: str, owner: str | None) -> httpx.Response:
        if not owner:
            if not self.config["default_owner"]:
                Text.error(
                    "You must specify a user OR set a default user with 'octotrack config set default_owner OWNERNAME' or 'octotrack repo default <owner/repo>"
                )
                exit(1)

            owner = self.config["default_owner"]

        return await self._get(f"/repos/{owner}/{repo}/readme")

    async def get_contents(
        self, repo: str, owner: str, path: str | None, hidden: bool, depth: int
    ) -> list[RepositoryContent]:
        if not owner:
            if not self.config["default_owner"]:
                Text.error(
                    "You must specify a user OR set a default user with 'octotrack config set default_owner OWNERNAME' or 'octotrack repo default <owner/repo>"
                )
                exit(1)

            owner = self.config["default_owner"]

        elif depth < 0:
            Text.error("--depth cannot be less than 0")
            exit(1)

        content: list[RepositoryContent] = []

        response = await self._get(
            f"/repos/{owner}/{repo}/contents/{path}"
            if path
            else f"/repos/{owner}/{repo}/contents/"
        )
        json: list[dict] = response.json()

        for item in json:
            try:
                n_item = RepositoryContent.model_validate(item)

            except ValidationError:
                Text.error("Invalid file path (Check filename?).")
                exit(1)

            if not hidden and n_item.name.startswith("."):
                continue

            if n_item.type == "dir" and depth != 0:
                n_item.content = await self._get_content(
                    owner, repo, n_item.path, hidden, depth - 1
                )

            content.append(n_item)

        return content
