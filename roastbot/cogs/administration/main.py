# System Imports
import datetime
from pathlib import Path

# Discord Imports
import discord
from discord.ext import commands, tasks
from discord.commands import SlashCommandGroup, Option

# Project Imports
from ...resources import globals
from ...utils import logging
from ...utils.heartbeat import Heartbeat
from ...resources.globals import config
from ...utils.types import deltaFormatter

class Administration(commands.Cog):
    heartbeat: Heartbeat    

    def __init__(self, bot: discord.AutoShardedBot):
        self.bot = bot
        self.heartbeat = Heartbeat()
        self.heartbeat.MakeFile()
        self.heartbeat.CleanOldFiles()
        self.HeartBeatTask.start()

        logging.debug('Administration Cog loaded successfully')
    utilitySlashGroup = SlashCommandGroup("utils", "Utility commands for Roastbot")

    @tasks.loop(minutes=globals.config.HEARTBEAT.INTERVAL)
    async def HeartBeatTask(self):
        try:
            self.heartbeat.UpdateFile()
        except FileNotFoundError:
            logging.debug('Heartbeat file has been deleted, shutting down bot.')
            await self.bot.close()
            exit()

    @utilitySlashGroup.command(name="getlog", description="Retrieves current logfile", guild_ids=[461362371139469328])
    async def Getlog(self, ctx: discord.ApplicationContext):
        if not ctx.author.id in globals.config.DISCORD.ACTIVE.DEVS:
            logging.CommandLogger(ctx, "getlog", "The command is restricted to active devs.")
            return await ctx.respond("This command is restricted to the current active devs.", ephemeral=True)

        logging.CommandLogger(ctx, "getlog", "The logfile")
        file = Path.joinpath(globals.paths.RESOURCES, 'logs', 'roast_log.log')
        if not file.is_file():
            return await ctx.respond(f'uh oh - the log: {file} does not exist!', ephemeral=True)
        await ctx.respond(file=discord.File(file), ephemeral=True)

    @utilitySlashGroup.command(name='status', description='Shows information about the bot.')
    async def SendStatusMessage(self, ctx: discord.ApplicationContext,
                            hidden: Option(bool, "Want the message to be hidden?", required=False, default=False)):
        delta = deltaFormatter(datetime.datetime.now() - globals.__START_TIME__)
        
        description = f'```\n'\
                    f'version____: {globals.__VERSION__}\n'\
                    f'username___: {self.bot.user.name}\n'\
                    f'uptime_____: {delta}\n'\
                    f'shard_count: {self.bot.shard_count}\n'\
                    f'guilds_____: {len(self.bot.guilds)}\n'\
                    f'```'

        if config.COMMANDS.LOCK.STATUS.COMMAND and ctx.author.id not in config.DISCORD.ACTIVE.DEVS:
            description = f'Roasting people in {len(self.bot.guilds)} servers.'
        embed = self._presetEmbed('Roast bot status message', description)

        logging.CommandLogger(ctx, 'status', f'\n{description}')
        await ctx.respond(embed=embed, ephemeral=hidden)

    @utilitySlashGroup.command(name='invite', description="Retrieve a list of useful links.")
    async def ProvideLinks(self, ctx: discord.ApplicationContext,
                        hidden: Option(bool, "Want the message to be hidden?", required=False, default=False)):
        links = f'Here are all useful links. \n'\
                f'Roastbot can be invited by following: [this link](https://discordapp.com/oauth2/authorize?client_id=461361233644355595&scope=bot&permissions=8")\n'\
                f'Our support server can be found: [here](https://discord.com/invite/9y8yV42)\n'\
                f'Vote Roastbot at: [top.gg](https://top.gg/bot/461361233644355595)\n'\
                f'Public git repo: [Roast-Bot-Python](https://github.com/ElheroLeGoat/Roast-Bot-Python)'
        embed = self._presetEmbed('Roastbot links', links)

        logging.CommandLogger(ctx, 'invite', f'\n{links}')
        await ctx.respond(embed=embed, ephemeral=hidden)

    def _presetEmbed(self, title: str, description: str) -> discord.Embed:
        embed = discord.Embed(title=f'{title} <:roast_circle:474755210485563404>', description=description)
        embed.set_footer(text=f'Roastbot - Python Version {globals.__VERSION__} made with ❤ by Ole113#2421 and ElHeroLeGoat#9561')
        return embed
    
    @ProvideLinks.error
    @SendStatusMessage.error
    @Getlog.error
    async def ErrorHandler(self, ctx: discord.ApplicationContext, error: Exception):
        await ctx.delete()
        logging.error(error)

def setup(bot):
    """
    Setup function for cogs.
    Args:
    bot: the bot object.
    Returns:
    None
    """
    bot.add_cog(Administration(bot))