# System Imports
from pathlib import Path
import random

# Discord Imports
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option

# Project Imports
from ...utils import database, logging
from ...resources.globals import paths
class Memes(commands.Cog):
    def __init__(self, bot):
        logging.debug('Memes Cog loaded successfully')
        self.bot = bot

    MemesSlashGroup = SlashCommandGroup("memes", "Commands related to Memes.")

    @commands.slash_command(name='meme', description="Retrieve a Meme!")
    @commands.has_permissions(send_messages=True)
    async def meme(self, ctx: discord.ApplicationContext, 
                    id: Option(int, "get a specific meme.", required=False)):
        """A Command used to retrieve a random meme

        Args:
            ctx (discord.ApplicationContext): The ApplicationContext
            id (int, optional): The meme id.
        """
        guild = await database.getGuild(ctx.guild.id)
        if guild and not guild.meme:
            if ctx.author.guild_permissions.ban_members:
                return await ctx.respond(f'`{ctx.guild.name}` has disabled memes, you can enable it by using `/memes censor False`', ephemeral=True)
            return await ctx.respond(f'Sorry, but `{ctx.guild.name}` has disabled memes', ephemeral=True)

        # @TODO: Make sure .jpg files are disallowed.
        meme_path = Path.joinpath(paths.RESOURCES, 'images', 'memes')
        meme_count = len(list(meme_path.glob('*.png')) + list(meme_path.glob('*.jpg'))) if meme_path else 0

        if not meme_count:
            return await ctx.respond('Oh no! Roastbot has forgotten all the memes (Error: 404 Memes-not-found)', ephemeral=True)

        if not id:
            id = random.randint(1, meme_count)

        file = Path.joinpath(meme_path, f'meme{id}.png')
        if not file:
            file = Path.joinpath(meme_path, f'meme{id}.jpg')
        await ctx.respond(file=discord.File(file))

    @MemesSlashGroup.command(name="censor", description="Enable / disable Memes for the current guild.")
    @commands.has_permissions(ban_members=True)
    async def CensorUrban(self, ctx:discord.ApplicationContext,
                        enable: Option(bool, "Is enabled by default")):
        """An Administrator Command used to Enable / Disable the Memes.

        Args:
            ctx (discord.ApplicationContext): The ApplicationContext
            enable (boolean): a True / False option
        """
        guild = await database.getGuild(ctx.guild.id)
        if guild:
            await database.createGuild(guild.id, guild.censor, guild.urban, enable)
        else:
            await database.createGuild(ctx.guild.id, memes=enable)
        await ctx.respond("Settings for the Urban Dictionary has been updated", ephemeral=True)

def setup(bot):
    """
    Setup function for cogs.
    Args:
        bot: the bot object.
    Returns:
        None
    """
    bot.add_cog(Memes(bot))