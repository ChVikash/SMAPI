from fastapi import  HTTPException, status, Depends, APIRouter 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils, oauth2


router = APIRouter()


@router.get("/login", response_model=schemas.Token)
def user_login(user_info : OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_info.username).first()

    if not user : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify_pass(user_info.password, user.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    access_token = oauth2.create_access_token(data={"user_id" : user.id, "user_email": user.email})

    return {"access_token": access_token, "token_type" : "bearer"}