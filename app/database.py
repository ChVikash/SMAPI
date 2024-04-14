from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, select, inspect
from sqlalchemy import create_engine, Table, MetaData, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


# cnx = psycopg2.connect(user="sqladminuser", password="Chvik1998post", host="api-sqlserver.postgres.database.azure.com", port=5432, database="fastapi")

from sqlalchemy import create_engine, MetaData, Table

connection_string = 'postgresql://'

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


# # You can test the connection by executing a simple query
# with engine.connect() as conn:
#     result = conn.execute("SELECT 'Hello, PostgreSQL!'")
#     print(result.fetchone()[0])

