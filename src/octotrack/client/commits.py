import httpx
import os

from ..utils import load_config, Text, TOKEN_NAME
from ..core import load_github_token, GitHubTokenStatus

__all__ = ["CommitClient"]

class CommitClient:
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
    
    async def get_commit(self, owner: str, repo: str, commit: str | None = None) -> httpx.Response:
        response = await self._get(f"repos/{owner}/{repo}/commits/{commit}" if commit else f"repos/{owner}/{repo}/commits")
    
        return response