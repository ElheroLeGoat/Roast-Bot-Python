import sys
import subprocess
import pathlib
from src.utils.types import ConvertBool, wrap
from src.resources.globals import __CONFIG__, __PATHS__
banner = """
______ _____  ___   _____ _____  ______  _____ _____  \r
| ___ \  _  |/ _ \ /  ___|_   _| | ___ \|  _  |_   _| \r
| |_/ / | | / /_\ \\\ `--.  | |   | |_/ /| | | | | |  \r
|    /| | | |  _  | `--. \ | |   | ___ \| | | | | |   \r
| |\ \\\ \_/ / | | |/\__/ / | |   | |_/ /\ \_/ / | |  \r
\_| \_|\___/\_| |_/\____/  \_/   \____/  \___/  \_/   \r
    ______ _   _ _   _ _____ _____  _____ _           \r
    | ___ \ | | | \ | |_   _|  _  ||  _  | |          \r
    | |_/ / | | |  \| | | | | | | || | | | |          \r
    |    /| | | | . ` | | | | | | || | | | |          \r
    | |\ \| |_| | |\  | | | \ \_/ /\ \_/ / |____      \r
    \_| \_|\___/\_| \_/ \_/  \___/  \___/\_____/      \r
"""
print(banner)
if sys.version_info.major < 3 or (sys.version_info.major == 3 and sys.version_info.minor < 11):
    print(f'Roastbot requires python version >3.11 in order to run, current version: {sys.version}')
    exit(1)

venv_path = pathlib.Path.joinpath(__PATHS__["ROOT"].parent, __CONFIG__["SETUP"]["VENV.NAME"])
activate = pathlib.Path.joinpath(venv_path, "Scripts", "activate")

if not ConvertBool(__CONFIG__["RUNTIME"]["HEADLESS"]):
    print(wrap(f'The python bot is **NOT** running in headless therefore you cant close this window'))
    print(f'Activating virtual env and starting the bot.')
    with subprocess.Popen(f'{activate} && python sandbox.py', shell=True) as proc:
        pass
else:
    print(wrap(f'the python bot will be running in headless mode.'))
    print(f'Activating virtual env and starting the bot. \n')
    if sys.platform == "linux":
        # @TODO: ADD linux logic for RUN script
        print("The runtime and setup script does not support linux yet.")
        exit(1)
    elif sys.platform == "win32":
        f = subprocess.Popen(f'{activate} && python sandbox.py', shell=True)

    print("you may now close the window")