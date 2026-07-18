import typer

from .commands import config_app, setup_app


app = typer.Typer()

app.add_typer(config_app, name = "config")
app.add_typer(setup_app, name = "setup")
