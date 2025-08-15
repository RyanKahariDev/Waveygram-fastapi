from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint


class WhoCreatedPost(BaseModel):
    email: str

    class Config:
        orm_mode = True


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

    # rating: Optional[int] = None


class PostReturn(BaseModel):
    title: str
    content: str
    # published: bool
    created_at: datetime
    # owner_id: int
    created_by: WhoCreatedPost

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostReturn
    votes: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserReturn(BaseModel):
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)  # type: ignore
