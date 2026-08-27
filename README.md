![OctoTrack](docs/images/octotrack_banner.png)

An Async API CLI Client for GitHub that can be used to track things like from GitHub Repositories like Releases, Pull Requests, Issues, and more!

OctoTrack uses the GitHub REST API Client to get any repository information needed.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
  - [`branches`](#branches)
  - [`commits`](#commits)
  - [`config`](#config)
  - [`issues`](#issues)
  - [`pr`](#pr)
  - [`releases`](#releases)
  - [`repo`](#repo)
  - [`setup`](#setup)
  - [`tags`](#tags)
- [Configuration](#configuration)
- [License](#license)

## Installation

Install via pip:

```bash
pip install octotrack
```

Requires Python 3.13+.

## Quick Start

```bash
# One-time setup: creates config/data directories
octotrack setup

# Add a GitHub personal access token
octotrack config set-token

# Set a default repo so you don't have to type it every time
octotrack repo default JKG-cpu/OctoTrack

# Pull general info on a repo
octotrack repo info
```

## Commands

Below is a list of all the OctoTrack commands. If you ever get stuck or just found some new command, run `octotrack <command> --help` or go check the documentation on (GitHub Pages)[https://jkg-cpu.github.io/OctoTrack/].

For any command that has an `owner/repo` option, if you choose not to provide one, it will fall back to whatever you set in the config. You can run `octotrack config set default_owner OWNER` and `octotrack config set default_repo REPO` to set a default.

### `branches`

Grabs all the branches for a repository.

| Command                           | Description                                       |
| --------------------------------- | ------------------------------------------------- |
| `octotrack branches [owner/repo]` | Get on or all the branches of a commit repository |

| Flag           | Description                                    |
| -------------- | ---------------------------------------------- |
| `-b, --branch` | Choose a branch to see (will output more text) |

### `commits`

Get the commits for a repository.

| Command | Description |
|---|---|
| `octotrack commits [owner/repo]` | Shows the commits for the current repository |

| Flag | Description |
|---|---|
| `-a, --all` | List every single commit |

### `config`

Reads and writes local configuration, including your GitHub token.

| Command | Description |
|---|---|
| `octotrack config show` | Prints all current config values. |
| `octotrack config set-token` | Prompts for a GitHub token and stores it as a local environment variable. Never written to the config file. |
| `octotrack config set <key> <value>` | Sets a config value directly. Valid keys: `default_owner`, `default_repo`, `default_pr_state`, `api_base_url`. |
| `octotrack config clear [--key/-k <key>]` | Resets a single config key to its default. Omit `--key` to reset the entire config. |
| `octotrack config path` | Prints the path to the config settings file. |
| `octotrack config github-token-help` | An explanation on how to create a GitHub Authentication Token |

### `issues`

Get all the issues for a repository.

| Command                         | Description                  |
| ------------------------------- | ---------------------------- |
| `octotrack issues [owner/repo]` | View Issues for a repository |

| Flags     | Description                                                                              |
| --------- | ---------------------------------------------------------------------------------------- |
| `--state` | Define a state to use to filter issues (default: all). Options: `all`, `open`, `closed`. |

### `pr`

Get and view all the pull requests for a repository.

| Command                     | Description                        |
| --------------------------- | ---------------------------------- |
| `octotrack pr [owner/repo]` | View Pull Requests for a repositry |

| Flags     | Description                                                                              |
| --------- | ---------------------------------------------------------------------------------------- |
| `--state` | Define a state to use to filter issues (default: all). Options: `all`, `open`, `closed`. |

### `releases`

Get and view all the releases for a repository.

| Command                           | Description                       |
| --------------------------------- | --------------------------------- |
| `octotrack releases [owner/repo]` | Get the releases for a repository |

### `repo`

Fetches and displays information about a GitHub repository.

| Command | Description |
|---|---|
| `octotrack repo info [owner/repo]` | Shows general repository info: description, language, visibility, stars, forks, license, and README preview. |
| `octotrack repo default <owner/repo>` | Sets a default owner and/or repo, used whenever `owner/repo` is omitted from other `repo` commands. |
| `octotrack repo readme [owner/repo]` | Fetches and renders just the repository's README. |
| `octotrack repo contents [owner/repo] [options]` | Lists the contents of a repository. |

| Flag | Description |
|---|---|
| `-p, --path <path>` | List contents of a specific folder in the repository. |
| `-h, --hidden` | Include hidden files (dotfiles) in the listing. |
| `-l, --list` | Print as a flat list instead of a tree. |
| `--depth <int>` | How many levels deep to recurse into subdirectories (default: `3`). |

### `setup`

Manages the local files OctoTrack needs to run (config directory, data directory, and env file for your token).

| Command | Description |
|---|---|
| `octotrack setup` | Creates the config and data directories, and the settings file, if they don't already exist. Safe to run again — existing valid setups are left untouched. |
| `octotrack setup validate` | Checks that all required paths exist and reports whether a GitHub token is set. |
| `octotrack setup remove` | Deletes all data and config files created by OctoTrack, after a confirmation prompt. |

### `tags`

View the newest tags for a repository.

| Command                       | Description                           |
| ----------------------------- | ------------------------------------- |
| `octotrack tags [owner/repo]` | View the latest tags for a repository |

## Configuration

OctoTrack stores its config in an OS-appropriate location via [`platformdirs`](https://github.com/tox-dev/platformdirs). Run `octotrack config path` to see the exact file on your system.

Your GitHub token is **never** stored in the config file — it lives exclusively in a local `.env` file managed by `octotrack config set-token`, and is loaded as an environment variable at runtime.

## License

MIT — see [LICENSE](./LICENSE) for details.

## Contributing

See [Contributing.md](./CONTRIBUTING.md) for details.
