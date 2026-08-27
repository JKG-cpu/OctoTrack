![OctoTrack](docs/images/octotrack_banner.png)

An Async API CLI Client for GitHub that can be used to track things like from GitHub Repositories like Releases, Pull Requests, Issues, and more!

OctoTrack uses the GitHub REST API Client to get any repository information needed.

## Installation

You can install OctoTrack via pip

```bash
pip install octotrack
```

## Basic Commands

There are quite a few OctoTrack commands that can help you get information about repositories. You can see all of these by typing `octotrack --help`.

Most of the commands take an `owner/repo` argument or you can choose to pass one or not. If you choose not to pass an argument for `owner/repo`, this will just default to your default owner / repo in your configuration. You can change these at any time by running `octotrack config set default_owner OWNER` and `octotrack config set default_repo REPO`.

If you find any commands you can quite understand, you can head over to the [OctoTrack Documentation](https://jkg-cpu.github.io/OctoTrack/) on GitHub Pages.

## License

This project is under the [MIT License](./LICENSE)

## Contributing

Read [Contributing](./CONTRIBUTING.md) for details.
