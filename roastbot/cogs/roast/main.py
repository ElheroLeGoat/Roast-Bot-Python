# Standard Library Imports

# Discord Imports
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, permissions, Option

# Project Imports
from ...resources import globals
from ...utils import database
from . import logic

class Roast(commands.Cog):
    
    def __init__(self, bot):
        print("ROAST Cog Loaded")
        self.bot = bot
        self.roasts = logic.RoastLogic()

    RoastSlashGroup = SlashCommandGroup("roasts", "Commands related to the Roasts.")

    @RoastSlashGroup.command(name='roast')
    async def Roast(self, ctx: discord.ApplicationContext, 
                    user:     Option(discord.Member, "What user do you want to roast?", required=False),
                    roast_id: Option(int, "don't set this if you want a random roast.", required=False)):
        
        guild = await database.getGuild(ctx.guild.id)
        acg = []
        if guild:
            acg = guild.censor
        roast = self.roasts.GetRoast(acg, roast_id)
        if roast["success"]:
            if user.id == self.bot.user.id:
                user = ctx.author
            await ctx.respond(f'{user.mention}, {roast["message"]}')
        else:
            await ctx.respond(roast["message"], ephemeral=True)


    @RoastSlashGroup.command(name="search_roasts")
    async def SearchRoast(self, ctx: discord.ApplicationContext,
                        search: Option(str, "What do you want to search for?", required=True)):
        await ctx.defer()
        guild = await database.getGuild(ctx.guild.id)
        agc = []
        if guild:
            agc = guild.censor
        
        roast = self.roasts.SearchRoast(search, agc)
        await ctx.respond(roast["message"])


def setup(bot):
    """
    Setup function for cogs.
    Args:
        bot: the bot object.
    Returns:
        None
    """
    bot.add_cog(Roast(bot))