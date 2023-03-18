# Standard Library Imports

# Discord Imports
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option

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

    @RoastSlashGroup.command(name='roast', description="Roast someone!")
    @commands.has_permissions(send_messages=True)
    async def Roast(self, ctx: discord.ApplicationContext, 
                    user:     Option(discord.Member, "What user do you want to roast?", required=False),
                    roast_id: Option(int, "don't set this if you want a random roast.", required=False)):
        """A Command used to roast another user.

        Args:
            ctx (discord.ApplicationContext): The ApplicationContext
            user (discord.Member): The user to roast.
            roast_id (roast_id, optional): The roast_id if present.
        """
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

    @RoastSlashGroup.command(name="search", description="search for words or sentences in our roast library")
    @commands.has_permissions(send_messages=True)
    async def SearchRoast(self, ctx: discord.ApplicationContext,
                        search: Option(str, "What do you want to search for?", required=True)):
        """A command used to search for keywords in the roast database.

        Args:
            ctx (discord.ApplicationContext): The ApplicationContext
            search (str): The string to search for.
        """
        await ctx.defer()
        guild = await database.getGuild(ctx.guild.id)
        agc = []
        if guild:
            agc = guild.censor
        
        roast = self.roasts.SearchRoast(search, agc)
        await ctx.respond(roast["message"])

    async def _get_censor_list(self, ctx: discord.AutocompleteContext) -> list:
        """Private AutoComplete to retrieve the censor list.

        Args:
            ctx (discord.AutocompleteContext): The ApplicationContext

        Returns:
            list: the list of groups
        """
        if not ctx.interaction.user.guild_permissions.ban_members:
            return ["Missing Permissions"]
        return self.roasts.censor_groups
    
    @RoastSlashGroup.command(name="censor", description="Allow / disallow censor groups")
    @commands.has_guild_permissions(ban_members=True)
    async def CensorGuild(self, ctx:discord.ApplicationContext,
                        group: Option(str, "The group to allow / disallow", autocomplete=_get_censor_list),
                        allow: Option(bool, "A simple yes /no question. should they be allowed?")):
        """An Administrator command to censor specific groups in a guild

        Args:
            ctx (discord.ApplicationContext): The ApplicationContext
            allow (bool): Wether or not to allow the specific group
            group (str, optional): an autocompletecontext string. Defaults to _get_censor_list).

        Returns:
            _type_: _description_
        """
        await ctx.defer(ephemeral=True)
        if group not in self.roasts.censor_groups:
            return await ctx.respond("Bruw, please select one of the options from the dropdown instead of writing it yourself.")

        guild = await database.getGuild(ctx.interaction.guild.id)
        index = self.roasts.censor_groups.index(group)
        try:
            if guild:
                # Retrieve the index of the censor so we can add it.    
                if not allow:
                    # We want to remove the index from allowed elements.
                    try:
                        acg = guild.censor.remove(index)
                    except ValueError:
                        acg = guild.censor
                else:
                    acg = set(guild.censor)
                    acg.add(index)
                await database.createGuild(guild.id, list(acg), guild.urban, guild.meme)
            else:
                if allow:
                    await database.createGuild(ctx.interaction.guild.id, [index])
        except Exception as e:
            # Log error?
            print(e.with_traceback())
            return await ctx.respond("Bruw you fucked up.")

        await ctx.respond("Update of guild censorship is done.")

    @CensorGuild.error
    @SearchRoast.error
    @Roast.error
    async def censorError(self, ctx: discord.ApplicationContext, error:Exception):
        """Error handling for the Roast cog

        Args:
            ctx (discord.ApplicationContext): The ApplicationContext parsed from the command.
            error (Exception): The Error Exception
        """
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.delete()
        else:
            # Log error.
            pass


def setup(bot):
    """
    Setup function for cogs.
    Args:
        bot: the bot object.
    Returns:
        None
    """
    bot.add_cog(Roast(bot))