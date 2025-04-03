from .schemas import UserSchema, UserSchemaUpdate
from .models import User
from portal.base import  BaseApi

# CRUD operations for User
user_api = BaseApi(model=User, schema=UserSchema, update_schema=UserSchemaUpdate)
