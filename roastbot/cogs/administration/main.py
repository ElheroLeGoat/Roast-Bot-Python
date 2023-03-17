import discord
from discord.ext import commands, tasks
from ...utils import heartbeat
from ...resources import globals

class Administration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        if globals.__CONFIG__["HEARTBEAT"]["ENABLED"]:
            self.Heartbeat.start()

    @staticmethod
    @tasks.loop(minutes=5)
    async def Heartbeat():
        heartbeat.GenerateHeartbeat()

def setup(bot):
    """
    Setup function for cogs.
    Args:
        bot: the bot object.
    Returns:
        None
    """
    bot.add_cog(Administration(bot))