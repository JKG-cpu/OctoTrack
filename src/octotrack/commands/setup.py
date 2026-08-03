import typer

from ..core import stp, val, rm


__all__ = ["app"]

app = typer.Typer()


@app.callback(invoke_without_command=True, help="Run the setup command")
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        stp()


@app.command(help="Validate the current setup")
def validate() -> None:
    val()


@app.command(help="Remove the current setup")
def remove() -> None:
    rm()
