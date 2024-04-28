from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from . import schemas, database,models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer('login')

SECRET_KEY = "HELLO Learning the JWT key"
JWT_ALGO = "HS256"
ACCESS_TOKEN_AUTO_EXPIRE_MINUTES = 3000

def create_access_token(data:dict):
    data_copy = data.copy()
    expiration_time = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_AUTO_EXPIRE_MINUTES)
    data_copy.update({"exp":expiration_time})
    jwt_encoded_token = jwt.encode( data_copy, key=SECRET_KEY, algorithm=JWT_ALGO)
    return jwt_encoded_token


def verify_access_token(token: str, cred_exception): 

    try:    
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[JWT_ALGO])
        user_id : int = payload.get("user_id")
        user_email : str = payload.get("email")

        if user_id is None: 
            raise cred_exception
      
        #validating it with schema
        token_data = schemas.TokenData(id=user_id, email=user_email)
    except JWTError:
        raise cred_exception
    return token_data
    
def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                   detail=f"Invalid Credentials", 
                                   headers={"WWW-Authenticate" : "Bearer"})
    token_data = verify_access_token(token, cred_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    print(type(user))
    return user




