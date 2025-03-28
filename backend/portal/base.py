from pydantic import BaseModel
from typing import Optional
from core.database import db
from typing import Dict, Any
from fastapi.responses import JSONResponse
from typing import Generic, TypeVar, Optional


class BaseSchema(BaseModel):
    id: Optional[str] = None  
    
    class Config:
        from_attributes = True  


class BaseModel:
    collection_name = ""

    @classmethod
    def get_collection(cls):
        return db[cls.collection_name]

    @classmethod
    async def create(cls, data: Dict[str, Any]) -> str:
        result = await cls.get_collection().insert_one(data)
        return str(result.inserted_id)

    @classmethod
    async def get_all(cls, limit: int = 100):
        documents = await cls.get_collection().find().to_list(limit)
        for doc in documents:
            doc["_id"] = str(doc["_id"]) 
        return documents




T = TypeVar("T")

class BaseResponse(JSONResponse, Generic[T]):
    def __init__(self, success: bool = True, message: str = '', data: Optional[T] = None, status_code: int = 200, error=None):
        if error:
            success = False
        content = {"success": success, "message": message, "data": data, "error": error}
        super().__init__(content=content, status_code=status_code)
