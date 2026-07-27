> Base command: `octotrack`

## Todos
- [x] Create all the setup commands
- [x] Add the functions for the setup commands
- [x] Create all the config commands
- [x] Add the functions for the config commands
- [x] Create all the repository metadata commands
- [x] Add the functions for the repository metadata commands
- [ ] Allow clearing / resetting config values

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
| `octotrack repo languages <owner/repo>`       | Breakdown of languages used                       |
| `octotrack repo topics <owner/repo>`          | Repository topics / tags                          |
| `octotrack repo contents <owner/repo> <path>` | File / directory contents at a given ref          |
| `octotrack repo readme <owner/repo>`          | Get the repository's README.md                    |
| `octotrack repo license <owner/repo>`         | Get the repository's LICENSE                      |


[^1]: General Repository Info includes
	-  Description
	-  Default Branch
	-  Visibility
	-  Size
	-  Stars / forks / watchers counts
	-  License
	-  Topics
	-  Homepage
	-  Archived
	-  Status
	-  Created at
	-  Updated at
	-  Pushed at
