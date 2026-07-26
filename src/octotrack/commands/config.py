import typer

from ..core import ConfigKey, edit_config, show_config, edit_github_token
from ..utils import Text, CONFIG_SETTINGS_PATH

__all__ = ["app"]

app = typer.Typer()


@app.command()
def show() -> None:
    show_config()


@app.command(name="edit-token")
def edit_token() -> None:
    edit_github_token()


@app.command(name="set")
def set_config(key: ConfigKey, value: str) -> None:
    edit_config(key, value)


@app.command()
def path() -> None:
    Text.info(f"Config Path: {CONFIG_SETTINGS_PATH}")
