from fastapi import HTTPException, Response, status, Depends, APIRouter
from .. import models, schemas,  oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


# @router.post("/createposts")
# async def createposts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"message" : f"user name is {payLoad['User']}  message : post created successfully"}

# @router.get("/posts/getpostbyid" )
# async def getpostbyid(id: Id):
#     select_query = """
#                     SELECT * FROM posts.allposts where id = %d
#                     """
#     cursor.execute(select_query, (id.id))
#     row = cursor.fetchone()
#     return row


##################################################################      CREATE       #################################################################################

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def createposts(user_post: schemas.PostCreateUpdate, db: Session = Depends(get_db),  current_user: models.User = Depends(oauth2.get_current_user)):
    # insert_query = """
    #                 INSERT INTO posts.allposts (title, content, published) OUTPUT inserted.* VALUES (%s, %s, %s)
    #             """
    # insert_params = (user_post.title, user_post.content, user_post.published)
    # cursor.execute(insert_query, insert_params)
    # row_inserted = cursor.fetchone()
    # conn.commit()
    # val = {**(user_post.model_dump())}
    # print(val)
    # print(user_post)
    # print(current_user)
    row_inserted = models.Post(
        user_id=current_user.id, **(user_post.model_dump()))
    # print(row_inserted)
    # db.add(row_inserted)
    db.commit()
    db.refresh(row_inserted)

    return row_inserted

#############################################################              READ              ########################################################################


@router.get("/", response_model=List[schemas.PostItemResponse])
async def posts(db: Session = Depends(get_db), user=Depends(oauth2.get_current_user), limit: int = 15, skip: int = 0, search: Optional[str] = ""):
    
    postandvotes = db.query(models.Post, 
                            func.count(models.Vote.post_id).label("votes")
                            ).join(
        models.Vote, 
        models.Post.id==models.Vote.post_id, 
        isouter=True
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.title.contains(
            search)
            ).limit(limit=limit).offset(skip).all()
    return postandvotes


@router.get("/{id}", response_model=schemas.PostItemResponse)
async def getpostbyid(id: int, db: Session = Depends(get_db), 
                      current_user: models.User = Depends(oauth2.get_current_user)):
    # select_query = """
    #                 SELECT * FROM posts.allposts where id = %d
    #                 """
    # cursor.execute(select_query, (id))
    # postbyid = cursor.fetchone()

    # all keeps searching even after finding one and we know only one exists

    postandvote = db.query(models.Post, 
                            func.count(models.Vote.post_id).label("votes")
                            ).filter(models.Post.id == id).join(
        models.Vote, 
        models.Post.id==models.Vote.post_id, 
        isouter=True
    ).group_by(
        models.Post.id
    ).first()
    if not postandvote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with Id: {id}, not found")
    return postandvote


######################################################################## UPDATE###########################################################################################


@router.put("/{id}", response_model=schemas.PostResponse)
def updatepostbyid(id: int, post: schemas.PostCreateUpdate, db: Session = Depends(get_db),  current_user: models.User = Depends(oauth2.get_current_user)):
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
    updated_post = update_stmt.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with Id: {id}, not found")
    # post_dict = post.model_dump()
    # post_dict["id"] = id
    # post_dict["created_at"] = datetime.now(UTC)
    # print(post_dict)

    if updated_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Action can't be performed")
    row_updated = update_stmt.update(
        post.model_dump(), synchronize_session=False)
    print(row_updated)
    db.commit()

    print("reached")
    return update_stmt.first()

########################################################################### DELETE########################################################################################


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteposts(id: int, db: Session = Depends(get_db),  current_user: models.User = Depends(oauth2.get_current_user)):
    #     delete_query = """
    #                     DELETE FROM posts.allposts OUTPUT deleted.* where id = %d
    #                     """
    #     cursor.execute(delete_query, (id))
    #     row = cursor.fetchone()
    #     conn.commit()

    row = db.query(models.Post).filter(models.Post.id == id)
    row_result = row.first()
    if not row_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with Id: {id}, not found")

    if row_result.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Action can't be performed")
    row.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
