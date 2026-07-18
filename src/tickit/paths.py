from platformdirs import user_data_dir
from pathlib import Path

__all__ = ["DATA_DIR", "setup_paths", "validate_paths"]

APP_NAME = "Tickit"
APP_AUTHOR = "JKG-cpu"

DATA_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))


# Setup Function
def setup_paths() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def validate_paths() -> list[Path]:
    paths_missing = []

    for path in [DATA_DIR]:
        if not path.exists():
            paths_missing.append(path)

    return paths_missing
