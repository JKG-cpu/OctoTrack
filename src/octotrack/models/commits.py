from datetime import datetime

from pydantic import BaseModel

__all__ = ["Commit", "CommitAuthor", "CommitDetails", "CommitTree"]


class CommitAuthor(BaseModel):
    date: datetime
    email: str
    name: str


class CommitTree(BaseModel):
    sha: str
    url: str


class CommitDetails(BaseModel):
    committer: CommitAuthor
    message: str
    tree: CommitTree
    url: str


class Commit(BaseModel):
    commit: CommitDetails
    sha: str
    url: str
