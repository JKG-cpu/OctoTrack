from enum import Enum, auto

__all__ = ["GitHubTokenStatus"]


class GitHubTokenStatus(Enum):
    INVALID_PATH = auto()
    TOKEN_NOT_SET = auto()
    TOKEN_SET = auto()
