import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from typing import Any


class AsyncMongo:
    def __init__(self, uri: str, db: str):
        self.uri = uri
        self.db = db
        self.client = AsyncIOMotorClient(self.uri, server_api=ServerApi('1'))
        asyncio.run(self.ping_server())

    async def ping_server(self):
        client = AsyncIOMotorClient(self.uri, server_api=ServerApi('1'))
        # Replace the placeholder with your Atlas connection string
        # Send a ping to confirm a successful connection
        try:
            await client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print("No database connection", e)
            exit(1)

    async def insert(self, collection: str, document: dict) -> Any:
        try:
            client = AsyncIOMotorClient(self.uri, server_api=ServerApi('1'))
            result = await client[self.db][collection].insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            print(e)

    async def find_all(self, collection: str, match: dict):
        cursor = self.client[self.db][collection].find(match)
        return [doc for doc in await cursor.to_list(length=100)]

    async def aggregate(self, collection: str, pipeline: list):
        return [doc async for doc in self.client[self.db][collection].aggregate(pipeline)]
