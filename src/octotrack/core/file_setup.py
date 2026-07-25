from pathlib import Path

from ..utils import (
    Text,
    setup_paths,
    validate_paths,
    remove_paths,
    DATA_DIR,
    CONFIG_DIR,
    CLI_NAME
)
from .config_handler import load_github_token
from .flags import GitHubTokenStatus

__all__ = ["setup", "validate", "remove"]


def setup() -> None:
    try:
        with Text.status("Setting Up Files and Directories...", style="bold cyan"):
            setup_paths()

        Text.success("Files and Directories Set Up!")
        Text.info(
            f"    - Data Directory: {DATA_DIR}\n    - Config Directory: {CONFIG_DIR}"
        )

    except Exception as e:
        Text.error(f"Error setting up files and directories: {e}")


def validate() -> None:
    try:
        with Text.status("Checking Files and Directories...", style="bold cyan"):
            paths: list[Path] = validate_paths()
            token_status: GitHubTokenStatus = load_github_token()

        if paths:
            Text.error("Not all paths exist... some may have been moved or deleted.")
            Text.info(f"Please run '{CLI_NAME} setup' to complete the path setup.")

        elif token_status == GitHubTokenStatus.INVALID_PATH:
            Text.error(
                f"A path for the config is missing. Please run '{CLI_NAME} setup' to complete the path setup."
            )

        else:
            Text.success("All files and directories are present.")
            if token_status == GitHubTokenStatus.TOKEN_SET:
                Text.success("GitHub token is set.")

            elif token_status == GitHubTokenStatus.TOKEN_NOT_SET:
                Text.info(
                    f"GitHub token is not set. Please run '{CLI_NAME} config --set-token'"
                )

    except Exception as e:
        Text.error(f"Error checking up files and directories: {e}")


def remove() -> None:
    try:
        confirm: str = Text.get_input(
            text="Are you sure you would like to remove all data and config files? (y/n)",
            style="bold yellow",
        )

        if confirm.lower().startswith("y"):
            with Text.status("Removing Files and Directories...", style="bold cyan"):
                remove_paths()

            Text.success(f"Removed all files and directories created by {CLI_NAME}.")

        elif confirm.lower().startswith("n"):
            Text.info("Canceled.")

    except Exception as e:
        Text.error(f"Error removing files and directories: {e}")
