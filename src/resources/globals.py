import configparser
import os
from pathlib import Path
# Path Globals
# We probably doesn't need em but hey, now we have em.
__ROOTPATH__ = Path(__file__).parent.parent
__PATHS__ = {
    "ROOT": __ROOTPATH__,
    "RESOURCES": Path.joinpath(__ROOTPATH__, "resources"),
    "COGS": Path.joinpath(__ROOTPATH__, "cogs"),
    "UTILS": Path.joinpath(__ROOTPATH__, "utils")
}

# Setting the config globally so it's easy to change one place.
__CONFIG__ = configparser.ConfigParser()
__CONFIG__.sections()
__CONFIG__.read(f'{__PATHS__["RESOURCES"]}{os.path.sep}config.ini')