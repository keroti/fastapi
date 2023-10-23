from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional
import datetime

class PostBase(BaseModel):
	title: str
	content: str
	published: bool = True

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime
    class Config:
        orm_mode = True
        
class CreatePost(PostBase):
	pass

class Post(PostBase):
    created_at: datetime.datetime
    id: int
    user_id: int
    owner: UserOut
    class Config:
        orm_mode = True

class PostOut(PostBase):
    Post: Post
    No_of_votes: int

class CreateUser(BaseModel):
    email: EmailStr
    password: str
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    class Config:
        orm_mode = True