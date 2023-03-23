# System imports
import os
import logging as log_lib

# Project imports
from ..resources.globals import __CONFIG__ as config
from .types import ConvertBool

log_lib.getLogger("main")
log_lib.basicConfig(filename="roast_unordered_log.log", level=log_lib.ERROR, datefmt=config["LOGGING"]["DATE.FORMAT"])

def filter(record: log_lib.LogRecord):
    path_list = record.pathname.split(os.path.sep)
    cog = path_list[-2] if path_list[-2] not in ['resources', 'controls', 'roastbot'] else 'main'
    file = path_list[-1].rstrip('.py')
    if file != 'main':
        record.cog = f'{cog} - {file}'
    else:
        record.cog = cog
    return record


ErrorLog = log_lib.getLogger('roast_errors')
InfoLog = log_lib.getLogger('roast_info')

if ConvertBool(config["RUNTIME"]["DEBUG"]):
    ErrorLog.setLevel(log_lib.DEBUG)
else:
    ErrorLog.setLevel(log_lib.WARNING)
InfoLog.setLevel(log_lib.INFO)

ErrorFileHandler = log_lib.FileHandler('roast_log.log')
InfoFileHandler = log_lib.FileHandler('roast_log.log')
ErrorFileHandler.addFilter(filter)

ErrorFileHandler.setFormatter(log_lib.Formatter(config["LOGGING"]["LOG.FORMAT"]))
InfoFileHandler.setFormatter(log_lib.Formatter('%(message)s'))

ErrorLog.addHandler(ErrorFileHandler)
InfoLog.addHandler(InfoFileHandler)

info     = InfoLog.info
debug    = ErrorLog.debug
error    = ErrorLog.error
warning  = ErrorLog.warning
critical = ErrorLog.critical