import httpx


# TEST_COMMAND= "pytest -s -v ./api/test/test_user.py"

ENDPOINT = "http://localhost:8000"

Bearer_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtamItRlNYdnlmNlFFU3pFdlZ5ZFUiLCJleHAiOjE3MTA1NDI4NjN9.2osF7pourFa6deJcjXN9pjSo5JCUNxPkVgtzcTHdAvg"


def test_can_call_endpoint():
    response = httpx.get(ENDPOINT + "/api/health")
    print("Testing endpoint")
    assert response.status_code == 200
    pass


def test_create_new_user():
    response = httpx.post(
        ENDPOINT + "/api/users/register",
        json={
            "username": "user7",
            "email": "user7@test.com",
            "password": "user12345",
        },
    )
    json_response = response.json()
    assert response.status_code == 201
    assert json_response["success"] == True
    pass


def test_login_user():
    response = httpx.post(
        ENDPOINT + "/api/users/login",
        data={
            "username": "user2",
            "password": "user12345",
        },
    )
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["token_type"] == "bearer"
    assert json_response["access_token"]
    print("Access token:\n", json_response["access_token"])
    pass
