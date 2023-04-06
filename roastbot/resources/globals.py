# System Imports
import os, datetime, configparser
from typing import Union
from pathlib import Path

# Discord Imports

# Project Imports
from ..utils.types import obj

# Path Globals
# We probably doesn't need em but hey, now we have em.
__ROOTPATH__ = Path(__file__).parent.parent
__PATHS__ = {
    "ROOT": __ROOTPATH__,
    "RESOURCES": Path.joinpath(__ROOTPATH__, "resources"),
    "COGS": Path.joinpath(__ROOTPATH__, "cogs"),
    "UTILS": Path.joinpath(__ROOTPATH__, "utils")
}

paths = obj("paths")
paths.set("ROOT", __ROOTPATH__)
paths.set("RESOURCES", Path.joinpath(__ROOTPATH__, "resources"))
paths.set("COGS", Path.joinpath(__ROOTPATH__, "cogs"))
paths.set("UTILS", Path.joinpath(__ROOTPATH__, "utils"))


__SEP__ = os.path.sep
__VERSION__ = "1.0.0"
__START_TIME__ = datetime.datetime.now()
# ANYTHING BELOW IS CONFIG BASED
class cfg(obj):
    """Welcome to the Hell of fixing configuration in Python.
    This class uses a custom object class "obj" as it's parent that just guarantees that if an key does not exist, it'll simply return None.

    The purpose of this class is to:
        1) Imitate the behavior of an .ini file
        2) Typecast the strings into its proper format.
    
    **NOTE**
    In order for this class to function properly there're 2 keywords to keep in mind:
        1) The name (left side of the =) the . is reserved to determine a sub-category or value. this is to make it easier on the eyes.
        2) The value (Right side of the =) a "c,s,v" surrounded by $[] imitates a list in python.
    > There's no tuples or dictionaries in this class.
    
    **EXAMPLE**

    .ini file:
    [EXAMPLE]
    A.A = hello
    A.B = World
    B.A = this
    B.B = is
    c   = $[a, test, 10, 3.14]
    
    Would be transformed into:
    cfg.EXAMPLE.A.A = str(Hello)
    cfg.EXAMPLE.A.B = str(World)
    cfg.EXAMPLE.B.A = str(this)
    cfg.EXAMPLE.B.B = str(is)
    cfg.EXAMPLE.c   = list([str(a), str(test), int(10), float(3.14)])
    """

    def __init__(self, _name: str, parser: configparser.ConfigParser):
        self.parser = parser
        self._loop_sections()

    def _loop_sections(self) -> None:
        """Internal method to loop all sections found in the parser.
        """
        for section_name in self.parser.sections():
            section_object = obj(section_name)
            for item in self.parser[section_name].items():
                value = self._verify_type(item[1])
                if "." in item[0]:
                    section_object.set(*self._get_sub_section(item[0].upper(), value, section_object))
                section_object.set(item[0].upper(), value)
            self.set(section_name, section_object)

    def _get_sub_section(self, _name: str, value: any, parent: obj) -> list:
        """A looping method that will generate sub sections based on the keyword: .

        Args:
            _name (str): The name of the sub section
            value (any): The value the sub section holds.
            parent (obj): The parent section

        Returns:
            list: [name, value]
        """
        split_name = _name.split(".", 1)
        section = parent.get(split_name[0])
        if not section:
            section = obj(split_name[0])

        # IF . is found in the name
        if not "." in split_name[1]:
            section.set(split_name[1], value)
        else:
            section.set(*self._get_sub_section(split_name[1], value, section))
        return (split_name[0], section)

    def _verify_type(self, item: str) -> Union[None, bool, int, str, float, list]:
        """Takes an item (str) and translates it into 4 different types:
            1) None - If empty
            2) INT
            3) Float
            4) List - Given keywords: $[] is found

        Args:
            item (str): The item value to typecast.

        Returns:
            Union[int, str, float, list]: The method basically typecasts
        """
        try:
            if not item:
                return None
            elif item.lower() in ["yes", "yep", "true", "$1", "active"]:
                return True
            elif item.lower() in ["no", "nope", "false", "$0", "inactive"]:
                return False
            elif item.isnumeric():
                # The item is an integer, we'll just return it as an int.
                return int(item)
            elif item.strip().startswith("$[") and item.strip().endswith("]"):
                # The item is a list.
                l = []
                litems = item.strip("$[]").split(",")
                for litem in litems:
                    l.append(self._verify_type(litem.strip()))
                return l
            return float(item)
        except ValueError:
            return item

# Setting the config globally so it's easy to change one place.
__CONFIG__ = configparser.ConfigParser()
__CONFIG__.sections()
__CONFIG__.read(f'{__PATHS__["RESOURCES"]}{os.path.sep}config.ini')
config = cfg("config", __CONFIG__)