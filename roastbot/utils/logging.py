# System imports
import os
import logging as log_lib
from pathlib import Path
# Discord imports
import discord

# Project imports
from ..resources.globals import __CONFIG__ as config
from ..resources.globals import config
from ..resources.globals import paths

path = Path.joinpath(paths.RESOURCES, 'logs')
if config.LOGGING.PATH:
    path = Path(config.LOGGING.PATH)  
path.mkdir(exist_ok=True, parents=True)

log_lib.getLogger("main")
log_lib.basicConfig(filename=Path.joinpath(path, 'unordered_log.log'), level=log_lib.ERROR, datefmt=config.LOGGING.DATE.FORMAT)

def filter(record: log_lib.LogRecord):
    path_list = record.pathname.split(os.path.sep)
    cog = path_list[-2] if path_list[-2] not in ['resources', 'controls', 'roastbot'] else 'main'
    file = path_list[-1].rstrip('.py')
    if file == "logging":
        record.cog = f'Command Logger'
    elif file not in ["main", "__main__"]:
        record.cog = f'{cog.upper()} - {file}'
    else:
        record.cog = cog
    return record

def CommandLogger(ctx: discord.ApplicationContext, command: str, response: str):
        debug(f'[SHARD {ctx.guild.shard_id}] "{ctx.author.name}#{ctx.author.discriminator}" ran command "/{command}" in "{ctx.guild.name}" and recieved {response}')

ErrorLog = log_lib.getLogger('roast_errors')
InfoLog = log_lib.getLogger('roast_info')

if config.LOGGING.DEBUG:
    ErrorLog.setLevel(log_lib.DEBUG)
else:
    ErrorLog.setLevel(log_lib.WARNING)
InfoLog.setLevel(log_lib.INFO)

ErrorFileHandler = log_lib.FileHandler(Path.joinpath(path, 'roast_log.log'))
InfoFileHandler = log_lib.FileHandler(Path.joinpath(path, 'roast_log.log'))
ErrorFileHandler.addFilter(filter)
ErrorFileHandler.setFormatter(log_lib.Formatter(config.LOGGING.LOG.FORMAT))
InfoFileHandler.setFormatter(log_lib.Formatter('%(message)s'))

ErrorLog.addHandler(ErrorFileHandler)
InfoLog.addHandler(InfoFileHandler)

info     = InfoLog.info
debug    = ErrorLog.debug
error    = ErrorLog.error
warning  = ErrorLog.warning
critical = ErrorLog.critical