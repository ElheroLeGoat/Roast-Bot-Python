# System Imports 
from typing import Union
import aiosqlite

# Discord Imports

# Project Imports
from ..resources import globals
from ..utils import logging

database_path = f'{globals.__PATHS__["RESOURCES"]}{globals.__SEP__}{"storage.db"}'

class Guild(object):
    """
    The Guild is simply an object for GetGuild
    it does not have any logic.
    """
    id: int = None
    censor: list = []
    urban: bool = None
    meme: bool = None
    
    
    def __init__(self, **attributes):
        for attribute, value in attributes.items():
            if hasattr(self, attribute):
                setattr(self, attribute, value)
            else:
                # Log Error, inconsistency in database and Guild object 
                continue

async def getGuild(id: int) -> Union[Guild, None]:
    """Retrieves a guild from the database.

    Args:
        id (int): The id of the guild

    Returns:
        Union[Guild, None] - Returns a Guild object if found else None
    """
    async with aiosqlite.connect(database_path) as con:
        con.row_factory = lambda cursor, row: Guild(id=row[0], censor=row[1].split(","), urban=bool(row[2]), meme=bool(row[3]))
        cur = await con.execute("SELECT * FROM guilds WHERE id = ?", (id,))
        fetch = await cur.fetchone()
        logging.debug(f'Fetched following values from the database: {fetch}')
        return fetch
    

async def createGuild(id: int, acg: list = [], urban: bool = True, meme: bool = True) -> bool:
    """Creates or updates a guild in the database (storage.db)

    Args:
        id (int): The guild ID
        acg (list, optional): allowed censor groups - the groups Roast can select from. Defaults to [].
        urban (bool, optional): Wether or not urban should be allowed. Defaults to True.
        meme (bool, optional): Wether or not memes should be allowed. Defaults to True.

    Returns:
        bool
    """
    values = {
        "id": id,
        "censor": ",".join(map(str, acg)),
        "urban": int(urban),
        "meme": int(meme)
    }
    try:
        async with aiosqlite.connect(database_path) as con:
            guild = await getGuild(id)
            if not guild:
                cur = await con.execute("INSERT INTO guilds (id, censor, urban, meme) VALUES (:id, :censor, :urban, :meme)", values)
            else:
                cur = await con.execute("UPDATE guilds SET censor=:censor, urban=:urban, meme=:meme WHERE id = :id", values)
            await con.commit()
        logging.debug(f'Successfully created a guild in the database with following values: {values}')
        return bool(cur.rowcount)
    except Exception as e:
        # Log error
        logging.debug(f'Unable to create a guild with values: {values} the error that occured was: {e}')
        return False