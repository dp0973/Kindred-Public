from aiohttp import ClientSession
import os
import static_data
from typing import Any, Optional, Union

from utils.db.mongo import Mongo
from utils.static.data import regions


class MongoRequest(Mongo):
    def __init__(self):
        super().__init__(os.environ['MONGO_DB'])
        self.regions = regions

    async def get_region(self, user_id: int) -> Optional[str]:
        if region := await self.get_user_region(user_id):
            return region

        return None

    async def set_region(self, user_id: int, region: str) -> bool:
        if region in self.regions:
            if await self.get_user_region(user_id):
                return await self.update_user_region(user_id, region)

            return await self.register_user_region(user_id, region)
        
        return False

class BaseRequest:
    def __init__(self, base_url: Optional[str] = None):
        self.BASE_URL = base_url if base_url else ''

    async def request(self, url: str, return_type: str) -> Union[dict[str, Any], bytes, str]:
        async with ClientSession() as session:
            async with session.get(self.BASE_URL+url) as response:
                if return_type == 'json':
                    return await response.json()

                if return_type == 'bytes':
                    return await response.read()
                
                return await response.text()

class RiotRequest(BaseRequest):
    def __init__(self):
        super().__init__('http://ddragon.leagueoflegends.com/')
        self.ddragon = static_data.ddragon()
        self.version = None
        self.type = {
            'champion': 'champion.json',
            'summoner': 'summoner.json',
            'item': 'item.json',
            'perk': 'runesReforged.json'
        }

    async def set_version(self) -> dict[str, Any]:
        versions = await self.request('api/versions.json', 'json')
        self.version = versions[0]

    async def get_ddragon(self, type: str) -> dict[str, Any]:
        if version := self.version:
            return await self.request(f'cdn/{version}/data/en_US/{self.type[type]}', 'json')
        
        await self.set_version()
        return await self.request(f'cdn/{self.version}/data/en_US/{self.type[type]}', 'json')

    def get_id_by_key(self, key: int, mode: str) -> str:
        if mode == 'champion':
            return self.ddragon.getChampion(key).id

        return self.ddragon.getSummoner(key).id

    def get_name_by_key(self, key: int, mode: str) -> str:
        if mode == 'champion':
            return self.ddragon.getChampion(key).name

        return self.ddragon.getSummoner(key).name

    async def get_perk_ids(self):
        perk_list: list[int] = []
        perks = await self.get_ddragon('perk')
        for category in perks:
            for slot in category['slots']:
                for rune in slot['runes']:
                    perk_list.append(rune['id'])

        return perk_list
