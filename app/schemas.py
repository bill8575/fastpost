from pydantic import BaseModel, EmailStr, conint, Field
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True
class PostCreate(PostBase):
    pass

# class UpdatePost(BaseModel):
#     # title: str
#     # content: str
#     published: bool

# class PostUpdate(PostBase):

# Response 
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
      orm_model = True

# class Post(BaseModel):
#     id: int
#     title: str
#     content: str
#     published: bool
#     created_at: datetime    

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
      orm_model = True
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]