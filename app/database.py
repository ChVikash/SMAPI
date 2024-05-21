from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

from sqlalchemy import create_engine

connection_string = settings.database_conn_str

# Create the engine
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try :
        yield db
    except Exception as e:
        print("Error yielding the database {e}")
        db.close()
        raise 

