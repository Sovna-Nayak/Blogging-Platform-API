from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):  # For signup
    username: str
    email: str
    password: str

class UserLogin(BaseModel):   # For login
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True   # ✅ FIXED

    # class Config:
    #     orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str




# class UserCreate(BaseModel):       # For signup
#     username: str
#     email: EmailStr
#     password: str

# class UserLogin(BaseModel):        # For login
#     username: str
#     password: str

# class UserOut(BaseModel):
#     id: int
#     username: str
#     email: EmailStr

#     class Config:
#         orm_mode = True

# class Token(BaseModel):
#     access_token: str
#     token_type: str


