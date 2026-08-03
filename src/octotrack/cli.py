import typer

from .commands import setup_app, config_app, repo_app

__all__ = ["app"]

app = typer.Typer()
app.add_typer(setup_app, name="setup")
app.add_typer(config_app, name="config", help="Run config commands")
app.add_typer(repo_app, name="repo", help="Run repository related commands")
