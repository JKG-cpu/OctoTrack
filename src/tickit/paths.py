from platformdirs import user_data_dir, user_config_dir
from pathlib import Path
from shutil import rmtree

__all__ = ["DATA_DIR", "setup_paths", "validate_paths", "remove_paths"]

APP_NAME = "Tickit"
APP_AUTHOR = "JKG-cpu"

DATA_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
CONFIG_DIR = Path(user_config_dir(APP_NAME, APP_AUTHOR))
ENV_PATH = CONFIG_DIR / ".env"


# Setup Functions
def setup_paths() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    ENV_PATH.touch(exist_ok=True)


def validate_paths() -> list[Path]:
    paths_missing = []

    for path in [DATA_DIR]:
        if not path.exists():
            paths_missing.append(path)

    return paths_missing


def remove_paths() -> None:
    rmtree(DATA_DIR)
    rmtree(CONFIG_DIR)
