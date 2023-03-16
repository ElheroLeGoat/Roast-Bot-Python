import os
import discord
from resources import globals

config = globals.__CONFIG__

class RoastClient(discord.Bot):
    ready = False

    async def on_ready(self):
        if self.ready:
            return
        self.ready = True
        await bot.change_presence(status=discord.Status.online)
    
    async def on_connect(self):
        if bool(config["RUNTIME"]["DEBUG"]):
            await self.register_commands()
    
    @staticmethod
    def load_cogs():
        
        try:
            for cog in os.listdir(globals.__PATHS__["cogs"]):
                bot.load_extension(f'cogs.{cog}.main')
        except IndexError as e:
            # Unable to find the index?
            pass
        except Exception as e:
            # the cog is already loaded
            pass

bot = RoastClient(owner_id=config["DISCORD"]["OWNER"])
bot.load_cogs()
bot.run(config["DISCORD"]["TOKEN"])