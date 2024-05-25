from fastapi import HTTPException, Response, status, Depends, APIRouter
from .. import models, schemas,  oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):

    row = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if not row.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post doesn't exist")
    voted_already = db.query(models.Vote).filter(
        models.Vote.user_id == user.id, models.Vote.post_id == vote.post_id)

    already_present = voted_already.first()

    if vote.bool >= 1:
        if already_present:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User has already voted for the post")
        else:
            row = models.Vote(user_id=user.id, post_id=vote.post_id)
            db.add(row)
            db.commit()
            db.refresh(row)
            return {"message": "Voted Successfully"}
    else:
        if already_present:
            voted_already.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User has not voted on the post")
