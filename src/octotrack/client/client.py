import asyncio
import os
import sys
from urllib.parse import parse_qs, urlparse

import httpx
from pydantic import ValidationError

from ..core import GitHubTokenStatus, load_github_token
from ..models import RepositoryContent
from ..utils import TOKEN_NAME, Text, load_config

__all__ = ["Client"]


class Client:
    def __init__(self) -> None:
        self._load_token()
        self.config: dict = load_config()

        self.client = httpx.AsyncClient(
            base_url=self.config["api_base_url"], headers=self._load_headers()
        )

    # Helpers
    def _load_token(self) -> None:
        status = load_github_token()

        if status == GitHubTokenStatus.INVALID_PATH:
            Text.error("Not all paths exist... some may have been moved or deleted.")
            Text.info("Please run 'octotrack setup' to complete the path setup.")
            sys.exit(1)

        elif status == GitHubTokenStatus.TOKEN_NOT_SET:
            Text.warning(
                "[!] GitHub token not set. Run 'octotrack config set-token' to set a GitHub Auth Token."
            )
            sys.exit(1)

    def _load_headers(self) -> dict:
        return {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {os.environ.get(TOKEN_NAME)}",
            "User-Agent": "OctoTrack",
        }

    # Base Get Method
    async def _get(self, path: str, params: dict | None = None) -> httpx.Response:
        response = await self.client.get(path, params=params)

        self.rate_remaining = int(response.headers.get("x-ratelimit-remaining", 0))
        self.rate_reset = int(response.headers.get("x-ratelimit-reset", 0))

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            Text.error(f"Error when getting path: {path}. Error: \n{e}")
            sys.exit(1)

        return response

    # Repo
    # region
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

    async def get_repo(self, repo: str, owner: str | None) -> httpx.Response:
        if not owner:
            if not self.config["default_owner"]:
                Text.error(
                    "You must specify a user OR set a default user with 'octotrack config set default_owner OWNERNAME' or 'octotrack repo default <owner/repo>"
                )
                sys.exit(1)

            owner = self.config["default_owner"]

        return await self._get(f"/repos/{owner}/{repo}")

    async def get_readme(self, repo: str, owner: str | None) -> httpx.Response:
        if not owner:
            if not self.config["default_owner"]:
                Text.error(
                    "You must specify a user OR set a default user with 'octotrack config set default_owner OWNERNAME' or 'octotrack repo default <owner/repo>"
                )
                sys.exit(1)

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
                sys.exit(1)

            owner = self.config["default_owner"]

        elif depth < 0:
            Text.error("--depth cannot be less than 0")
            sys.exit(1)

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
                sys.exit(1)

            if not hidden and n_item.name.startswith("."):
                continue

            if n_item.type == "dir" and depth != 0:
                n_item.content = await self._get_content(
                    owner, repo, n_item.path, hidden, depth - 1
                )

            content.append(n_item)

        return content

    # Commits
    async def get_commit(
        self, owner: str, repo: str, commit: str | None = None
    ) -> httpx.Response:
        response = await self._get(
            f"repos/{owner}/{repo}/commits/{commit}"
            if commit
            else f"repos/{owner}/{repo}/commits"
        )

        return response

    # endregion

    # Branches
    # region
    async def get_branches(self, owner: str, repo: str) -> httpx.Response:
        response = await self._get(f"repos/{owner}/{repo}/branches")

        return response

    async def get_branch(self, owner: str, repo: str, branch: str) -> httpx.Response:
        response = await self._get(f"repos/{owner}/{repo}/branches/{branch}")

        return response

    # endregion

    # Tags
    # region
    async def get_tags(self, owner: str, repo: str) -> httpx.Response:
        response = await self._get(f"repos/{owner}/{repo}/tags")

        return response

    # endregion

    # Releases
    # region
    async def get_releases(self, owner: str, repo: str) -> httpx.Response:
        response = await self._get(f"repos/{owner}/{repo}/releases")

        return response

    # endregion

    # Issues
    # region
    async def get_issues(self, owner: str, repo: str, state: str = "all") -> list[dict]:
        response = await self._get(
            f"repos/{owner}/{repo}/issues", {"per_page": 100, "state": state}
        )

        results = response.json()

        last_link = response.links.get("last")
        if not last_link:
            return results

        last_page = int(parse_qs(urlparse(last_link["url"]).query()["page"][0]))

        tasks = [
            self._get(
                f"repos/{owner}/{repo}/issues",
                {"per_page": 100, "state": state, "page": page},
            )
            for page in range(2, last_page + 1)
        ]
        responses = await asyncio.gather(*tasks)

        for r in responses:
            results.extend(r.json())

        return response

    # endregion

    # PRs
    # region
    async def get_prs(self, owner: str, repo: str, state: str) -> list[dict]:
        response = await self._get(
            f"repos/{owner}/{repo}/pulls",
            {"per_page": 100, "state": state}
        )

        results = response.json()

        last_link = response.links.get("last")
        if not last_link:
            return results

        last_page = int(parse_qs(urlparse(last_link["url"]).query()["page"][0]))

        tasks = [
            self._get(
                f"repos/{owner}/{repo}/pulls",
                {"per_page": 100, "state": state, "page": page},
            )
            for page in range(2, last_page + 1)
        ]

        responses = await asyncio.gather(*tasks)

        for r in responses:
            results.extend(r.json())

        return response

    #endregion
