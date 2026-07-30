import json

import pytest

from octotrack.core import ConfigKey, edit_config, load_github_token
from octotrack.core.flags import GitHubTokenStatus
from octotrack.utils import load_config, save_config, CONFIG_SETTINGS


def test_load_config_returns_defaults(isolated_config_paths):
    config = load_config()
    assert config == CONFIG_SETTINGS


def test_save_then_load_round_trips(isolated_config_paths):
    updated = dict(CONFIG_SETTINGS)
    updated["default_owner"] = "JKG-cpu"

    save_config(updated)

    assert load_config()["default_owner"] == "JKG-cpu"


def test_load_config_exits_on_missing_file(isolated_config_paths):
    isolated_config_paths["config_path"].unlink()

    with pytest.raises(SystemExit):
        load_config()


def test_load_config_exits_on_corrupted_keys(isolated_config_paths):
    isolated_config_paths["config_path"].write_text(json.dumps({"unexpected_key": 1}))

    with pytest.raises(SystemExit):
        load_config()


def test_edit_config_updates_single_key(isolated_config_paths):
    edit_config(ConfigKey.default_owner, "JKG-cpu")

    config = load_config()
    assert config[ConfigKey.default_owner] == "JKG-cpu"
    # Other keys should be untouched.
    assert config["default_repo"] is None


def test_load_github_token_invalid_path_when_env_missing(isolated_config_paths):
    isolated_config_paths["env_path"].unlink()

    assert load_github_token() == GitHubTokenStatus.INVALID_PATH


def test_load_github_token_not_set_when_env_empty(isolated_config_paths, monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    assert load_github_token() == GitHubTokenStatus.TOKEN_NOT_SET


def test_load_github_token_set_when_env_has_token(isolated_config_paths, monkeypatch):
    isolated_config_paths["env_path"].write_text("GITHUB_TOKEN=abc123\n")
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    assert load_github_token() == GitHubTokenStatus.TOKEN_SET
