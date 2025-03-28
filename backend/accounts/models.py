from core.database import db
from portal.base import BaseModel


class Account(BaseModel):
    collection = db.accounts

