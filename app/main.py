from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth, votes
from fastapi.middleware.cors import CORSMiddleware

## Not needed after alembic
##models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"] ##domains which can access/reach our API

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)

app.include_router(users.router)

app.include_router(auth.router)

app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "Method not allowed"}
