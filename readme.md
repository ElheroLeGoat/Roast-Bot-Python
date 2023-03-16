![Roast bot logo](https://user-images.githubusercontent.com/36930869/44614153-d8fe7a80-a7dc-11e8-98f3-c3e83a29b266.PNG)

[![Discordbots widget](https://discordbots.org/api/widget/461361233644355595.svg)](https://discordbots.org/bot/461361233644355595)


# Roast Bot - The Python rewrite
[![Made with python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

**125** Roasts, More than *300* memes, Roast-Bot has everything you need to give your friends a warm welcome!

## Requirements:
- [Python 3.11.2 or newer](https://www.python.org/downloads/)
- [Py-cord 2.4.0](https://pypi.org/project/py-cord/)

## Setup:
1. Download Latest Release
2. execute `setup.py`
   > This will rename `config.ini.dist` > `config.ini`, create the `virtual environment` and install all `dependencies`
3. Edit `config.ini` so all required information is added.

## Running the bot
you can execute: `run.py` to easily run the bot.
if you don't want to use `run.py` you can always run the `src/roastbot.py` directly, however doing this prevents the config `RUNTIME.HEADLESS` from working properly, on windows you can read up on `pythonw` and on linux `nohub` to get around this.

## FaQ:
### Q) Why does the bot die when i closes the terminal window?
> **A)** make sure the `RUNTIME.HEADLESS` is set to `yes` in your `config.ini` and start the bot by executing `run.py`

### Q) Why does the bot die unexpectedly
> **A)** If you haven't changed the logging setting in the `config.ini` file you can find all logs under `src/resources/logs`

### Q) Is there a way to see if the bot is online?
> **A)** running `/roast_status` will show you the status of your active bot instance.
> If this does not work, the bot will generate a heartbeat file in the root, here you should be able to see when it last responded.
