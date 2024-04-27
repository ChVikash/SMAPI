from jose import JWTError, jwt
from datetime import datetime, timedelta


SECRET_KEY = "HELLO Learning the JWT key"
JWT_ALGO = "HS256"
ACCESS_TOKEN_AUTO_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    data_copy = data.copy()
    expiration_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_AUTO_EXPIRE_MINUTES)
    data_copy.update({"exp":expiration_time})
    jwt_encoded_token = jwt.encode( data_copy, key=SECRET_KEY, algorithm=JWT_ALGO)
    return jwt_encoded_token
