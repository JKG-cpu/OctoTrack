# For config settings
import typer

app = typer.Typer()

@app.command()
def show_config() -> None:
    print("Show config")

