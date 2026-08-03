import base64

import httpx
import pytest
import respx

from octotrack.client.repo import RepoClient
from octotrack.core.flags import GitHubTokenStatus

API_BASE = "https://api.github.com"


@pytest.fixture
def repo_client(isolated_config_paths, monkeypatch):
    """
    A RepoClient with the token check short-circuited (so __init__ doesn't
    exit) and pointed at the isolated test config.
    """
    monkeypatch.setattr(
        "octotrack.client.repo.load_github_token",
        lambda: GitHubTokenStatus.TOKEN_SET,
    )
    monkeypatch.setenv("GITHUB_TOKEN", "fake-token-for-tests")

    return RepoClient()


def _sample_repo_payload(**overrides) -> dict:
    payload = {
        "owner": {
            "login": "JKG-cpu",
            "id": 1,
            "html_url": "https://github.com/JKG-cpu",
            "type": "User",
        },
        "full_name": "JKG-cpu/OctoTrack",
        "name": "OctoTrack",
        "html_url": "https://github.com/JKG-cpu/OctoTrack",
        "description": "An async CLI for tracking GitHub repos.",
        "language": "Python",
        "default_branch": "main",
        "visibility": "public",
        "permissions": {"admin": False, "maintain": False, "pull": True, "push": False},
        "license": None,
        "size": 128,
        "stargazers_count": 3,
        "forks": 1,
        "watchers": 3,
        "homepage": None,
        "archived": False,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-02-01T00:00:00Z",
        "pushed_at": "2026-02-01T00:00:00Z",
    }
    payload.update(overrides)
    return payload


@respx.mock
def test_get_repo_returns_response_for_explicit_owner(repo_client):
    route = respx.get(f"{API_BASE}/repos/JKG-cpu/OctoTrack").mock(
        return_value=httpx.Response(200, json=_sample_repo_payload())
    )

    response = _run(repo_client.get_repo("OctoTrack", "JKG-cpu"))

    assert route.called
    assert response.json()["full_name"] == "JKG-cpu/OctoTrack"


@respx.mock
def test_get_repo_falls_back_to_default_owner(repo_client):
    repo_client.config["default_owner"] = "JKG-cpu"

    route = respx.get(f"{API_BASE}/repos/JKG-cpu/OctoTrack").mock(
        return_value=httpx.Response(200, json=_sample_repo_payload())
    )

    response = _run(repo_client.get_repo("OctoTrack", None))

    assert route.called
    assert response.json()["name"] == "OctoTrack"


def test_get_repo_exits_without_owner_or_default(repo_client):
    repo_client.config["default_owner"] = None

    with pytest.raises(SystemExit):
        _run(repo_client.get_repo("OctoTrack", None))


@respx.mock
def test_get_readme_decodes_base64_content(repo_client):
    encoded = base64.b64encode(b"# OctoTrack\n\nTrack your repos.").decode("utf-8")

    respx.get(f"{API_BASE}/repos/JKG-cpu/OctoTrack/readme").mock(
        return_value=httpx.Response(200, json={"name": "README.md", "content": encoded})
    )

    response = _run(repo_client.get_readme("OctoTrack", "JKG-cpu"))
    decoded = base64.b64decode(response.json()["content"]).decode("utf-8")

    assert decoded == "# OctoTrack\n\nTrack your repos."


@respx.mock
def test_get_request_exits_on_http_error(repo_client):
    respx.get(f"{API_BASE}/repos/JKG-cpu/missing-repo").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )

    with pytest.raises(SystemExit):
        _run(repo_client.get_repo("missing-repo", "JKG-cpu"))


@respx.mock
def test_get_contents_skips_hidden_files_by_default(repo_client):
    respx.get(f"{API_BASE}/repos/JKG-cpu/OctoTrack/contents/").mock(
        return_value=httpx.Response(
            200,
            json=[
                {"name": "README.md", "path": "README.md", "size": 100, "type": "file"},
                {
                    "name": ".gitignore",
                    "path": ".gitignore",
                    "size": 20,
                    "type": "file",
                },
            ],
        )
    )

    contents = _run(
        repo_client.get_contents("OctoTrack", "JKG-cpu", None, hidden=False, depth=0)
    )

    names = [item.name for item in contents]
    assert "README.md" in names
    assert ".gitignore" not in names


@respx.mock
def test_get_contents_includes_hidden_files_when_requested(repo_client):
    respx.get(f"{API_BASE}/repos/JKG-cpu/OctoTrack/contents/").mock(
        return_value=httpx.Response(
            200,
            json=[
                {"name": "README.md", "path": "README.md", "size": 100, "type": "file"},
                {
                    "name": ".gitignore",
                    "path": ".gitignore",
                    "size": 20,
                    "type": "file",
                },
            ],
        )
    )

    contents = _run(
        repo_client.get_contents("OctoTrack", "JKG-cpu", None, hidden=True, depth=0)
    )

    names = {item.name for item in contents}
    assert names == {"README.md", ".gitignore"}


def _run(coro):
    """Small helper so tests can stay plain `def` instead of async def."""
    import asyncio

    return asyncio.run(coro)
