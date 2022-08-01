from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config: 
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

#USER -> SERVER 
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

#using inheritance 
class PostCreate(PostBase):
    pass #accept everything PostBase has 

#SERVER -> USER (removing the id and data field )
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id : int
    owner: UserOut #this is defined in the orm models 
    #the properties are already inherited from the base class 
    class Config: 
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir:conint(ge=0, le=1)