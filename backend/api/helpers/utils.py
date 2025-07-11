from bson import ObjectId
from fastapi import HTTPException, status

def convert_str_to_object_id(id: str) -> ObjectId:
    try:
        obj_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    return obj_id