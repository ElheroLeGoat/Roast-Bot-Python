# System Imports

# Discord Imports
import discord
from discord.ext import commands, tasks
from discord.commands import SlashCommandGroup, Option

# Project Imports
from ...resources import globals
from ...utils import logging
from ...utils.heartbeat import Heartbeat

class Administration(commands.Cog):
    heartbeat: Heartbeat    

    def __init__(self, bot: discord.AutoShardedBot):
        self.bot = bot
        self.heartbeat = Heartbeat()
        self.heartbeat.MakeFile()
        self.heartbeat.CleanOldFiles()
        self.HeartBeatTask.start()

        logging.debug('Administration Cog loaded successfully')
    AdminSlashGroup = SlashCommandGroup("radmin", "Admin commands that can only be run by the selected few")

    @tasks.loop(minutes=globals.config.HEARTBEAT.INTERVAL)
    async def HeartBeatTask(self):
        try:
            self.heartbeat.UpdateFile()
        except FileNotFoundError:
            logging.debug('Heartbeat file has been deleted, shutting down bot.')
            await self.bot.close()
            exit()

    @AdminSlashGroup.command(name="getlog", description="Retrieves current logfile", guild_ids=[461362371139469328])
    async def Getlog(self, ctx: discord.ApplicationContext):
        if not ctx.author.id in globals.config.DISCORD.ACTIVE.DEVS:
            logging.CommandLogger(ctx, "getlog", "The command is restricted to active devs.")
            return await ctx.respond("This command is restricted to the current active devs.", ephemeral=True)

        logging.CommandLogger(ctx, "getlog", "The logfile")
        file = f'{globals.__ROOTPATH__.parent}{globals.__SEP__}roast_log.log'
        await ctx.respond(file=discord.File(file), ephemeral=True)

    @AdminSlashGroup.command(name="globalmsg", description="Admin command to send out a global message from Roast bot", guild_ids=[461362371139469328])
    async def SendSysMessage(self, ctx: discord.ApplicationContext, 
                            message: Option(str, "The message to send out.")):
        if not ctx.author.id in globals.config.DISCORD.ACTIVE.DEVS:
            logging.CommandLogger(ctx, "SendSysMessage (globalmsg)", "The command is restricted to active devs.")
            return await ctx.respond("This command is restricted to the current active devs.", ephemeral=True)
        elif len(message) > 2000:
            logging.CommandLogger(ctx, "SendSysMessage (globalmsg)", f'Message too long error {len(message)}')
            return await ctx.respond(f'Your message is {(len(message) - 2000)} characters for long', ephemeral=True)
        # @TODO: Actually make the logic lol
        logging.debug(f'{len(ctx.bot.guilds)}')

def setup(bot):
    """
    Setup function for cogs.
    Args:
    bot: the bot object.
    Returns:
    None
    """
    bot.add_cog(Administration(bot))