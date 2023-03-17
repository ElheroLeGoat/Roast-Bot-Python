import random
import json
from ...resources import globals

# class Roast(commands.Cog):
class RoastLogic():

    """The Roast Dictionary
    The dictionary structure is as following:
    {
        "censor_group_id"
        {
            "roast_id": "roast Goes here" 
        }
    }
    """
    roasts: dict = {}
    
    """The Censor Group list. they can be found in roasts.json
    """
    censor_groups: list = []

    """The total amount of roasts loaded to determine if the roast a person is specifying exists or is just not present in the allowed groups
    """
    total_roasts: int = 0

    def __init__(self):
        self.LoadRoasts()
    

    def ReloadRoasts(self) -> None:
        """Alias for LoadRoasts
        """
        return self.LoadRoasts()

    def LoadRoasts(self) -> None:
        """Loads the roasts into memory
        """
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

    def SearchRoast(self, search_param: str, acg: list = []) -> dict:
        """Searches the roast list in the allowed groups.

        Args:
            search_param (str): The search string to look for (Case Insensitive)
            agc (list, optional): The groups allowed, these can be seen in resources/roasts.json and starts at 0. Defaults to [].

        Returns:
            dict[succes, message]: Returns the possible success.
        """
        lookup_table = self._getLookupTable(acg)

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


    def GetRoast(self, agc: list = [], roast_id: int = None) -> dict:
        """Retrieve a roast, either random or by the roast_id

        Args:
            agc (list, optional): The groups allowed, these can be seen in resources/roasts.json and starts at 0. Defaults to [].
            roast_id (int, optional): The roast ID if one is looking for a specific roast. Defaults to None.

        Returns:
            dict[succes, message]: Returns the possible success.
        """
        retval = {"success": True}
        lookup_table = self._getLookupTable(agc)

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
    

    def _getLookupTable(self, agc: list = []) -> dict:
        """Private Method to retrieve the Lookup Table.

        Args:
            agc (list, optional): The groups allowed, these can be seen in resources/roasts.json and starts at 0. Defaults to [].

        Returns:
            dict: All the roasts in their dictionaries.
        """
        # Group 0 (no censor) is always allowed.
        lookup_table = self.roasts[0]

        # We want to find the other allowed groups
        for group in agc:
            lookup_table.update(self.roasts[group])
        return lookup_table