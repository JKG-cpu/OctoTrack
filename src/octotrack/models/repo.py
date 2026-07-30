from pydantic import BaseModel
from typing import Literal
from datetime import datetime

__all__ = [
    "RepositoryOwner",
    "RepositoryPermissions",
    "RepositoryLicense",
    "RepositoryReadme",
    "RepositoryInfo",
]


class RepositoryOwner(BaseModel):
    login: str
    id: int
    html_url: str
    type: str


class RepositoryPermissions(BaseModel):
    admin: bool = False
    maintain: bool = False
    pull: bool = False
    push: bool = False


class RepositoryLicense(BaseModel):
    key: str
    name: str
    url: str


class RepositoryReadme(BaseModel):
    content: str
    name: str


class RepositoryInfo(BaseModel):
    owner: RepositoryOwner
    full_name: str
    name: str
    html_url: str

    description: str | None = None
    language: str
    default_branch: str
    visibility: Literal["private", "public", "internal"]

    permissions: RepositoryPermissions
    license: RepositoryLicense | None = None
    readme: RepositoryReadme | None = None

    size: int

    stargazers_count: int
    forks: int
    watchers: int
    homepage: str | None = None

    archived: bool

    created_at: datetime
    updated_at: datetime
    pushed_at: datetime
