
#Function to format MongoDB documents
from typing import List, Dict, Any
from bson import ObjectId

async def format_docs(cursor) -> List[Dict[str, Any]]:
    print("Formatting documents...")
    docs = []
    async for doc in cursor:
        if "_id" in doc and isinstance(doc["_id"], ObjectId):
            doc["id"] = str(doc["_id"]) 
            del doc["_id"]
        docs.append(doc)
    return docs
