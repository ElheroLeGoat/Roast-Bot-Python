# System Imports
import os

# Discord Imports
import discord

# Project Imports
from .resources import globals
from .utils import logging
from .utils.types import wrap
class RoastClient(discord.AutoShardedBot):
    ready = False
    FirstConnection = True

    async def on_ready(self):
        if self.ready:
            return

        logging.info(wrap(f'ROAST BOT IS LIVE',
                          f'Version___: {globals.__VERSION__}',
                          f'Username__: {bot.user.name}',
                          f'Shards____: {bot.shard_count}',
                          f'Servers___: {len(bot.guilds)}',
                          f'Process id: {os.getpid()}', 
                          f'Debug Mode: {"Yes" if globals.config.LOGGING.DEBUG else "No"}'
                        )
                    )
        self.ready = True
        await bot.change_presence(status=discord.Status.online)
    
    async def on_connect(self):
        if globals.config.LOGGING.DEBUG and self.FirstConnection:
            logging.debug(f'Debug is enabled and command registration will begin')
            commands = await self.register_commands(force=True, delete_existing=True)
            self.FirstConnection = False

    @staticmethod
    def load_cogs():
        for cog in os.listdir(globals.__PATHS__["COGS"]):
            try:
                bot.load_extension(f'roastbot.cogs.{cog}.main')
            except discord.errors.NoEntryPointError:
                pass

bot = RoastClient(owner_id=globals.config.DISCORD.OWNER)
bot.load_cogs()
bot.run(globals.config.DISCORD.TOKEN)