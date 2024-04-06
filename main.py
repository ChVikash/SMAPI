from typing import Optional
from fastapi import Body, FastAPI 
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel): 
    title : str
    content : str
    posted : bool = True
    rating : Optional[int]= None

@app.get("/")
async def root():
    return {"message" : "HW"}

@app.get("/posts")
async def posts():
    return {"message" : "these are your posts"}

# @app.post("/createposts")
# async def createposts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"message" : f"user name is {payLoad['User']}  message : post created successfully"}

@app.post("/createposts")
async def createposts(user_post: Post):
    print(user_post.model_dump())
    return {"message" : f"post title is {user_post.title}, with content {user_post.content} and it status posted {user_post.posted} rating is {user_post.rating}"}