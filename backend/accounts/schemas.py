from portal.base import BaseSchema
from pydantic import Field

class AccountSchema(BaseSchema):
    name: str = Field(..., title="Account Name")
    email: str = Field(..., title="Account Email")
