import httpx
import os

from ..utils import load_config, Text, TOKEN_NAME
from ..core import load_github_token, GitHubTokenStatus


class GitHubClient:
    def __init__(self) -> None:
        self._load_token()
        self.config: dict = load_config()

        self.httpx_client = httpx.AsyncClient(
            base_url=self.config["api_base_url"], headers=self._load_headers()
        )

    def _load_token(self) -> None:
        status = load_github_token()

        if status == GitHubTokenStatus.INVALID_PATH:
            Text.error("Not all paths exist... some may have been moved or deleted.")
            Text.info("Please run 'ghtickit setup' to complete the path setup.")
            exit(1)

        elif status == GitHubTokenStatus.TOKEN_NOT_SET:
            Text.warning(
                "[!] GitHub token not set. Run 'ghtickit config --setup-token' to set a GitHub Auth Token."
            )
            exit(1)

    def _load_headers(self) -> dict:
        return {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {os.environ.get(TOKEN_NAME)}",
            "User-Agent": "ghticket",
        }

    async def _get(self, path: str, **params) -> httpx.Response:
        response = await self.httpx_client.get(path, params=params)

        self.rate_remaining = int(response.headers.get("x-ratelimit-remaining", 0))
        self.rate_reset = int(response.headers.get("x-ratelimit-reset", 0))

        response.raise_for_status()
        return response

    async def get_repo(self, repo: str, user: str | None = None) -> httpx.Response:
        if not user:
            if not self.config["default_owner"]:
                Text.error(
                    "You must specify a user OR set a default user with 'ghtickit config edit default_owner OWNERNAME'"
                )
                exit(1)

            user = self.config["default_owner"]

        return await self._get(f"/repos/{user}/{repo}")
