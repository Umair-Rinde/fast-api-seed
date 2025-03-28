from fastapi import FastAPI
from accounts.routes import router as account_router
from contextlib import asynccontextmanager
from core.database import Database


app = FastAPI()

app.include_router(account_router, prefix="/api/accounts", tags=["Accounts"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.connect()
    yield 
    await Database.close()