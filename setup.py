# SETUP SCRIPT
# This script makes it easy to setup the correct venv.
import sys, subprocess, configparser, sqlite3, pathlib, zipfile, time
from roastbot.utils.types import wrap

if sys.version_info.major < 3 or (sys.version_info.major == 3 and sys.version_info.minor < 11):
    print(f'Roastbot requires python version >3.11 in order to run, current version: {sys.version}')
    exit(1)

start_time = time.process_time()
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


####################
# GLOBAL VARIABLES #
####################
print(wrap('Setting Global Variables'))
__ROOT__ = pathlib.Path(__file__).parent
__CONFIG__ = configparser.ConfigParser()
__CONFIG__.sections()
__CONFIG__.read(pathlib.Path.joinpath(__ROOT__, "roastbot", "resources", "config.ini.dist"))

###########################
# CONFIGURATION UNPACKING #
###########################
print(wrap('Renaming roastbot/resources/config.ini.dist to config.ini'))
try:
    path = pathlib.Path.joinpath(__ROOT__, "roastbot", "resources")
    file = pathlib.Path.joinpath(path, "config.ini.dist")
    file.rename(pathlib.Path.joinpath(path, "config.ini"))
    print('Renaming successfull\n')
except Exception as e:
    if "already exists" in str(e):
        print('[INFO] config.ini already exists.\n')
    else:
        print('[ERROR] does config.ini.dist exist? (unknown error)\n')
        print(e)
        
###################
# VENV GENERATION #
###################
venv_path = pathlib.Path.joinpath(__ROOT__, __CONFIG__["SETUP"]["VENV.NAME"])
print(wrap(f'Generating a new Virtual environment in {venv_path}'))
try:
    if not pathlib.Path.exists(venv_path):
        with subprocess.Popen(f'py -m venv {venv_path}', shell=True) as proc:
            pass
        print('Virtual Environment generated.\n')
    else:
        print('[INFO] Virtual environment already exists.\n')
except Exception as e:
    print('[ERROR] Unable to generate virtual environment.\n')
    print(e)
    exit(1)

###########################
# DEPENDENCY INSTALLATION #
###########################
print(wrap('Installing all dependencies'))
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
    print('Dependencies installed with no issues.')
except Exception as e:
    print('[ERROR] Unable to install required packages')
    print(e)
    exit(1)

#######################
# DATABASE GENERATION #
#######################
print('\n'+wrap('Generating database in roastbot/resources/storage.db'))
try:
    connection = sqlite3.connect(pathlib.Path.joinpath(__ROOT__, "roastbot", "resources", "storage.db"))
    c = connection.cursor()
    c.execute("CREATE TABLE guilds(id, censor, urban, meme)")
except Exception as e:
    if 'already exists' in str(e):
        print('[INFO] Table guilds already exists.\n')
    else:
        print('[ERROR] Something went wrong creating the database.\n')
        print(e)


##################
# MEME UNZIPPING #
##################
print(wrap('Unzipping Memes in roastbot/resources/images'))
try:
    imgpath = pathlib.Path.joinpath(__ROOT__, 'roastbot', 'resources', 'images')
    with zipfile.ZipFile(pathlib.Path.joinpath(imgpath, 'memes.zip'), 'r') as ref:
        ref.extractall(imgpath)
except Exception as e:
    print('[ERROR] Unable to unzip memes.zip, you can do this manually though.')
    print(e)
print(wrap('Setup complete', 'Please check the print', 'to make sure no errors occured.', f'Time spent: {(time.process_time() - start_time)} seconds'))