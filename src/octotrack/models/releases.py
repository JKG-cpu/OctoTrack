from datetime import datetime

from pydantic import BaseModel

__all__ = ["Releases"]


class ReleasesAuthor(BaseModel):
    login: str
    html_url: str


class Releases(BaseModel):
    url: str
    html_url: str

    author: ReleasesAuthor

    tag_name: str
    name: str
    body: str

    draft: bool
    prerelease: bool

    created_at: datetime
    updated_at: datetime
    published_at: datetime

