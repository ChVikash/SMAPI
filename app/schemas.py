from pydantic import BaseModel, EmailStr 
from datetime import datetime 
from typing import Optional

class UserOut(BaseModel):
    id : int 
    email : EmailStr 
    created_at : datetime
    class Config :
        from_attributes = True
        populate_by_name = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str



class UserAuth(UserCreate):
    pass

class PostBase(BaseModel): 
    title : str
    content : str
    published : bool = True
    owner : UserOut
    

class PostCreateUpdate(PostBase): 
    pass


class PostResponse(PostBase): 
    id : int 
    created_at : datetime
    user_id : int
    class Config :
        from_attributes = True
        populate_by_name = True




class Token(BaseModel):
    access_token  : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None
    email : Optional[str] = None