from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
import logging
from core.config import settings

class Database:
    _client: AsyncIOMotorClient = None
    _db = None

    @classmethod
    async def connect(cls):
        try:
            cls._client = AsyncIOMotorClient(settings.MONGO_URI)
            cls._db = cls._client[settings.MONGO_DB_NAME]
            logging.info("Connected to MongoDB")
        except PyMongoError as e:
            logging.error(f"Failed to connect to MongoDB: {e}")

    @classmethod
    async def close(cls):
        if cls._client:
            cls._client.close()
            logging.info("MongoDB connection closed")

    @classmethod
    def get_db(cls):
        if cls._db is None:
            raise Exception("Database is not connected. Call `Database.connect()` first.")
        return cls._db
