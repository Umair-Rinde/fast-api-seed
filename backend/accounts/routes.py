from .apis import user_api
from portal.base import BaseRouter 

#CRUD Routes for User
router = BaseRouter(user_api).router 