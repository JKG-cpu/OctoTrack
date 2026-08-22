# Config

***OctoTrack*** has commands to help you setup a default configuration for Octotrack. Including things like what repository to view!

## Setting a GitHub Auth Token

Setting a token for OctoTrack to view is pretty easy. All you do is run `octotrack config set-token` and paste in the token.

OctoTrack is setup where you can paste your GitHub Token and it won't be shown to anyone even if you show them your terminal output. OctoTrack also saved the token in a .env file, where it is only accessible to you. OctoTrack won't show you your token ever.

Do NOT share your GitHub Token!!!

## Setting and Clearing Your Config

You can set different config keys to have different values with `octotrack config set {key} {value}`. Run `octotrack config set --help` to view the key values you can set.

- `<default_owner>` sets the default Repository Owner
- `<default_repo>` sets the default Repository
- `<default_pr_state>` sets the default Pull Requests to fetch
- `<api_base_url>` is the base api url (useful if you work in an organization)

You can always clear the config with `octotrack config clear` or just clear a key with `octotrack config clear {key}`. OctoTrack **does not** clear your GitHub Auth Token.

## Viewing your config

You can view your OctoTrack config via `octotrack config show` OR you can get the path and view it via `octotrack config path`

??? note "Got Ideas?"
    If you think these commands ***should*** display other things or ***shouldn't*** display other things, you can head over to the [OctoTrack Repository](https://github.com/JKG-cpu/OctoTrack) and create an issue.

    I check these about every week, so there's a good change your request will be seen and fullfilled!