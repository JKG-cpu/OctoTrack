from datetime import datetime

from pydantic import BaseModel

__all__ = ["Issues", "Profile"]


class Profile(BaseModel):
    login: str
    html_url: str


class Issues(BaseModel):
    html_url: str

    user: Profile
    title: str
    state: str
    body: str
    number: int
    labels: list

    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None
    closed_by: Profile | None
