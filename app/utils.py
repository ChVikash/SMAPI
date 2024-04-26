from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(pwd:str):
    hashed_pass = pwd_context.hash(pwd)
    return hashed_pass