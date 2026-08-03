import os
import stat
from enum import Enum
from getpass import getpass
from dotenv import load_dotenv

from ..utils import (
    Text,
    TOKEN_NAME,
    ENV_PATH,
    load_config,
    save_config,
    CONFIG_SETTINGS,
)
from .flags import GitHubTokenStatus

__all__ = [
    "ConfigKey",
    "set_github_token",
    "edit_config",
    "show_config",
    "load_github_token",
    "clear",
]


class ConfigKey(str, Enum):
    default_owner = "default_owner"
    default_repo = "default_repo"
    default_pr_state = "default_pr_state"
    api_base_url = "api_base_url"


# GitHub Token
# region
def load_github_token() -> GitHubTokenStatus:
    if ENV_PATH.exists():
        load_dotenv(ENV_PATH)

        # Check for token
        if os.environ.get(TOKEN_NAME):
            return GitHubTokenStatus.TOKEN_SET

        return GitHubTokenStatus.TOKEN_NOT_SET

    else:
        return GitHubTokenStatus.INVALID_PATH


def save_github_token(token: str) -> None:
    ENV_PATH.write_text(f"{TOKEN_NAME}={token}\n")
    ENV_PATH.chmod(stat.S_IRUSR | stat.S_IWUSR)


def set_github_token() -> None:
    Text.text("Enter in your GitHub token: ", style="text.base_text", end="")
    token = getpass("").strip()

    save_github_token(token)

    Text.success("GitHub token saved.")


# endregion


# GitHub Config
# region
def edit_config(key: ConfigKey, value: str) -> None:
    with Text.status(f"Changing '{key}' in config...", style="text.base_text"):
        config_settings = load_config()
        config_settings[key] = value
        save_config(config_settings)

    Text.success("Change successful")


def show_config() -> None:
    config_settings = load_config()

    Text.text("--- Config Settings ---", style="text.header")

    for name, value in config_settings.items():
        Text.text(f"{name}: {value}", style="text.base_text")

    print()


def clear(key: ConfigKey | None) -> None:
    if key:
        config_settings = load_config()
        config_settings[key] = CONFIG_SETTINGS[key]
        save_config(config_settings)

    else:
        save_config(CONFIG_SETTINGS)

    Text.info("Change successful.")


# endregion
