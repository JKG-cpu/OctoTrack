from pydantic import BaseModel

from .commits import Commit, CommitTree

__all__ = ["Branch", "SimpleBranch"]


class SimpleBranch(BaseModel):
    name: str
    commit: CommitTree
    protected: bool
    commit_message: str = ""


class Branch(BaseModel):
    name: str
    sha: str | None = None
    commit: Commit

    protected: bool
