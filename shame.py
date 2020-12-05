import asyncio
import logging
import json

import discord

logging.basicConfig(level=logging.INFO)

config_file = open('config.json', 'r')
config = json.load(config_file)
shame_channel_ids = config['channel_ids']
token = config['token']

# Play the shame clip over and over as long as the VoiceClient is connected
async def play_forever(vc: discord.VoiceClient):
    event = asyncio.Event()
    while vc.is_connected():
        audio = discord.FFmpegPCMAudio('resources/shame.mp3')
        vc.play(audio, after=lambda _: event.set())
        await event.wait()
        event.clear()

class Shame(discord.Client):
    async def on_ready(self):
        logging.info("Shamebot ready to shame!")

    # Get the Client's VoiceClient if connected to a specific Guild
    def get_guild_vc(self, guild: discord.Guild) -> discord.VoiceClient:
        for bot_vc in self.voice_clients:
            if bot_vc.guild == guild:
                return bot_vc
        return None

    # Leave channel in specific guild if it is empty
    async def leave_if_empty(self, guild):
        guild_vc = self.get_guild_vc(guild)
        if guild_vc is None:
            return
        if len(guild_vc.channel.members) <= 1:
            await guild_vc.disconnect()

    async def on_voice_state_update(self, 
                                    member: discord.Member,
                                    before: discord.VoiceState,
                                    after: discord.VoiceState):

        if member == self.user:
            return

        # Return if event wasn't leave or join
        if before.channel == after.channel:
            return

        # Leave channel if last member left
        guild = member.guild
        if before.channel is not None and before.channel.id in shame_channel_ids:
            print("leaving!!")
            await self.leave_if_empty(guild)
            return

        # Return if a channel wasn't joined
        if after.channel is None:
            return

        # Return if someone joined the wrong channel
        if after.channel.id not in shame_channel_ids:
            return

        # Connect and start playing unless we are already connected
        guild_vc = self.get_guild_vc(guild)
        if guild_vc is None or guild_vc.channel != after.channel:
            guild_vc: discord.VoiceClient = await after.channel.connect()
            asyncio.create_task(play_forever(guild_vc))
        elif guild_vc.channel == after.channel:
            return

shame = Shame()

shame.run(token)
