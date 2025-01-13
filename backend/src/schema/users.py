from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Literal
from datetime import datetime


class UserBase(BaseModel):
    fullname: str = Field(..., min_length=2, max_length= 60)
    email: EmailStr
    user_type: Literal["Student", "Teacher", "Parent", "Admin"]


class Enroll(UserBase):
    pass


class UnapprovedUsers(UserBase):
    approved: bool = False


class UserInDB(UserBase):
    password: str
    approved: bool = False
    is_first_login: bool = True
    picture_url: Optional[str]
    address: Optional[str]
    dob: Optional[str]
    phone_number: Optional[str]


### Response models
class GetUsers(UserBase):
    #id: str
    approved: bool 

class EnrollResponse(BaseModel):
    user_id: str
    message: str


class forgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    new_password: str
    token: str