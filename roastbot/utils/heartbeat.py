from datetime import datetime
from src.resources.globals import __CONFIG__ as config
import os
import pathlib

def GenerateHeartbeat() -> bool:
    """is function will generate the heartbeat file if it's enabled in the configuration

    Returns:
        bool: If heartbeat is disabled it will return None else boolean.
    """
    if not bool(config["HEARTBEAT"]["ENABLED"]):
        return None
    try:
        ct = datetime.now()
        filename = f'ROAST.{config["HEARTBEAT"]["FORMAT"]}.heartbeat'
        filename = filename.replace("%y", str(ct.year))\
            .replace("%d", str(ct.day))\
            .replace("%m", str(ct.month))\
            .replace("%H", str(ct.hour))\
            .replace("%M", str(ct.minute))\
            .replace("%S", str(ct.second))\
            .replace("%PID", str(os.getpid()))
        
        for file in pathlib.Path(config["HEARTBEAT"]["PATH"]).glob('ROAST*.heartbeat'):
            file.rename(filename)
        else:
            open(filename, "x").close()
        return True
    except Exception as e:
        pass
    return False

def checkheartbeat() -> bool:
    """Checks the current heartbeat file.

    Returns:
        bool: if heartbeats are disabled it will return none else boolean
    """
    if not bool(config["HEARTBEAT"]["ENABLED"]):
        return None
    
    heartbeat_files = list(pathlib.Path(config["HEARTBEAT"]["PATH"]).glob('ROAST*.heartbeat'))    
    if len(heartbeat_files) == 0 or len(heartbeat_files) > 1:
        # If there's no heartbeat files or there's more than one something went wrong.
        return False
    elif len(heartbeat_files) == 1:
        # if there's exactly one heartbeat file we want to regenerate.
        return True