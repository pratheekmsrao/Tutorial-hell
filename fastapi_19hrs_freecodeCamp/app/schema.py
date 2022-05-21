from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
