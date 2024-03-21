from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from uuid import UUID
from sqlmodel import SQLModel, Field


# class TodoModel(Base):
#     __tablename__ = "todo"

#     todoId = Column(String, primary_key=True)
#     userId = Column(String, ForeignKey("users.id"))
#     title = Column(String)
#     description = Column(String)
#     isCompleted = Column(Boolean)


class TodoModel(SQLModel, table=True):
    __tablename__ = "todo"

    todoId: str = Field(primary_key=True)
    userId: str = Field(foreign_key="users.id")
    title: str
    description: str
    isCompleted: bool
