# SETUP SCRIPT
# This script makes it easy to setup the correct venv.
import sys
import subprocess
import configparser
import sqlite3
import pathlib
from roastbot.utils.types import wrap

if sys.version_info.major < 3 or (sys.version_info.major == 3 and sys.version_info.minor < 11):
    print(f'Roastbot requires python version >3.11 in order to run, current version: {sys.version}')
    exit(1)

banner = """
______ _____  ___   _____ _____  ______  _____ _____  \r
| ___ \  _  |/ _ \ /  ___|_   _| | ___ \|  _  |_   _| \r
| |_/ / | | / /_\ \\\ `--.  | |   | |_/ /| | | | | |  \r
|    /| | | |  _  | `--. \ | |   | ___ \| | | | | |   \r
| |\ \\\ \_/ / | | |/\__/ / | |   | |_/ /\ \_/ / | |  \r
\_| \_|\___/\_| |_/\____/  \_/   \____/  \___/  \_/   \r
            _____ _____ _____ _   _______             \r
           /  ___|  ___|_   _| | | | ___ \            \r
           \ `--.| |__   | | | | | | |_/ /            \r
            `--. \  __|  | | | | | |  __/             \r
           /\__/ / |___  | | | |_| | |                \r
           \____/\____/  \_/  \___/\_|                \r
"""
print(banner)


print(f'Setting Global Variables \n')
__ROOT__ = pathlib.Path(__file__).parent
__CONFIG__ = configparser.ConfigParser()
__CONFIG__.sections()
__CONFIG__.read(pathlib.Path.joinpath(__ROOT__, "roastbot", "resources", "config.ini.dist"))

print(f'Renaming: roastbot/resources/config.ini.dist to config.ini \n')
try:
    path = pathlib.Path.joinpath(__ROOT__, "src", "resources")
    file = pathlib.Path.joinpath(path, "config.ini.dist")
    file.rename(pathlib.Path.joinpath(path, "config.ini"))
    print(f'Renaming successfull \n')
except Exception as e:
    if "already exists" in str(e):
        print(wrap("config.ini already exists"))
    else:
        print(wrap("[ERROR] unexpected error occured when renaming"))
        print(e)
        

venv_path = pathlib.Path.joinpath(__ROOT__, __CONFIG__["SETUP"]["VENV.NAME"])
# Generate our VirtualEnv
print(f'Generating a new Virtual environment in: {venv_path} \n')
try:
    if not pathlib.Path.exists(venv_path):
        with subprocess.Popen(f'python -m venv {venv_path}', shell=True) as proc:
            pass
        print('Virtual Environment generated \n')
    else:
        print(wrap('Virtual Environment already exists'))
except Exception as e:
    print(wrap("[ERROR] unable to generate virtual env"))
    print(e)
    exit(1)

# Installing Dependencies inside the venv
print(f'Installing all dependencies \n')
try:
    requirements = pathlib.Path.joinpath(__ROOT__, "requirements.txt")
    activate     = pathlib.Path.joinpath(venv_path, "Scripts", "activate")
    if sys.platform == "linux":
        # @TODO: ADD linux logic for RUN script
        print("The runtime and setup script does not support linux yet.")
        exit(1)
    elif sys.platform == "win32":
        with subprocess.Popen(f'{activate} && python -m pip install -r {requirements}', shell=True) as proc:
            pass
    print("\n"+wrap("Dependencies installed with no issues"))
except Exception as e:
    print(wrap("[ERROR] Unable to install required packages"))
    print(e)
    exit(1)

print("Creating database in roastbot/resources")
connection = sqlite3.connect(pathlib.Path.joinpath(__ROOT__, "roastbot", "resources", "storage.db"))
c = connection.cursor()
c.execute("CREATE TABLE guilds(id, censor, urban, meme)")
