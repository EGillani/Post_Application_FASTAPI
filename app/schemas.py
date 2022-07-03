from datetime import datetime
from pydantic import BaseModel, EmailStr
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
    user_id: int
    owner: UserOut #this is defined in the orm models 
    #id : int <--dont want to show id 
    #created_at: datetime
    #the properties are already inherited from the base class 
    class Config: 
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
