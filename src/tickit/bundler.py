import typer

from .core import stp, val, rm, ConfigKey, edit_config, edit_github_token

app = typer.Typer()


# Setup Commands
# region
@app.command()
def setup(
    validate: bool = typer.Option(
        False, "--validate", help="Validate required folders and files exist."
    ),
    remove: bool = typer.Option(
        False,
        "--remove",
        "-r",
        help="Remove all the folders and files created by ticket.",
    ),
) -> None:
    if validate:
        val()

    elif remove:
        rm()

    else:
        stp()


# endregion


# Config Commands
# region
config_app = typer.Typer()
app.add_typer(config_app, name="config")


@config_app.callback(invoke_without_command=True)
def config_main(
    ctx: typer.Context,
    show: bool = typer.Option(False, "--show", help="Show the current config."),
    change_token: bool = typer.Option(
        False, "--set-token", "-s", help="Set your GitHub token."
    ),
) -> None:
    if show:
        print("Show Config")

    elif change_token:
        edit_github_token()

    elif ctx.invoked_subcommand is None:
        print(ctx.get_help())


@config_app.command()
def edit(key: ConfigKey, value: str) -> None:
    edit_config(key, value)


# endregion
