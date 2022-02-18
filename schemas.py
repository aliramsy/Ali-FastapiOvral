from pydantic import BaseModel, conint
from datetime import datetime
from typing import Optional

from pydantic.networks import EmailStr


class User(BaseModel):
    username:str
    password:str
    email:EmailStr

class Ruser(BaseModel):

    username:str
    email:EmailStr
    created_at:datetime
    
    class Config:
        orm_mode = True



class Post(BaseModel):
    
    title:str
    content:str
    
class Rpost(Post):
    
    created_at:datetime
    owner_id:int
    owner:Ruser
    
    class Config:
        orm_mode = True


class Ropost(BaseModel):
    Post:Rpost
    likes:int

    class Config:
        orm_mode = True



class Login(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Like(BaseModel):
    post_id:int
    dir:conint(le=1)
