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
        "status.success": "bold green",
        "status.error": "bold red",
        "status.warning": "bold yellow",
        "status.info": "bold cyan",
        "text.base_text": "bold white",
        "text.header": "bold cyan",
        "label": "dim",
        "value": "default",
        "muted": "dim italic",
    }
)
