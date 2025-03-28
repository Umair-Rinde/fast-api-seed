from portal.base import BaseSchema
from pydantic import Field

class AccountSchema(BaseSchema):
    name: str = Field(..., title="Account Name", max_length=100)
    email: str = Field(..., title="Email Address", regex=r'^\S+@\S+\.\S+$')