from pydantic import BaseModel
from typing import Optional
from typing import Dict, Any
from fastapi.responses import JSONResponse
from typing import Generic, TypeVar, Optional
from core.database import Database
from bson import ObjectId
from typing import Any, Dict, List, Optional


class BaseSchema(BaseModel):
    id: Optional[str] = None  
    
    class Config:
        from_attributes = True  



class BaseModel:
    collection_name = ""  

    @classmethod
    def get_collection(cls):
        if not cls.collection_name:
            raise ValueError(f"{cls.__name__} must set 'collection_name'")
        return Database.get_db()[cls.collection_name]

    @classmethod
    async def create(cls, data: Dict[str, Any]) -> str:
        result = await cls.get_collection().insert_one(data)
        return str(result.inserted_id)

    @classmethod
    async def get_all(cls, limit: int = 100) -> List[Dict[str, Any]]:
        documents = await cls.get_collection().find().to_list(limit)
        for doc in documents:
            doc["_id"] = str(doc["_id"])  
        return documents

    @classmethod
    async def get_by_id(cls, object_id: str) -> Optional[Dict[str, Any]]:
        document = await cls.get_collection().find_one({"_id": ObjectId(object_id)})
        if document:
            document["_id"] = str(document["_id"])
        return document

    @classmethod
    async def update(cls, object_id: str, data: Dict[str, Any]) -> bool:
        result = await cls.get_collection().update_one(
            {"_id": ObjectId(object_id)}, {"$set": data}
        )
        return result.modified_count > 0

    @classmethod
    async def delete(cls, object_id: str) -> bool:
        result = await cls.get_collection().delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count > 0



T = TypeVar("T")

class BaseResponse(JSONResponse, Generic[T]):
    def __init__(self, success: bool = True, message: str = '', data: Optional[T] = None, status_code: int = 200, error=None):
        if error:
            success = False
        content = {"success": success, "message": message, "data": data, "error": error}
        super().__init__(content=content, status_code=status_code)
