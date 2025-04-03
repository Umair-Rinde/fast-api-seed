from pydantic_settings import BaseSettings
from .database import Database
from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await Database.connect()
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        raise
    yield 
    await Database.close()


class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str

    class Config:
        env_file = "core/.env"

settings = Settings()
