from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker
from main import app
from dependencies import get_db
from todo.models import TodoModel
from uuid import uuid4

import pytest
import os

TEST_DB_URL = os.getenv("TEST_POSTGRES_DB_URL")

engine = create_engine(TEST_DB_URL, pool_recycle=300)


def override_get_db():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


# Fixture to create a test client
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


# Fixture to set up and tear down the test database
@pytest.fixture
def test_db():
    SQLModel.metadata.create_all(bind=engine)
    yield
    # SQLModel.metadata.drop_all(bind=engine)


headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzdUstcmNrbTBQcGNuMmVVUHJLbkQiLCJleHAiOjE3MTEwMTUzMzB9.-axRxjXMvF9zktfPliGLGoqCEjgSYsEJzWJsy0nsaeM"
}


# Create a new todo item
def test_create_todo_item(client, test_db):
    # Create a new todo item
    response = client.post(
        "/api/todo/create",
        json={"title": "Test Todo", "description": "Test Description"},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True
    assert data["message"] == "Todo item added successfully"
    assert data["response"]["title"] == "Test Todo"


# get all todo items
def test_get_all_todo(client, test_db):
    # Assuming a todo item has been added from the create test
    response = client.get("/api/todo/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert len(data["response"]) >= 1  # There should be at least one todo


# get one todo item
def test_get_one_todo(client, test_db):
    new_todo = client.post(
        "/api/todo/create",
        json={
            "title": "Test Todo for getting one",
            "description": "Test Description for getting one todo at one time",
        },
        headers=headers,
    )

    todo_id = new_todo.json()["response"]["todoId"]

    # now getting this newly created todo item by its id. This should return the todo item with the given id.
    response = client.get(f"/api/todo/{todo_id}", headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["response"]["todoId"] == todo_id


# update todo item
def test_update_todo(client, test_db):
    new_todo = client.post(
        "/api/todo/create",
        json={
            "title": "Test Todo for update",
            "description": "Test Description for update",
        },
        headers=headers,
    )

    todo_id = new_todo.json()["response"]["todoId"]

    # now updating this newly created todo item with new title and isCompleted set to True
    response = client.put(
        f"/api/todo/{todo_id}",
        json={"title": "Updated Title", "isCompleted": True},
        headers=headers,
    )
    assert response.status_code == 202
    data = response.json()
    assert data["success"] == True
    assert data["message"] == "Todo item updated successfully"
    assert data["response"]["title"] == "Updated Title"


def test_delete_todo(client, test_db):
    # Assuming a todo item has been added and its id is 'todo_id'
    new_todo = client.post(
        "/api/todo/create",
        json={
            "title": "Test Todo for delete",
            "description": "Test Description for delete",
        },
        headers=headers,
    )
    todo_id = new_todo.json()["response"]["todoId"]

    # now deleting this newly created todo item
    response = client.delete(f"/api/todo/{todo_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["message"] == "Todo item deleted successfully"
