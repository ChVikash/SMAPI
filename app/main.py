from fastapi import Body, FastAPI, HTTPException, Response, status, Depends 
from . import models, schemas, utils
from .database import engine, get_db 
from sqlalchemy.orm import Session
from typing import List 
from .routers import posts, users


models.Base.metadata.create_all(bind = engine)

app = FastAPI()


app.include_router(posts.router)

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message" : "Method not allowed"}