from uuid import uuid4
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    id: str = str(uuid4())
    full_name: str
    username: str
    email: EmailStr
    password: str
    birth_date: str
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    pss_token: str
