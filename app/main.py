from fastapi import Body, FastAPI, HTTPException, Response, status, Depends 
from . import models, schemas, utils
from .database import engine, get_db 
from sqlalchemy.orm import Session
from typing import List 



models.Base.metadata.create_all(bind = engine)

app = FastAPI()



@app.get("/")
async def root():
    return {"message" : "Method not allowed"}

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



##################################################################      CREATE       #################################################################################

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.PostResponse)
async def createposts(user_post: schemas.PostCreateUpdate, db:Session = Depends(get_db)):
    # insert_query = """
    #                 INSERT INTO posts.allposts (title, content, published) OUTPUT inserted.* VALUES (%s, %s, %s)
    #             """
    # insert_params = (user_post.title, user_post.content, user_post.published)
    # cursor.execute(insert_query, insert_params)
    # row_inserted = cursor.fetchone()
    # conn.commit() 
    # val = {**(user_post.model_dump())}
    # print(val)
    row_inserted = models.Post(**(user_post.model_dump()))
    db.add(row_inserted)
    db.commit()
    db.refresh(row_inserted)
    
    return row_inserted

###########################################################################READ##########################################################################################
@app.get("/posts", response_model= List[schemas.PostResponse])
async def posts(db : Session = Depends(get_db)):
    rows = db.query(models.Post).all()
    return rows

@app.get("/posts/{id}", response_model=schemas.PostResponse )
async def getpostbyid(id: int,db:Session = Depends(get_db)):
    # select_query = """
    #                 SELECT * FROM posts.allposts where id = %d
    #                 """
    # cursor.execute(select_query, (id))
    # postbyid = cursor.fetchone()

    postbyid = db.query(models.Post).filter(models.Post.id == id).first() #all keeps searching even after finding one and we know only one exists
    # print(postbyid)
    if not postbyid : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with Id: {id}, not found")
    return postbyid


########################################################################UPDATE###########################################################################################


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def updatepostbyid(id: int, post :schemas.PostCreateUpdate, db:Session = Depends(get_db)):
    # update_query = """UPDATE posts.allposts 
    #                     SET title = %s, 
    #                     content = %s, 
    #                     published = %s 
    #                 OUTPUT inserted.* 
    #                 WHERE id = %d"""  
    # update_params = (post.title, post.content, post.published, id)
    # cursor.execute(update_query, update_params)
    # row_updated = cursor.fetchone()
    # conn.commit()

    update_stmt = db.query(models.Post).filter(models.Post.id == id) 
    if not update_stmt.first() : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with Id: {id}, not found")
    row_updated = update_stmt.update( post.model_dump(), synchronize_session=False)
    db.commit()
    return row_updated

###########################################################################DELETE########################################################################################


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteposts(id:int, db: Session = Depends(get_db)):
#     delete_query = """
#                     DELETE FROM posts.allposts OUTPUT deleted.* where id = %d
#                     """
#     cursor.execute(delete_query, (id))
#     row = cursor.fetchone()
#     conn.commit()
    
    row = db.query(models.Post).filter(models.Post.id == id)
    if not row.first() : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with Id: {id}, not found")
    row.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#################################################################            USERS               ######################################################

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def createuser(user_cred: schemas.UserCreate, db:Session = Depends(get_db)):
    # insert_query = """
    #                 INSERT INTO posts.allposts (title, content, published) OUTPUT inserted.* VALUES (%s, %s, %s)
    #             """
    # insert_params = (user_post.title, user_post.content, user_post.published)
    # cursor.execute(insert_query, insert_params)
    # row_inserted = cursor.fetchone()
    # conn.commit() 
    # val = {**(user_post.model_dump())}
    # print(val)
    user_cred.password = utils.hash_pass(user_cred.password)
    user_details = models.User(**(user_cred.model_dump()))
    db.add(user_details)
    db.commit()
    db.refresh(user_details)
    
    return user_details

@app.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user_info = db.query(models.User).filter(models.User.id == id).first()
    if not user_info : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"USer with Id: {id}, not found")
    return user_info
