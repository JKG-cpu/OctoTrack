import json

import pytest

from octotrack.utils.global_vars import CONFIG_SETTINGS


@pytest.fixture
def fake_config() -> dict:
    """A fresh copy of the default config settings for each test."""
    return dict(CONFIG_SETTINGS)


@pytest.fixture
def isolated_config_paths(tmp_path, monkeypatch):
    """
    Points CONFIG_SETTINGS_PATH / ENV_PATH at a temp directory so tests
    never touch the real user config on disk, and pre-seeds a valid
    settings.json so load_config() doesn't error out.
    """
    from octotrack.utils import paths as paths_module
    from octotrack.core import config_handler as config_handler_module

    config_path = tmp_path / "settings.json"
    env_path = tmp_path / ".env"

    config_path.write_text(json.dumps(CONFIG_SETTINGS))
    env_path.touch()

    # paths.py owns the module-level globals that load_config/save_config
    # actually read from.
    monkeypatch.setattr(paths_module, "CONFIG_SETTINGS_PATH", config_path)
    monkeypatch.setattr(paths_module, "ENV_PATH", env_path)

    # config_handler.py did `from ..utils import ENV_PATH`, which bound its
    # own copy of the name at import time, so it needs patching separately.
    monkeypatch.setattr(config_handler_module, "ENV_PATH", env_path)

    return {"config_path": config_path, "env_path": env_path}
