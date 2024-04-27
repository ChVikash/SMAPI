from fastapi import  HTTPException, Response, status, Depends, APIRouter 
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils, oauth2


router = APIRouter()


@router.get("/login")
def user_login(user_info : schemas.UserCreate, db:Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_info.email).first()

    if not user : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    if not utils.verify_pass(user_info.password, user.password):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    access_token = oauth2.create_access_token(data={"user_id" : user.id, "user_email": user.email})

    return {"access_token": access_token, "token_type" : "bearer"}