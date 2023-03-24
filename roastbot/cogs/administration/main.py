import discord
from discord.ext import commands, tasks
from discord.commands import SlashCommandGroup, Option

from ...resources import globals
from ...utils import logging
from ...utils.heartbeat import Heartbeat

config = globals.__CONFIG__
ActiveDevelopers = config["DISCORD"]["ACTIVE.DEVS"].replace(" ", "").split(",")

class Administration(commands.Cog):
    heartbeat: Heartbeat    

    def __init__(self, bot: discord.AutoShardedBot):
        self.bot = bot
        self.heartbeat = Heartbeat()
        self.heartbeat.MakeFile()
        self.heartbeat.CleanOldFiles()
        logging.debug('Administration Cog loaded successfully')
    AdminSlashGroup = SlashCommandGroup("adm", "Admin commands that can only be run by the selected few", guild_ids = [461362371139469328], guild_only = True)

    @tasks.loop(minutes=int(config["HEARTBEAT"]["INTERVAL"]))
    async def HeartBeatTask(self):
        try:
            self.heartbeat.UpdateFile()
        except FileNotFoundError:
            logging.debug('Heartbeat file has been deleted, shutting down bot.')
            await self.bot.close()
            exit()

    @AdminSlashGroup.command(name="getlog", description="Retrieves current logfile")
    async def Getlog(self, ctx: discord.ApplicationContext):
        if not str(ctx.author.id) in ActiveDevelopers:
            return await ctx.respond("This command is restricted to the current active devs.", ephemeral=True)

        file = f'{globals.__ROOTPATH__.parent}{globals.__SEP__}roast_log.log'
        await ctx.respond(file=discord.File(file), ephemeral=True)

def setup(bot):
    """
    Setup function for cogs.
    Args:
    bot: the bot object.
    Returns:
    None
    """
    bot.add_cog(Administration(bot))