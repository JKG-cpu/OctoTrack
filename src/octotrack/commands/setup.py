import typer

from ..core import stp, val, rm


__all__ = ["app"]

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        stp()


@app.command()
def validate() -> None:
    val()


@app.command()
def remove() -> None:
    rm()
