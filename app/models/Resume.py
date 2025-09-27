from pydantic import BaseModel,Field
from typing import Optional
from bson import ObjectId
class Resume(BaseModel):

    applicant_id:ObjectId
    url:str=Field(...)
    cloudinary_public_id:str=Field(...)
    is_active:bool

    class Config:
        arbitrary_types_allowed = True