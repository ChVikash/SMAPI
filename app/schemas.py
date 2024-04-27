from pydantic import BaseModel, EmailStr 
from datetime import datetime 
from typing import List

class PostBase(BaseModel): 
    title : str
    content : str
    published : bool = True
    

class PostCreateUpdate(PostBase): 
    pass


class PostResponse(PostBase): 
    id : int 
    created_at : datetime
    class Config :
        from_attributes = True
        populate_by_name = True


class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int 
    email : EmailStr 
    created_at : datetime
    class Config :
        from_attributes = True
        populate_by_name = True

class UserAuth(UserCreate):
    pass