from .schemas import AccountSchema
from .models import Account

async def create_account(account: AccountSchema):
    account_dict = account.model_dump() 
    account_id = await Account.create_account(account_dict)
    return {"id": account_id}

async def get_all_accounts():
    return await Account.get_accounts()
