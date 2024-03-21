from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from fastapi import FastAPI, Depends, HTTPException, status

from main import app
from user.models import UserModel
from dependencies import get_db

import pytest
import os

# Create a SQLModel test engine with SQLite in-memory database
TEST_DATABASE_URL = os.getenv("TEST_POSTGRES_DB_URL")

engine = create_engine(TEST_DATABASE_URL, pool_recycle=300)


# Dependency override for the database session
def override_get_db():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


# Test client fixture
@pytest.fixture(name="client")
def fixture_client():
    with TestClient(app) as c:
        yield c


# Fixture to create and drop the database tables
@pytest.fixture(name="create_test_database")
def fixture_create_test_database():
    SQLModel.metadata.create_all(engine)
    yield
    # SQLModel.metadata.drop_all(engine)


# Test register_user endpoint
def test_register_user(client, create_test_database):
    response = client.post(
        "/api/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    json_res = response.json()
    assert json_res["success"] == True
    assert json_res["message"] == "User registered successfully"


# Test login_user endpoint
def test_login_user(client, create_test_database):
    # First, register a user
    client.post(
        "/api/users/register",
        json={
            "username": "testloginuser",
            "email": "testlogin@example.com",
            "password": "testpassword",
        },
    )
    # Then, attempt to log in
    response = client.post(
        "/api/users/login",
        data={
            "username": "testloginuser",
            "password": "testpassword",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    json_res = response.json()
    # assert json_res["success"] == True
    assert json_res["message"] == "User logged in successfully"
    assert "access_token" in json_res
    print("Access token:\n", json_res["access_token"])
    assert json_res["token_type"] == "bearer"
