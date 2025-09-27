from pydantic import BaseModel,Field
from typing import Optional,List

class JobDescription(BaseModel):
    role:str=Field(max_length=20)
    recruiter_id:str
    required_experience:float=Field(ge=0)
    package_offered:Optional[float]
    description:str=Field(max_length=500)
