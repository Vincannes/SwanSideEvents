#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import discord


class DiscordBot(object):
    LOGGER = None

    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        intents = discord.Intents.default()
        intents.messages = True
        intents.guilds = True
        intents.message_content = True
        self.client = discord.Client(intents=intents)

    def run(self, message):
        @self.client.event
        async def on_ready():
            self.LOGGER.info(f'Bot connect has {self.client.user}')
            channel = self.client.get_channel(self.channel_id)
            if channel:
                self.LOGGER.info(f'Channel found : {self.channel_id}')
                await channel.send(message)
            else:
                self.LOGGER.error(f'Channel not found : {self.channel_id}')
            await self.client.close()

        self.client.run(self.token)
