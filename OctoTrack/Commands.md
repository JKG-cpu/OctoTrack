To run the module, use `octotrack`.
## Setup
```bash
octotrack setup
```
> Sets up OctoTrack for first-time use.

```bash
octotrack setup --validate
```
> Checks that your current installation is valid.

```bash
octotrack setup --remove
```
> Removes the current OctoTrack configuration.

## Config
```bash
octotrack config
```
> Sets up OctoTrack's config

```bash
octotrack config --show
```
> Shows OctoTrack's current config setup

```bash
octotrack config --set-token
```
> Set your GitHub token (*needed for the app to work*)

```bash
octotrack config edit --args
```
> Edit a specific argument in the config

OctoTrack config
```json
{
	"default_owner": "Repo Owner",
	"default_pr_state": "open" | "closed" | "all",
	"api_base_url": "https://api.github.com" | "https://github.mycompany.com/api/v3"
}
```

For the GitHub token, it will be stored in a .env file within the config directory *(generated via `octotrack setup`)*. 

## Client
```
octotrack client repo "Repo Name"
```
