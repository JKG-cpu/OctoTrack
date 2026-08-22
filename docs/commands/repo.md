# Repo

***OctoTrack*** has commands that can fetch things about Repositories.

## Quick Setting a default

You can quickly set a default owner / repository without using config commands by typing `octotrack repo default <owner/repo>`. This saves automatically, so you don't have to see the current config / set a new repository to default to.

## Basic Information

The most basic *(maybe most useful?)* command for repositories in OctoTrack is `octotrack repo info <owner/repo>`. This fetches data from a repository and displays it all neatly in front of you.

## Contents

You can also view repository contents with `octotrack repo contents <owner/repo> <path>`. This makes a nice tree for you where you can see everything inside of a repository. If you only want to see one part of the repository, you can specify a `<path>` argument, which is just the folder / file name you would like to view.

You can specify a depth to view, whether or not to show hidden files, or whether or not to just list them *(view `octotrack repo contents --help` for more information)*.

## Readme

You can also view the repository's README.md with `octotrack repo readme <owner/repo>`. This displays the README.md in markdown text.

??? note "Got Ideas?"
    If you think these commands ***should*** display other things or ***shouldn't*** display other things, you can head over to the [OctoTrack Repository](https://github.com/JKG-cpu/OctoTrack) and create an issue.

    I check these about every week, so there's a good change your request will be seen and fullfilled!