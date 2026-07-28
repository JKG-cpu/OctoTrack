from rich.theme import Theme

__all__ = ["OCTOTRACK_THEME"]

OCTOTRACK_THEME = Theme(
    {
        "repo.title": "bold cyan",
        "repo.owner": "blue",
        "repo.stats": "yellow",
        "repo.metadata": "green",
        "status.archived": "bold red",
        "status.visibility": "bold magenta",
        "label": "dim",
        "value": "default",
        "muted": "dim italic",
    }
)
