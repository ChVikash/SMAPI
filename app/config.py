from  pydantic_settings import BaseSettings


class Settings(BaseSettings): 
    database_conn_str : str
    jwt_algo : str 
    JWT_KEY : str
    JWT_TOKEN_EXPIRE_MINUTES : int
    class Config: 
        env_file = ".env"

settings = Settings()