# For setting up paths
import typer
from pathlib import Path

from ..paths import setup_paths, validate_paths, DATA_DIR
from ..global_vars import Text


app = typer.Typer()


# Commands
@app.command()
def paths() -> None:
    stp()

@app.command()
def validate() -> None:
    # Check if all the setup paths, config, etc are all setup. Return anything that isn't
    with Text.status("Checking Folders and Files...", style = "bold cyan"): 
        paths: list[Path] = validate_paths()

    if paths:
        Text.error("Not all paths are created, some may have been moved / destroyed.")
        Text.info("Please run 'tickit setup paths'")

    else:
        Text.success("All Files and Folders are properly setup and created!")

# Functions
def stp() -> None:
    with Text.status("Creating Folders and Files...", style = "bold cyan"):
        setup_paths()

    Text.success(f"Created Folders and Files at {DATA_DIR}!")


