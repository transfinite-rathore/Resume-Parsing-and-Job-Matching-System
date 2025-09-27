from pydantic import BaseModel,Field,EmailStr,field_validator
from ..utils.password_setups import hash_password
from typing import Optional



class Recruiter(BaseModel):
    company_name:str
    established_in:str=Field(max_length=4,min_length=4)
    employee_count:int=Field(ge=0)
    password:str=Field(...)
    email:EmailStr=Field(...)
    
    @field_validator("password",mode="before")
    @classmethod
    def hash_password(cls,pas:str) -> str:
        if not pas.startswith("$2b$"):
            return hash_password(pas)
        return pas

class RecuriterLogin(BaseModel):
    email:EmailStr=Field(...)
    password:str=Field(...)

class change_recuriter_password(BaseModel):
    current_password:str
    new_password:str