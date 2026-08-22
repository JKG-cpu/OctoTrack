import json
import sys
from pathlib import Path
from shutil import rmtree

from platformdirs import user_config_dir, user_data_dir

from .global_vars import CONFIG_SETTINGS, Text

__all__ = [
    "CONFIG_DIR",
    "CONFIG_SETTINGS_PATH",
    "DATA_DIR",
    "ENV_PATH",
    "load_config",
    "remove_paths",
    "save_config",
    "setup_paths",
    "validate_paths",
]

APP_NAME = "OctoTrack"
APP_AUTHOR = "JKG-cpu"

DATA_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))

CONFIG_DIR = Path(user_config_dir(APP_NAME, APP_AUTHOR))
ENV_PATH = CONFIG_DIR / ".env"
CONFIG_SETTINGS_PATH = CONFIG_DIR / "settings.json"


# Setup Functions
def setup_paths() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    ENV_PATH.touch(exist_ok=True)

    if not CONFIG_SETTINGS_PATH.exists():
        with open(CONFIG_SETTINGS_PATH, "w") as f:
            json.dump(CONFIG_SETTINGS, f, indent=4)
    else:
        with open(CONFIG_SETTINGS_PATH, "r") as f:
            data: dict = json.load(f)

        if not isinstance(data, dict):
            with open(CONFIG_SETTINGS_PATH, "w") as f:
                json.dump(CONFIG_SETTINGS, f, indent=4)

        else:
            if data.keys() != CONFIG_SETTINGS.keys():
                with open(CONFIG_SETTINGS_PATH, "w") as f:
                    json.dump(CONFIG_SETTINGS, f, indent=4)


def validate_paths() -> list[Path]:
    paths_missing = []

    for path in [DATA_DIR]:
        if not path.exists():
            paths_missing.append(path)

    return paths_missing


def remove_paths() -> None:
    rmtree(DATA_DIR)
    rmtree(CONFIG_DIR)


# Load / Save functions
def load_config() -> dict:
    if not CONFIG_SETTINGS_PATH.exists():
        Text.error(
            "Data in config file changed or corrupted. Please run 'octotrack setup'"
        )
        sys.exit(1)

    with open(CONFIG_SETTINGS_PATH, "r") as f:
        data = json.load(f)

    if not isinstance(data, dict) or data.keys() != CONFIG_SETTINGS.keys():
        Text.error(
            "Data in config file changed or corrupted. Please run 'octotrack setup'"
        )
        sys.exit(1)

    return data


def save_config(config: dict) -> None:
    with open(CONFIG_SETTINGS_PATH, "w") as f:
        json.dump(config, f)
