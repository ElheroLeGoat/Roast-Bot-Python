# System Imports
import os
from datetime import datetime
from typing   import Union
from pathlib  import Path

# Discord Imports

# Project Imports
from ..resources.globals import __CONFIG__ as config
from .types import Singleton
from . import logging

class Heartbeat(metaclass=Singleton):
    """The Heartbeat Class is used to generate and track specific heartbeat files. these files is used by a human to:
        
        Humans can use the specific .heartbeat files to:
        a) Check if the bot is still running
        b) Kill the bot (by deleting the heartbeat file)
        
        An Auto-reboot script can use the .heartbeat files to:
        a) make sure the bot is still running
            - If not Restart or alert the server owner.
        b) Kill itself if the file is deleted.

    Raises:
        FileNotFoundError: The class will raise FileNotFound in some methods, check the method docstring to see what method raises this and when.
        RuntimeError: If the class is instantiated using isMainScript = False, Following methods will raise this error: MakeFile, UpdateFile, CleanOldFiles
    """
    filePath: Path
    absPath: Path
    filename: str
    isMainScript: bool

    def __init__(self, isMainScript: bool = True) -> None:
        self.absPath = Path(config["HEARTBEAT"]["PATH"]) if config["HEARTBEAT"]["PATH"] else  Path(__file__).parent.parent.parent
        self.isMainScript = isMainScript
        if not self.isMainScript:
            self.filePath = self.GetNewestFile()
            logging.debug(f'[HEARTBEAT - rebooter] tracking file {self.filePath}')
        else: 
            self.filename = f'{config["HEARTBEAT"]["FILENAME"]}.{os.getpid()}.heartbeat'
            self.filePath = Path.joinpath(self.absPath, self.filename)
            logging.debug(f'file will be stored at {self.absPath} with filename {self.filename}')

    def GetFile(self) -> Union[None, Path]:
        """Retrieves the absolute file path if it exists

        Returns:
            Union[None, Path]: Returns None if the file does not exist.
        """
        if not self.filePath.is_file():
            return None
        return self.filePath
        
    def MakeFile(self) -> bool:
        """Generates the heartbeat file

        Raises:
            RuntimeError: If a script uses this class with isMainScript=False this will be raised when running.

        Returns:
            bool: Returns Fales if the file already exists, else True.
        """
        self._checkScript('MakeFile')
        if self.GetFile():
            logging.debug('A request to make a Heartbeat file was made but the file already exists.')
            return False
        
        time = datetime.now().strftime("%Y-%m-%dT%H:%M")
        with open(self.filePath, "w+") as file:
            file.write(time)

        logging.debug(f'A request to make a Heartbeat file was made the file is saved with the timestamp: {time}')
        return True

    def UpdateFile(self) -> None:
        """Updates the file with the new timestamp

        Raises:
            FileNotFoundError: If the file does not exist this will be raised (can be used to kil the bot.)
            RuntimeError: If a script uses this class with isMainScript=False this will be raised when running.
        """
        self._checkScript('UpdateFile')
        if not self.GetFile():
            logging.debug(f'A request to update the Heartbeat file was made, but the file does not exist.')
            raise FileNotFoundError('Make sure to run MakeFile before trying to update it.')

        time = datetime.now().strftime("%Y-%m-%dT%H:%M")
        with open(self.filePath, "w") as file:
            file.truncate(self.filePath.stat().st_size)
            file.write(time)
        logging.debug(f'A request to update the Heartbeat file was made, new time set: {time}')

    def CleanOldFiles(self) -> None:
        """Removes old .heartbeat files that is not in use anymore.

        Raises:
            RuntimeError: If a script uses this class with isMainScript=False this will be raised when running.
        """
        self._checkScript('CleanOldFiles')
        for file in list(self.absPath.glob(f'{config["HEARTBEAT"]["FILENAME"]}.*.heartbeat')):
            if file == self.filePath:
                continue
            os.remove(file)

    def _checkScript(self, method: str) -> None:
        """A small internal wrapper method to check if the class is instantiated using isMainScript=False, if this is the case it'll raise RuntimeError.

        Args:
            action (str): The method to raise the RuntimeError for.

        Raises:
            RuntimeError: Raises RuntimeError if isMainScript is false.
        """
        if not self.isMainScript:
            raise RuntimeError(f'This action {method} is only allowed by the main script.')


    def GetNewestFile(self) -> Union[Path, None]:
        """Retrieves the newest file. This function is mainly used by the auto-reload script

        Returns:
            Union[Path, None]: If the file is found it'll return the Absolute path else None
        """
        f: Path = None
        for file in list(self.absPath.glob(f'{config["HEARTBEAT"]["FILENAME"]}.*.heartbeat')):
            if not f or file.stat().st_mtime > f.stat().st_mtime:
                f = file
        return f
    
    def GetUpdateTime(self) -> datetime:
        """Retrieves the Timestamp inside the file.

        Raises:
            FileNotFoundError: If the file does not exist this will be raised (can be used to kil the bot.)

        Returns:
            datetime: A datetime object of the stored time.
        """
        if not self.GetFile():
            raise FileNotFoundError()
        
        with open(self.filePath, "r") as file:
            return datetime.strptime(file.readline(-1), "%Y-%m-%dT%H:%M")