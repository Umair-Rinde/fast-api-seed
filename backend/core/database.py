from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    client = None

    @staticmethod
    async def connect():
        if Database.client is None:
            mongo_uri = os.getenv("MONGO_URI")
            db_name = os.getenv("DB_NAME")

            if "." in db_name:
                raise ValueError("Database name cannot contain a '.' character.")

            Database.client = AsyncIOMotorClient(mongo_uri)
            print("Connected to MongoDB.")

    @staticmethod
    def get_db():
        if Database.client is None:
            raise Exception(" Database is not connected. Call `Database.connect()` first.")
        return Database.client[os.getenv("DB_NAME")]

    @staticmethod
    async def close():
        if Database.client:
            Database.client.close()
            Database.client = None
            print("Database connection closed.")
