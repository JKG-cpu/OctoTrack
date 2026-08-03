import typer

from ..core import ConfigKey, edit_config, show_config, set_github_token, clear
from ..utils import Text, CONFIG_SETTINGS_PATH

__all__ = ["app"]

app = typer.Typer()


@app.command(help="Show the current config settings")
def show() -> None:
    show_config()


@app.command(name="set-token", help="Set your GitHub Authentication token")
def set_token() -> None:
    set_github_token()


@app.command(name="githubtoken-help", help="An explanation on how to create a GitHub Authentication Token")
def show_help() -> None:
    pass


@app.command(name="set", help="Set a config value")
def set_config(key: ConfigKey, value: str) -> None:
    edit_config(key, value)


@app.command(name="clear", help="Clear the current config")
def cls(
    key: ConfigKey = typer.Option(
        None, "--key", "-k", help="Clear a setting in the config OR clear all config"
    ),
) -> None:
    clear(key)


@app.command(help="Get the current config path")
def path() -> None:
    Text.info(f"Config Path: {CONFIG_SETTINGS_PATH}")
