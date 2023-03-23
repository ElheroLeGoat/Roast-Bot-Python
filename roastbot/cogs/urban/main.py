import discord
from discord import Embed
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option
from . import api
from ...utils import database, logging

class Urban(commands.Cog):
    def __init__(self, bot):
        print("ROAST Cog Loaded")
        self.bot = bot
        self.api = api.UrbanApi()

    UrbanSlashGroup = SlashCommandGroup("urban", "Commands related to urban dictionary.")

    @UrbanSlashGroup.command(name="search", description="Lookup something in the urban dictionary!")
    @commands.has_permissions(send_messages=True)
    async def Search(self, ctx: discord.ApplicationContext,
                    word: Option(str, "The word to lookup")):
        """A command to Search the Urban Dictionary

        Args:
            ctx (discord.ApplicationContext): The ApplicationContext
            word (string): The word to search for.
        
        Return:
            None
        """
        await ctx.defer()
        guild = await database.getGuild(ctx.guild.id)
        if guild and not guild.urban:
            return await ctx.respond(f'Sorry, but `{ctx.guild.name}` has disabled the Urban dictionary', ephemeral=True)
        lookup = await self.api.LookupByWord(word.strip())
        if lookup:
            embed = discord.Embed(
                color=0xEB671D,
                title=word.capitalize(),
                url=lookup['permalink'],
                description=f'**Definition**\n*{lookup["definition"]}*\n\n**Example**\n{lookup["example"]}'
            )
            embed.add_field(name="Author:", value=lookup["author"], inline=False)
            embed.add_field(name="Ratings:", value= f'**Upvotes: :thumbsup:**{lookup["thumbs_up"]} | **Downvotes: :thumbsdown:** {lookup["thumbs_down"]}', inline=False)
            return await ctx.respond(embed=embed)
        return await ctx.respond("Is Urban Dictionary down? - Unable to search at this moment.", ephemeral=True)
    
    @UrbanSlashGroup.command(name="censor", description="Enable / disable Urban dictionary for the current guild.")
    @commands.has_permissions(ban_members=True)
    async def CensorUrban(self, ctx:discord.ApplicationContext,
                        enable: Option(bool, "Is enabled by default")):
        """An Administrator Command used to Enable / Disable the Urban Dictionary in a guild.

        Args:
            ctx (discord.ApplicationContext): The ApplicationContext
            enable (boolean): a True / False option
        """
        guild = await database.getGuild(ctx.guild.id)
        if guild:
            await database.createGuild(guild.id, guild.censor, enable, guild.meme)
        else:
            await database.createGuild(ctx.guild.id, urban=enable)
        await ctx.respond("Settings for the Urban Dictionary has been updated", ephemeral=True)

    @CensorUrban.error
    @Search.error
    async def censorError(self, ctx: discord.ApplicationContext, error: Exception):
        """Error handling for UrbanDictionary

        Args:
            ctx (discord.ApplicationContext): The ApplicationContext parsed from the command.
            error (Exception): The Error Exception
        """
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.delete()
        else:
            # Log error.
            logging.error(f'{ctx.author.name}#{ctx.author.discriminator} Tried to use {ctx.command.qualified_name} in {ctx.guild.name} but it failed with error {error}')
            pass

def setup(bot):
    """
    Setup function for cogs.
    Args:
        bot: the bot object.
    Returns:
        None
    """
    bot.add_cog(Urban(bot))