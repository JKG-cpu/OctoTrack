from datetime import datetime

from pydantic import BaseModel

from .issues import Profile

__all__ = ["PRs"]


class PRs(BaseModel):
    html_url: str

    title: str
    user: Profile
    number: int
    state: str

    updated_at: datetime
