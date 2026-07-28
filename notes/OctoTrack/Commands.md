> Base command: `octotrack`

## Todos
- [x] Create Pydantic models for `octotrack repo info`
- [x] Create a display for models when commands like `octotrack repo info` are used
	- This might be temporary, depending on how I decided to handle themes
- [ ] Need to create Pydantic models for the rest of the `octotrack repo` commands
- [ ] Display models for the rest of the `octotrack repo` commands
---
- [ ] Start creating commands (structure) for commits, branches & tags, releases, issues, and pull requests
- [ ] Create models for commits, branches & tags, releases, issues, and pull requests
- [ ] Display models for commits, branches & tags, releases, issues, and pull requests
- [ ] [^2]Publish `v0.1.0`

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
| Command                                       | Description                                                              |
| --------------------------------------------- | ------------------------------------------------------------------------ |
| `octotrack repo default <owner/repo>`         | Set the default repository and / or owner quickly                        |
| `octotrack repo info <owner/repo>`            | [^1] General repository information                                      |
| `octotrack repo languages <owner/repo>`       | Breakdown of languages used                                              |
| `octotrack repo topics <owner/repo>`          | Repository topics / tags                                                 |
| `octotrack repo contents <owner/repo> <path>` | File / directory contents at a given ref                                 |
| `octotrack repo readme <owner/repo>`          | Get the repository's README.md                                           |
| `octotrack repo license <owner/repo>`         | Get the repository's LICENSE                                             |
| `octotrack repo permissions <owner/repo>`     | Get the permissions for the repository (based on your GitHub Auth Token) |


[^1]: General Repository Info includes
	-  Description
	-  Default Branch
	-  Visibility
	-  Size
	-  Stars / forks / watchers counts
	-  Homepage
	-  Archived
	-  Status
	-  Created at
	-  Updated at
	-  Pushed at

[^2]: Need to update / create the things listed below
	1. Update project `README.md`
	2. Updated `pyproject.toml`
	3. Create / update `requirements.txt`
	4. Create a workflow (for when a tag is created + pushed)
	5. ***PUSH*** workflow first, ***THEN*** tag it and push
