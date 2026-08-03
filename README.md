# OctoTrack

An async CLI client for GitHub, built to track commits, pull requests, issues, releases, and general repository activity — straight from your terminal.

OctoTrack talks directly to the [GitHub REST API](https://docs.github.com/en/rest) using `httpx`, so there's no dependency on the `gh` CLI or any GitHub SDK.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
  - [`setup`](#setup)
  - [`config`](#config)
  - [`repo`](#repo)
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

All commands are grouped under three top-level subcommands: `setup`, `config`, and `repo`. Run `octotrack --help`, or `--help` on any subcommand, to see this reference from the CLI itself.

### `setup`

Manages the local files OctoTrack needs to run (config directory, data directory, and env file for your token).

| Command | Description |
|---|---|
| `octotrack setup` | Creates the config and data directories, and the settings file, if they don't already exist. Safe to run again — existing valid setups are left untouched. |
| `octotrack setup validate` | Checks that all required paths exist and reports whether a GitHub token is set. |
| `octotrack setup remove` | Deletes all data and config files created by OctoTrack, after a confirmation prompt. |

### `config`

Reads and writes local configuration, including your GitHub token.

| Command | Description |
|---|---|
| `octotrack config show` | Prints all current config values. |
| `octotrack config set-token` | Prompts for a GitHub token and stores it as a local environment variable. Never written to the config file. |
| `octotrack config set <key> <value>` | Sets a config value directly. Valid keys: `default_owner`, `default_repo`, `default_pr_state`, `api_base_url`. |
| `octotrack config clear [--key/-k <key>]` | Resets a single config key to its default. Omit `--key` to reset the entire config. |
| `octotrack config path` | Prints the path to the config settings file. |

### `repo`

Fetches and displays information about a GitHub repository.

| Command | Description |
|---|---|
| `octotrack repo info [owner/repo]` | Shows general repository info: description, language, visibility, stars, forks, license, and README preview. |
| `octotrack repo default <owner/repo>` | Sets a default owner and/or repo, used whenever `owner/repo` is omitted from other `repo` commands. |
| `octotrack repo readme [owner/repo]` | Fetches and renders just the repository's README. |
| `octotrack repo contents [owner/repo] [options]` | Lists the contents of a repository. |

**`repo contents` options:**

| Flag | Description |
|---|---|
| `-p, --path <path>` | List contents of a specific folder in the repository. |
| `-h, --hidden` | Include hidden files (dotfiles) in the listing. |
| `-l, --list` | Print as a flat list instead of a tree. |
| `--depth <int>` | How many levels deep to recurse into subdirectories (default: `3`). |

Every `repo` command that accepts `owner/repo` will fall back to your configured default (set via `octotrack repo default`) for whichever part — owner, repo, or both — you omit.

## Configuration

OctoTrack stores its config in an OS-appropriate location via [`platformdirs`](https://github.com/tox-dev/platformdirs). Run `octotrack config path` to see the exact file on your system.

Your GitHub token is **never** stored in the config file — it lives exclusively in a local `.env` file managed by `octotrack config set-token`, and is loaded as an environment variable at runtime.

## License

MIT — see [LICENSE](./LICENSE) for details.

## Contributing

See [Contributing.md](./CONTRIBUTING.md) for details.