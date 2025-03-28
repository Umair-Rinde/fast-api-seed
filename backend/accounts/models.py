from core.database import Database
from portal.base import BaseModel


class Account(BaseModel):
    collection_name = Database.get_db()["accounts"]

