import typer
from rich.progress import track

app = typer.Typer()


def f():
    print("Doing something")


@app.command()
def main():
    for value in track(range(100)):
        f()

    print("Done")


if __name__ == "__main__":
    app()
