> Base command: `octotrack`
> Version command: `octotrack -v / --version`

## Setup

| Command                    | Description                 |
| -------------------------- | --------------------------- |
| `octotrack setup`          | First-time setup            |
| `octotrack setup remove`   | Remove configuration        |
| `octotrack setup validate` | Check installation is valid |

## Configuration
| Command                              | Description                                |
| ------------------------------------ | ------------------------------------------ |
| `octotrack config show`              | Show the current config                    |
| `octotrack config set-token`         | Set the GitHub Token, saved in a .env file |
| `octotrack config set <key> <value>` | Directly set key / value                   |
| `octotrack config clear <key>`       | Clear config OR value                      |
| `octotrack config path`              | Print Config Path                          |
### Config Settings
```json
CONFIG_SETTINGS = {
	"default_owner": None,
	"default_repo": None,
	"default_pr_state": "open" | "closed" | "all",
	"api_base_url": "https://api.github.com" | "https://github.mycompany.com/api/v3",
}
```

## Repository

| Command                                       | Description                                       |
| --------------------------------------------- | ------------------------------------------------- |
| `octotrack repo default <owner/repo>`         | Set the default repository and / or owner quickly |
| `octotrack repo info <owner/repo>`            | [^1] General repository information               |
| `octotrack repo contents <owner/repo> <path>` | File / directory contents at a given ref          |
| `octotrack repo readme <owner/repo>`          | Get the repository's README.md                    |

### Command Details / Layout

`octotrack repo contents <owner/repo> <path>`:
- `<owner/repo>` will function like the other commands
- `<path>` will be optional, it will show the top level of the GitHub repository
-  There will be some sub-commands for seeing less / more files, going through directories easily, max amount of sub folders visible.

Arguments Include:
- `<path>` *(optional)*
- `-h` / `--hidden`: Shows hidden files
- `-l` / `--list`: Shows files in a list format (like `ls -l /dir/`). Defaults to rich output
- `--depth`: Max amount of folders / files to display. Defaults to 3.

## Commits

| Command                               | Description                                 |
| ------------------------------------- | ------------------------------------------- |
| `octotrack commits show <owner/repo>` | Show commits for the current `<owner/repo>` |

Arguments Include:
- `-a` / `--all`: Show all the commits in the repository

## Branches + Tags

| Command                                    | Description                                                                     |
| ------------------------------------------ | ------------------------------------------------------------------------------- |
| `octotrack branches <owner/repo> <branch>` | Get the branches from a repository *or* view a single branch from a repository. |
| `octotrack tags <owner/repo>`              | Get the latest tags from a repository                                           |

### Command Details / Layout

`octotrack branches <owner/repo> <branch>`:
- `<owner/repo>` will function like the other commands
- `<branch>` will be optional, if you choose to view a branch, you can either type `-b <branch_name>` or `--branch <branch_name>`


## Releases

| Command                           | Description                                                                |
| --------------------------------- | -------------------------------------------------------------------------- |
| `octotrack releases <owner/repo>` | Gets the releases for the current repository (only 5 most recent releases) |

### Command Details / Layout
Arguments:
- pass `-all` to view all releases

[^1]: General Repository Info includes
	-  Description
	-  Default Branch
	-  Visibility
	-  Size
	-  Stars / forks / watchers counts
	-  Homepage
	-  Archived
	-  Created at
	-  Updated at
	-  Pushed at
	-  License (if available)
	-  Read me (if available)
