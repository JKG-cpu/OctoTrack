from pydantic import BaseModel
from datetime import datetime


__all__ = ["CommitAuthor", "CommitTree", "CommitDetails", "Commit"]


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
