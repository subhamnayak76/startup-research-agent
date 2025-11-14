import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.user import User
from dotenv import load_dotenv

load_dotenv()


class Database:
    client : AsyncIOMotorClient = None


database = Database()

async def connect_to_mongo():

    
    
    database.client = AsyncIOMotorClient(os.getenv("mongo_url", "mongodb://localhost:27017"))
    await init_beanie(
        database = database.client.startup,
        document_models=[User]
    )
    print(f"Successfully connected to DB")


async def close_mongo_connection():
    database.client.close()