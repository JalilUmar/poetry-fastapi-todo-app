from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DB_URL")
# engine = create_engine(POSTGRES_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


from sqlmodel import SQLModel, Field, create_engine

# Setting timeout of database
engine = create_engine(
    POSTGRES_DATABASE_URL,
    echo=True,
    # connect_args={
    #     "check_same_thread": False,
    # },
    pool_recycle=300,
)

SQLModel.metadata.create_all(engine)
