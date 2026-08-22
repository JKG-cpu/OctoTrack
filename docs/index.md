# OctoTrack

![OctoTrack](images/octotrack_banner.png)

An async CLI client for the GitHub API — track commits, pull requests, issues, releases, and repository activity straight from your terminal, with concurrent lookups so nothing feels slow.

## Quick Install

```bash
pip install octotrack
```

Requires Python 3.13+.

## Quick Start

Run the OctoTrack setup command

```bash
octotrack setup
```

This sets up all the important files for OctoTrack. For a brand new setup, you will still have to create / add a [GitHub Auth Token](authtoken.md).

If you ever decide to uninstall octotrack, or you think the configuration is messed up, you can run these two commands.

```bash
octotrack setup remove # Remove the OctoTrack Setup
```

```bash
octotrack setup validate # Validate the current OctoTrack setup
```

After the setup is complete, you can head over to [Running Your First Command](commands/first_command.md) to start using OctoTrack!

## Current Features

??? "Current OctoTrack Commands"
    ??? "Repository Information"
        - Description
        - Default Branch
        - Visibility
        - Size
        - Stars / forks / watchers counts
        - Homepage
        - Archived
        - Created at
        - Updated at
        - Pushed at
        - License *(if available)*
        - Read me *(if available)*

    * **Repository Content (Files and Folders)**
    * **Repository README**
        
    * **Repository Commits + Commit Messages**

    * **Repository Branches + Tags**

    ***More commands will be added soon!***

## More Info

- [Quick Start](quickstart.md)
- [Get a GitHub Auth Token](authtoken.md)
- [Running Your First Command](commands/first_command.md)