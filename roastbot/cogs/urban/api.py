import aiohttp
import json

class UrbanApi:
    uri: str = "https://api.urbandictionary.com/v0/"

    @staticmethod
    async def aiohttpWrapper(uri):
        async with aiohttp.ClientSession() as session:
            async with session.get(uri) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    async def LookupByWord(self, search: str):
        data = await self.aiohttpWrapper(f'{self.uri}define?term={search}')
        if data:
            content = data['list'][0]
            return {"permalink":content["permalink"],
                    "definition": content['definition'],
                    "example": content["example"],
                    "author": content["author"],
                    "thumbs_up": content["thumbs_up"],
                    "thumbs_down": content["thumbs_down"]}
        else:
            return await self.LookupByDefId(11084370)

    async def LookupByDefId(self, defid: int):
        data = await self.aiohttpWrapper(f'{self.uri}define?defid={defid}')
        if data:
            content = data['list'][0]
            return {"permalink":content["permalink"],
                    "definition": content['definition'],
                    "example": content["example"],
                    "author": content["author"],
                    "thumbs_up": content["thumbs_up"],
                    "thumbs_down": content["thumbs_down"]}
        return None