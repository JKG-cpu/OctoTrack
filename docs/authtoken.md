# How to create a GitHub Auth Token

You'll need a GitHub personal access token to use OctoTrack — here's a quick rundown of how to get one.

!!! note
    Before setting up an auth token, you must first setup the necessary files for OctoTrack to run. Just type in `octotrack setup` and you will be good to go!

1. Go to [GitHub's token settings page](https://github.com/settings/personal-access-tokens) and click 'Generate new token'.
2. Choose 'Fine-grained token' (recommended) or 'Token (classic)'.
3. Give it a name, an expiration, and at minimum 'repo' read access for the repositories you want to track.
4. Copy the generated token — ***GITHUB ONLY SHOWS THIS ONCE***
5. Run `octotrack config set-token` and paste it in when prompted.

!!! note
    OctoTrack does NOT save your GitHub Auth Token publicly.
    It is kept in a .env file in your App Data.

    Do NOT share your GitHub Token!!!

[More Info About GitHub Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)