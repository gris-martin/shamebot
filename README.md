# shamebot

## Quickstart Guide

1. Setup a bot application on the Discord Developer portal ([guide](https://discordpy.readthedocs.io/en/latest/discord.html))
2. Install and configure Docker. If on Windows, make sure Docker is configured to handle Linux images.
3. Navigate to repository directory.
4. Edit `config.json` with your bot token and the IDs of the channels where you want the shaming to occur.
5. Run `docker build -t shamebot .`
5. Run `docker run shamebot`
6. Shame.
