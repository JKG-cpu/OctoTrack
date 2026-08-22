import typer

from .commands import branch_app, commit_app, config_app, repo_app, setup_app, tag_app

__all__ = ["app"]

app = typer.Typer()
app.add_typer(
    branch_app,
    name="branches",
    help="Get one or all the branches of a commit repository",
)
app.add_typer(commit_app, name="commits", help="Get the commits for a repository")
app.add_typer(config_app, name="config", help="Run config commands")
app.add_typer(repo_app, name="repo", help="Run repository related commands")
app.add_typer(setup_app, name="setup")
app.add_typer(tag_app, name="tags", help="View the latest tags for a repository")
