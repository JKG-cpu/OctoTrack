# Running Your First OctoTrack Command

After the [OctoTrack Setup](../setup.md) is complete, you can run your first command.

The most basic *(and maybe most useful?)* OctoTrack command is getting repository information. You specify you want to fetch the information of a repository with `octotrack repo`.

There are a view arguments for the `octotrack repo` command. Right now, you will be only using the `info` command.

!!! note
    More info on `octotrack repo` commands can be found at [Repository Commands](./repo.md) or by running `octotrack repo --help`

When you run `octotrack repo info` for the first time, you will see you need to specify an repository argument.

You can specify a repository argument by typing `<owner/repo>` after `octotrack repo info`, but thats to much typing, and can be tedious if you are fetching information about the same repository over and over.

An easier way to do this, is by setting a default `<owner/repo>`. You can do this by running `octotrack repo default <owner/repo>`. By default, if you type the argument without a slash, OctoTrack will presume that your passing an owner argument. If you want to set a default owner and repo, just type `your_owner/your_repo`.

OctoTrack will tell you that the changes are successful. After that, you can just run `octotrack repo info` and you will fetch the repository information for the default repository your just set!

You can also see the current config setup by running `octotrack config show`.