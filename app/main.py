from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status 
from pydantic import BaseModel
import pymssql
import time 

app = FastAPI()

class Post(BaseModel): 
    title : str
    content : str
    published : bool = True

class Id(BaseModel): 
    id : int


attempts = 10
while attempts > 0 : 
    try:
        attempts -=1
        conn = pymssql.connect(server, username, password, database)
        cursor = conn.cursor(as_dict=True)
        break
    except Exception as e:
        print(f'Error connecting to SQL Server: {e}')


@app.get("/")
async def root():
    return {"message" : "HW"}

@app.get("/posts")
async def posts():
    query = 'SELECT * FROM posts.allposts'
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

# @app.post("/createposts")
# async def createposts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"message" : f"user name is {payLoad['User']}  message : post created successfully"}


# @app.get("/posts/getpostbyid" )
# async def getpostbyid(id: Id):
#     select_query = """
#                     SELECT * FROM posts.allposts where id = %d
#                     """
#     cursor.execute(select_query, (id.id))
#     row = cursor.fetchone()
#     return row

@app.get("/posts/{id}" )
async def getpostbyid(id: int):
    select_query = """
                    SELECT * FROM posts.allposts where id = %d
                    """
    cursor.execute(select_query, (id))
    row = cursor.fetchone()
    if not row : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with Id: {id}, not found")
    return row

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteposts(id:int):
    delete_query = """
                    DELETE FROM posts.allposts OUTPUT deleted.* where id = %d
                    """
    cursor.execute(delete_query, (id))
    row = cursor.fetchone()
    if not row : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with Id: {id}, not found")
    conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def updatepostbyid(id: int, post :Post):
    update_query = """UPDATE posts.allposts 
                        SET title = %s, 
                        content = %s, 
                        published = %s 
                    OUTPUT inserted.* 
                    WHERE id = %d"""
    
    update_params = (post.title, post.content, post.published, id)

    cursor.execute(update_query, update_params)

    row_updated = cursor.fetchone()
    if not row_updated : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with Id: {id}, not found")
    conn.commit()
    return row_updated

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def createposts(user_post: Post):
    insert_query = """
                    INSERT INTO posts.allposts (title, content, published) OUTPUT inserted.* VALUES (%s, %s, %s)
                """
    insert_params = (user_post.title, user_post.content, user_post.published)
    cursor.execute(insert_query, insert_params)
    row_inserted = cursor.fetchone()
    conn.commit() 
    return row_inserted