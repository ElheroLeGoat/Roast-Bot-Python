from datetime import datetime

from ..resources.globals import __CONFIG__ as config
from .types import Singleton
from pathlib import Path
import os
import pathlib

print(__file__)


class Hearbeat(metaclass=Singleton):
    pattern = "ROAST.*.heartbeat"


    @staticmethod
    def _RetrieveFileList() -> list:
        hbPath = config["HEARTBEAT"]["PATH"]
        if not hbPath:
            hbPath = Path(__file__).parent.parent.parent  

        return list(Path(hbPath).glob("ROAST.*.HEARTBEAT"))

    def _RemoveFiles(self, files: list) -> bool:
        """Removes files in a list.

        Args:
            files (list): The file needs to have the absolute path.

        Returns:
            bool: False if there were no files, true if there were and they got removed.
        """
        if not files:
            return False

        for file in files:
            os.remove(file)

        return True

    @staticmethod
    def _GenerateFilename(time: datetime) -> str:
        return f'ROAST.{config["HEARTBEAT"]["FORMAT"]}.heartbeat'\
        .replace("%y", time.strftime("%y")) \
        .replace("%m", time.strftime("%m")) \
        .replace("%d", time.strftime("%d")) \
        .replace("%H", time.strftime("%H")) \
        .replace("%M", time.strftime("%M")) \
        .replace("%S", time.strftime("%S")) \
        .replace("%P", str(os.getpid())) \
        .replace("%U", os.getlogin())

    def _GenerateHBFile(self) -> str:
        ct = datetime.now()
        filename = self._GenerateFilename(ct)
        f = open(filename, "x")
        f.write(ct.strftime("%y-%m-%dT%H:%M"))
        f.close()
        return Path()

    def GetActiveHBFile(self, generate: bool = True, cleanup: bool = False) -> Path:
        files = self._RetrieveFileList()

        print(files)
        file = None

        if not files and generate:
            print("Creating file")
            self._GenerateHBFile()

        if len(files) > 1 and cleanup:
            file = files.pop(0)
            self._RemoveFiles(files)
        return files[0] if files else file

    def CreateHeartbeat(self, generate: bool = True, cleanup: bool = True) -> None:
        ct = datetime.now()
        file = self.GetActiveHBFile(generate, False)
        file.rename(self._GenerateFilename(datetime.now()))
        with file.open("w") as f:
            f.truncate(file.stat().st_size)
            f.write(ct.strftime("%y-%m-%dT%H:%M"))