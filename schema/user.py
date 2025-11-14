from typing import Optional, List 
from pydantic import BaseModel,Field , EmailStr


class UserInput(BaseModel):
    username: str = Field(...,min_length=3,max_length=50)
    email: EmailStr
    password : str = Field(...,min_length=6)


class UserResponse(BaseModel):
    id : str
    username: str
    email : str


class Login(BaseModel):
    email : EmailStr
    password : str = Field(...,max_length=6)


class LoginResponse(BaseModel):
    id:str
    username: str
    email : str
    message: str   
