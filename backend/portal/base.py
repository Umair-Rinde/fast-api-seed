from pydantic import Field
from pydantic import BaseModel as PydanticBaseModel
from fastapi.responses import Response
from typing import Generic, TypeVar, Optional,Type
from datetime import datetime
from utils.helpers import format_docs
from fastapi.encoders import jsonable_encoder
from core.database import Database
import uuid
import json
from fastapi import APIRouter

class BaseSchema(PydanticBaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))  

    class Config:
        from_attributes = True  




class BaseModel:
    collection = ''

    def __init__(self, **data):
        self.created_on = datetime.now()
        self.updated_on = datetime.now()
        for key, value in data.items():
            setattr(self, key, value)

    def dict(self):
        return jsonable_encoder(self.__dict__)

    @classmethod
    def get_collection(self):
        return Database.get_db()[self.collection]

    @classmethod
    async def get_all(cls):
        cursor = cls.get_collection().find({})
        return await format_docs(cursor)
    
    @classmethod
    async def create(cls, data):
        obj = cls(**data)
        result = await cls.get_collection().insert_one(obj.dict())
        return str(result.inserted_id)

    @classmethod
    async def update(cls, obj_id, data):
        if not data:
            return 0  

        data["updated_on"] = datetime.now()  
        result = await cls.get_collection().update_one(
            {"id": obj_id}, {"$set": data}  
        )
        return result.modified_count  

    @classmethod
    async def get(cls, obj_id):
        doc = await cls.get_collection().find_one({"id": str(obj_id)})
        print(doc)
        if doc:
            doc.pop("_id", None) 
            return doc
        return None
        
    @classmethod
    async def delete(cls, obj_id):
        return await cls.get_collection().delete_one({"id": obj_id})



T = TypeVar("T")

class BaseResponse(Response, Generic[T]):
    def __init__(self, success: bool = True, message: str = '', data: Optional[T] = None, status_code: int = 200, error=None):
        if error:
            success = False
        content = {"success": success, "message": message, "data": data, "error": error}
        json_content = json.dumps(content, default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o))
        super().__init__(content=json_content, status_code=status_code)



class BaseApi():
    def __init__(self, model, schema: Type[PydanticBaseModel], update_schema: Optional[Type[PydanticBaseModel]] = None):
        self.model = model
        self.collection = None
        self.schema = schema
        self.update_schema = update_schema if update_schema else schema  # Use normal schema if partial one isn't provided

    async def create(self, data: dict):
        validated_data = self.schema(**data)  # Validate input
        obj_id = await self.model.create(validated_data.model_dump())
        return BaseResponse(message=f"{self.model.__name__} created successfully", data={"id": obj_id}, status_code=201)

    async def get_all(self):
        objects = await self.model.get_all()
        return BaseResponse(message=f"{self.model.__name__}s fetched successfully", data=objects, status_code=200)

    async def get_one(self, id: str):
        obj = await self.model.get(id)
        if not obj:
            return BaseResponse(success=False, message=f"{self.model.__name__} not found", status_code=404)
        return BaseResponse(message=f"{self.model.__name__} fetched successfully", data=obj, status_code=200)

    async def update(self, id: str, update_data: dict):
        validated_data = self.update_schema(**update_data)  # Use partial update schema
        update_dict = validated_data.model_dump(exclude_unset=True)

        if not update_dict:
            return BaseResponse(success=False, message="No fields to update", status_code=400)

        updated_count = await self.model.update(id, update_dict)
        if updated_count == 0:
            return BaseResponse(success=False, message=f"{self.model.__name__} not found", status_code=404)

        return BaseResponse(message=f"{self.model.__name__} updated successfully", status_code=200)

    async def delete(self, id: str):
        deleted_count = await self.model.delete(id)
        if deleted_count == 0:
            return BaseResponse(success=False, message=f"{self.model.__name__} not found", status_code=404)
        return BaseResponse(message=f"{self.model.__name__} deleted successfully", status_code=200)


class BaseRouter:
    def __init__(self, api: BaseApi):
        self.router = APIRouter( tags=[api.model.__name__])
        self.api = api
        self._add_routes()

    def _add_routes(self):
        self.router.post("/")(self.api.create)
        self.router.get("/")(self.api.get_all)
        self.router.get("/{id}")(self.api.get_one)
        self.router.put("/{id}")(self.api.update)
        self.router.delete("/{id}")(self.api.delete)