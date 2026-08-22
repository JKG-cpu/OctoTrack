# Branches & Tags

***OctoTrack*** has a command for grabbing branches on a GitHub Repository as well as the latest tags.

## Branches

By default, if you run `octotrack branches <owner/repo>`, it will fetch every branch on that repository, as well as if that branch is protected and the latest commit it is on.

If you want to view more information about a branch, you can pass in a branch argument.

```bash
octotrack branches -b branch_name
```

## Tags

***OctoTrack*** grabs the latest tags only from a GitHub Repository via `octotrack tags`.

This will display the branch, it's protection, and the latest commit's *information*.

??? note "Got Ideas?"
    If you think these commands ***should*** display other things or ***shouldn't*** display other things, you can head over to the [OctoTrack Repository](https://github.com/JKG-cpu/OctoTrack) and create an issue.

    I check these about every week, so there's a good change your request will be seen and fullfilled!
