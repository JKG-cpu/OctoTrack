import pytest
import typer

from octotrack.commands.repo import _parse_owner_repo


def test_explicit_owner_and_repo_ignores_config(fake_config):
    fake_config["default_owner"] = "should-not-be-used"
    fake_config["default_repo"] = "should-not-be-used"

    owner, repo = _parse_owner_repo("JKG-cpu/OctoTrack", fake_config)

    assert owner == "JKG-cpu"
    assert repo == "OctoTrack"


def test_bare_value_is_treated_as_repo_not_owner(fake_config):
    # A single value with no "/" is always interpreted as the repo name,
    # never the owner -- owner must come from config in this case. This
    # means there's currently no "owner-only" shorthand.
    fake_config["default_owner"] = None
    fake_config["default_repo"] = "should-not-be-used"

    with pytest.raises(typer.Exit):
        _parse_owner_repo("JKG-cpu", fake_config)


def test_repo_only_uses_default_owner(fake_config):
    fake_config["default_owner"] = "JKG-cpu"

    owner, repo = _parse_owner_repo("OctoTrack", fake_config)

    assert owner == "JKG-cpu"
    assert repo == "OctoTrack"


def test_no_value_uses_both_defaults(fake_config):
    fake_config["default_owner"] = "JKG-cpu"
    fake_config["default_repo"] = "OctoTrack"

    owner, repo = _parse_owner_repo(None, fake_config)

    assert owner == "JKG-cpu"
    assert repo == "OctoTrack"


def test_no_value_and_no_default_owner_exits(fake_config):
    fake_config["default_owner"] = None
    fake_config["default_repo"] = "OctoTrack"

    with pytest.raises(typer.Exit):
        _parse_owner_repo(None, fake_config)


def test_no_value_and_no_default_repo_exits(fake_config):
    fake_config["default_owner"] = "JKG-cpu"
    fake_config["default_repo"] = None

    with pytest.raises(typer.Exit):
        _parse_owner_repo(None, fake_config)


def test_value_without_slash_and_no_default_owner_exits(fake_config):
    # A bare value with no "/" is treated as the repo name, so this still
    # needs a default_owner configured or it should exit.
    fake_config["default_owner"] = None
    fake_config["default_repo"] = None

    with pytest.raises(typer.Exit):
        _parse_owner_repo("just-a-name-no-slash", fake_config)
