
<p align="center">
   <img src="https://user-images.githubusercontent.com/36930869/44614153-d8fe7a80-a7dc-11e8-98f3-c3e83a29b266.PNG" alt="roast bot logo"><br>
   <a href="https://discordbots.org/bot/461361233644355595"><img src="https://discordbots.org/api/widget/461361233644355595.svg" alt="discordbots.org widget" /></a>
</p>
<p align="center">
   <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python->%3D%203.11-blue?style=for-the-badge&logo=python" alt="python version 3.11 or newer required"/></a>
   <a href="https://github.com/ElheroLeGoat/Roast-Bot-Python/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge&logo=conventionalcommits" alt="Licensed under MIT"/></a>
</p>

# Roast Bot - The Python rewrite
**125** Roasts, More than **300** memes, Roast-Bot has everything you need to give your friends a warm welcome!

## Requirements:
- [Python 3.11 or newer](https://www.python.org/downloads/)
- [The zipped meme file](https://github.com/ElheroLeGoat/Roast-Bot-Python/blob/master/roastbot/resources/images/memes.zip)
   > You can download the zipped file directly and place it in roastbot/resources/images > The setup script will handle the rest.
   > memes.zip is saved with git LFS and simply downloading the sourcecode as ZIP results in corruption of the file.

## Setup:
1. Download Latest Release
2. execute `setup.py`
   > Renames `config.ini.dist` > `config.ini`
   > Generates a virtual environment for the bot to run in.
   > Installs all dependencies.
   > Generates the database required for the bot to function.
   > Unzips memes.zip.
3. Edit `config.ini` so all required information is added.
   * DISCORD.TOKEN

## Running the bot
Use `run.py` it's designed to 
1. Ease startup of the bot and.
2. Reboot the bot if it crashes.
## FaQ:
### Q) Why does the bot die when i closes the terminal window?
> **A)** make sure the `RUNTIME.HEADLESS` is set to `yes` in your `config.ini` and start the bot by executing `run.py`

### Q) Why does the bot die unexpectedly
> **A)** If you haven't changed the logging setting in the `config.ini` file you can find all logs under `roastbot/resources/logs`