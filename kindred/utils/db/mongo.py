from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional


class Mongo:
    def __init__(self, db_url: str):
        self.__client = AsyncIOMotorClient(db_url)
        self.__user_data = self.__client.region.user_data

    async def register_user_region(self, user_id: int, user_region: str) -> bool:
        await self.__user_data.insert_one({'user_id': user_id, 'user_region': user_region})
        return True

    async def get_user_region(self, user_id: int) -> Optional[str]:
        user_data = await self.__user_data.find_one({'user_id': user_id})
        return user_data['user_region'] if user_data else None

    async def update_user_region(self, user_id: int, user_region: str) -> bool:
        await self.__user_data.update_one({'user_id': user_id}, {'$set': {'user_region': user_region}})
        return True
