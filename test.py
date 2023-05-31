import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import motor
import pprint

uri = "mongodb://root:Rpuls4rL3ss@rpulsarless.freeddns.org:29097/?authSource=admin"


async def ping_server():
    # Replace the placeholder with your Atlas connection string
    # Set the Stable API version when creating a new client
    # Send a ping to confirm a successful connection
    try:
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

async def do_find_one():
    document = await client['prontopro']['reviews'].find_one()
    pprint.pprint(document)

async def insert(collection: str, document: dict) -> str:
    result = await client["tests"][collection].insert_one(document)
    return str(result.inserted_id)

async def main():

    await ping_server()
    res = await insert("docs", {"name": "Christian"})
    print(res)

client = motor.motor_asyncio.AsyncIOMotorClient(uri)
asyncio.run(ping_server())
asyncio.run(ping_server())

