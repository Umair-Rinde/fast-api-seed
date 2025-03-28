from fastapi import APIRouter
from .schemas import AccountSchema
from .apis import create_account, get_all_accounts

router = APIRouter()

@router.post("/")
async def post_account(account: AccountSchema):
    return await create_account(account)

@router.get("/")
async def get_accounts():
    return await get_all_accounts()
