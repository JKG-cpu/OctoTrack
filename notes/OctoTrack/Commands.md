> Base command: `octotrack`

## Todos
- [x] Create Pydantic models for `octotrack repo info`
- [x] Create a display for models when commands like `octotrack repo info` are used
	- This might be temporary, depending on how I decided to [^3]handle themes
- [x] Need to create Pydantic models for the rest of the `octotrack repo` commands + Display models for the rest of the `octotrack repo` commands
	- [x] `octotrack repo readme <owner/repo>`
	- [x] `octotrack repo contents <owner/repo> <path>`
- [x] Run a few tests (configured by Claude)
- [ ] [^2]Publish `v0.1.0`
---
- [ ] Start creating commands (structure) for commits, branches & tags, releases, issues, and pull requests
- [ ] Create models for commits, branches & tags, releases, issues, and pull requests
- [ ] Display models for commits, branches & tags, releases, issues, and pull requests
- [ ] [^2]Publish `v0.2.0`

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
### Metadata
| Command                                       | Description                                       |
| --------------------------------------------- | ------------------------------------------------- |
| `octotrack repo default <owner/repo>`         | Set the default repository and / or owner quickly |
| `octotrack repo info <owner/repo>`            | [^1] General repository information               |
| `octotrack repo contents <owner/repo> <path>` | File / directory contents at a given ref          |
| `octotrack repo readme <owner/repo>`          | Get the repository's README.md                    |

## Command Details / Layout

`octotrack repo contents <owner/repo> <path>`:
- `<owner/repo>` will function like the other commands
- `<path>` will be optional, it will show the top level of the GitHub repository
-  There will be some sub-commands for seeing less / more files, going through directories easily, max amount of sub folders visible.

Arguments Include:
- `<path>` *(optional)*
- `-h` / `--hidden`: Shows hidden files
- `-l` / `--list`: Shows files in a list format (like `ls -l /dir/`). Defaults to rich output
- `--depth`: Max amount of folders / files to display. Defaults to 3.


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

[^2]: Need to update / create the things listed below
	1. Update project `README.md`
	2. Updated `pyproject.toml`
	3. Create / update `requirements.txt`
	4. Create / update a workflow (for when a tag is created + pushed)
	5. ***PUSH*** workflow first, ***THEN*** tag it and push

[^3]: Changing themes / colors will be implemented in a different version, not `v0.1.0` or `v0.2.0`. Maybe `v0.3.0`.
