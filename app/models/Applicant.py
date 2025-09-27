from pydantic import BaseModel,Field,computed_field,EmailStr,field_validator
from typing import Optional
from passlib.context import CryptContext
from ..utils.password_setups import hash_password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ApplicantRegister(BaseModel):
    first_name: str=Field(...,min_length=2,max_length=50,)
    last_name: str=Field(...,min_length=2,max_length=50)
    age: int= Field(...,gt=18)
    username: str=Field(...,min_length=5,max_length=15)
    experience_in_years: float=Field(...,lt=50)
    email: EmailStr
    desired_role:str
    phone: str=Field(...,max_length=14,min_length=10)
    graduation_year: str=Field(...)
    github_link: Optional[str]
    linkdin_link: Optional[str]
    current_package_lpa: int
    expected_package_lpa: int
    password: str=Field(...,min_length=8)

    @field_validator("password", mode="before")
    @classmethod
    def hash_password_validator(cls, v: str) -> str:
        # Only hash if it’s not already hashed (to avoid double hashing)
        if not v.startswith("$2b$"):  # bcrypt hashes always start like this
            return hash_password(v)
        return v

    
class ApplicantLogin(BaseModel):
    username: Optional[str]=Field(None,min_length=5,max_length=150)
    email: Optional[EmailStr]
    password: str=Field(...,min_length=8)


class change_applicant_password(BaseModel):
    current_password: str=Field(...,min_length=8)
    new_password: str=Field(...,min_length=8)


#RESUME,ADDRESS
class ApplicantUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    age: Optional[int] = Field(None, gt=18)
    username: Optional[str] = Field(None, min_length=5, max_length=15)
    experience_in_years: Optional[float] = Field(None, lt=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=10)
    graduation_year: Optional[str] = None
    github_link: Optional[str] = None
    linkdin_link: Optional[str] = None
    current_package_lpa: Optional[int] = None
    expected_package_lpa: Optional[int] = None
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, max_length=15)

    

    @computed_field
    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
