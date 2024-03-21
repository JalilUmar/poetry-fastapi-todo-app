# from database import Base
from sqlalchemy import Column, String
from uuid import UUID

from sqlmodel import SQLModel, Field


# class UserModel(Base):
#     __tablename__ = "users"

#     id = Column(String, primary_key=True, default=UUID)
#     username = Column(String, unique=True, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     password = Column(String)


class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True)
    username: str = Field(unique=True, nullable=False)
    email: str
    password: str
