import random
import discord
from discord.ext import commands
from src.resources import globals
import json

# class Roast(commands.Cog):
class Roast():

    # Dictionary structure
    # censor_group
    #   roast_id
    #       roast_number
    roasts: dict = {}
    censor_groups: list = []
    total_roasts: int = 0

    def __init__(self, bot):
        self.bot = bot
        self.load_roasts()
    

    def reload_roasts(self):
        return self.load_roasts()

    def load_roasts(self):
        self.roasts = {}
        with open(f'{globals.__PATHS__["RESOURCES"]}{globals.__SEP__}roasts.json') as obj:
            data = json.loads(obj.read())

            # Setup of Censor groups
            self.censor_groups = list(data["censor_groups"])
            i = 0
            while i < len(self.censor_groups):
                self.roasts[i] = {}
                i += 1
            
            # Setup of roasts
            i = 0
            # Iterating roasts.
            for roast in data["roasts"]:
                i += 1
                try:
                    # Quick check to figure out if we have a censor group for the roast.
                    self.censor_groups[roast["censor"]]

                    self.roasts[roast["censor"]][i] = roast["roast"]
                except IndexError:
                    # Roast should not be saved since the censor doesn't exist.
                    pass
            self.total_roasts = i - 1

    def SearchRoast(self, search_param: str, allowed_groups: list = []):
        lookup_table = self._getLookupTable(allowed_groups)

        # Fucking magical searching
        def mapFunc(index):
            if search_param.lower() in lookup_table[index].lower():
                return f'{index}: {lookup_table[index]}'
        result = "\n".join(list(filter(lambda item: item is not None, list(map(mapFunc, lookup_table)))))


        message = f'**Found:**```{result}```'

        if not result:
            return {"success": False, "message": f'You looked for: `{search_param}` but there\'s no roasts containing that, try being less specific.'}
        elif len(message) > 2000:
            return {"success": False, "message": f'There were too many roasts found that have `{search_param}` in them, try being more specific.'}

        return {"success": True, "message": message}


    def GetRoast(self, allowed_groups: list = [], roast_id: int = None) -> str:
        retval = {"success": True}
        lookup_table = self._getLookupTable(allowed_groups)

        # If there's not roast ID we want to retrieve a random roast from the lookup table.
        index = roast_id
        if index is None:
            index = random.choice(list(lookup_table.keys()))

        # Retrieving the Roast.
        try:
            retval["message"] = f'{lookup_table[index]} \n **Roast #{str(index)}** <:roast_circle:474755210485563404>'
        except KeyError:
            retval["success"] = False
            # Roast doesn't exist in the lookup table.
            if index > 0 and index < self.total_roasts:
                retval["message"] = f'The roast you\'re trying to retrieve is censored and cannot be used in this guild.'
            retval["message"] = f'The roast does not exist!'
        return retval
    

    def _getLookupTable(self, allowed_groups: list = []):
        # Group 0 (no censor) is always allowed.
        lookup_table = self.roasts[0]

        # We want to find the other allowed groups
        for group in allowed_groups:
            lookup_table.update(self.roasts[group])
        return lookup_table