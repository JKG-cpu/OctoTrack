from pydantic import BaseModel
from typing import Literal
from datetime import datetime

__all__ = ["RepositoryOwner", "RepositoryInfo"]


class RepositoryOwner(BaseModel):
    login: str
    id: int
    html_url: str
    type: str


class RepositoryInfo(BaseModel):
    owner: RepositoryOwner
    full_name: str
    name: str
    html_url: str
    description: str | None = None
    default_branch: str
    visibility: Literal["private", "public", "internal"]
    size: int
    stargazers_count: int
    forks: int
    watchers: int
    homepage: str | None = None
    archived: bool
    created_at: datetime
    updated_at: datetime
    pushed_at: datetime
