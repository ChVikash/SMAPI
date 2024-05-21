from fastapi import  HTTPException, status, Depends, APIRouter 
from .. import models, schemas, utils, oauth2
from ..database import get_db 
from sqlalchemy.orm import Session 

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def createuser(user_cred: schemas.UserCreate, db:Session = Depends(get_db)):
    user_cred.password = utils.hash_pass(user_cred.password)
    user_details = models.User(**(user_cred.model_dump()))
    db.add(user_details)
    db.commit()
    db.refresh(user_details)
    
    return user_details

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db),  current_user: models.User = Depends(oauth2.get_current_user)):
    user_info = db.query(models.User).filter(models.User.id == id).first()
    if not user_info : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"USer with Id: {id}, not found")
    return user_info
