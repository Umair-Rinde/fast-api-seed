from portal.base import BaseSchema
from pydantic import Field
from typing import Optional

class UserSchema(BaseSchema):
    name: str = Field(..., title="User Name", max_length=100)
    email: str = Field(..., title="Email Address", pattern=r'^\S+@\S+\.\S+$')


class UserSchemaUpdate(BaseSchema):
    name: Optional[str] = Field(None, title="User Name", max_length=100)
    email: Optional[str] = Field(None, title="Email Address", pattern=r'^\S+@\S+\.\S+$')

    model_config = {"extra" :"allow"}  