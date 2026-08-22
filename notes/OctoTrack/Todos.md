# OctoTrack Versions
### `v0.1.0`
##### ***Introduction to Octotrack***
Have octotrack do basic things like setting up data + config and getting things from a Github Repository

- [x] Create Pydantic models for `octotrack repo info`
- [x] Create a display for models when commands like `octotrack repo info` are used
- [x] Need to create Pydantic models for the rest of the `octotrack repo` commands + Display models for the rest of the `octotrack repo` commands
	- [x] `octotrack repo readme <owner/repo>`
	- [x] `octotrack repo contents <owner/repo> <path>`
- [x] Run a few tests (configured by Claude)
- [x] [^1]Publish `v0.1.0`

### `v0.2.0`
##### ***Edits to certain commands***

- [x] Add new command `octotrack config github-token-help`
	-  Explains to people how to create and use a GitHub Token ***(Required for this project)***
- [x] Change command `octotrack config edit-token` => `octotrack config set-token`
- [x] [^1] Publish `v0.2.0`

### `v0.3.0`
##### ***Add useful things like grabbing commits + messages***

- [x] Start creating commands (structure) for commits
- [x] Create models for commits
- [x] Display models for commits
- [x] [^1]Publish `v0.3.0`

### `v0.4.0`
##### ***After Introduction to `httpx`, start grabbing common things from GitHub Repositories***
Also include commands that are in other CLI tools, i.e. seeing what version your current tool is + add a help section, maybe with links to documentation???

- [ ] Start creating commands (structure) and models for 
	- [x] Branches 
	- [x] Tags
	- [ ] Releases
	- [ ] Issues
	- [ ] Pull Requests
- [ ] Display models for
	- [x] Branches 
	- [x] Tags
	- [ ] Releases
	- [ ] Issues
	- [ ] Pull Requests
- [x] Add an `octotrack -v / --version` command
- [ ] Create an `octotrack help` section as a "file directory" for documentation on how to use OctoTrack, setting up GitHub Auth Tokens, and other things
- [ ] [^1]Publish `v0.4.0`

## `v0.5.0`
##### ***Better Displays!!!***
Not all people use CLI Tools comfortably, to create a Textual TUI Interface to allow more people to use OctoTrack *(also make code better by keeping display stuff in one "main" file / class / subclasses)*.

- [ ] Build a better display manager
	- A class that holds all the logic for display models + text (static methods + class methods)
	- [ ] Include option(s) for [^2]themes
- [ ] Polish code so it's easy to read + use `ruff` as the linter
- [ ] Create a Textual Interface so that OctoTrack could be used as a CLI tool AND a CLI App

# Overall Todo's
- [x] Start creating documentation for OctoTrack explaining
	- [x] What it is
	- [x] How to use it
	- [x] How to set up OctoTrack
- [x] [^3]Deploy to GitHub pages???
- [ ] Need to add more details to documentation, including
	- [ ] Each Command
		- [x] Setup
		- [x] Config
		- [x] Repository
		- [x] Commits
		- [x] Branches & Tags
		- [ ] Releases
		- [ ] Issues
		- [ ] Pull Requests
	- [x] Installation
	- [x] Quick Start
	- [x] GitHub Auth Token
- [ ] Maybe add better errors, specifically for invalid urls + timeouts

[^1]: Need to update / create the things listed below
	1. Update project `README.md`
	2. Updated `pyproject.toml`
	3. Create / update `requirements.txt`
	4. Create / update a workflow (for when a tag is created + pushed)
	5. ***PUSH*** workflow first, ***THEN*** tag it and push

[^2]: Changing themes / colors will be implemented in a different version, not `v0.1.0` or `v0.2.0` or `v0.3.0`. Maybe `v0.5.0+`.

[^3]: Create pages with MkDocs + Create a workflow
