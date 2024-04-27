# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_pass(pwd:str):
#     hashed_pass = pwd_context.hash(pwd)
#     return hashed_pass

# def verify_pass(pwd_received:str, pwd_in_db: str):
#     return pwd_context.verify(pwd_received, pwd_in_db)

# since passlib is no longer maintained, using bcrypt directly  

import bcrypt
def hash_pass(pwd:str): 
    pwd_to_bytes = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_to_bytes, salt=salt)
    string_pass = hashed_password.decode('utf-8')
    return string_pass

def verify_pass(pwd_received:str, pwd_in_db: str): 
    pwd_received_to_bytes = pwd_received.encode('utf-8')
    pwd_in_db_to_bytes = pwd_in_db.encode('utf-8')
    return bcrypt.checkpw(password=pwd_received_to_bytes, hashed_password= pwd_in_db_to_bytes)
    