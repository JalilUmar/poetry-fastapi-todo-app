import httpx
from httpx import Client


# TEST_COMMAND= "pytest -s -v ./api/test/test_todo.py"

ENDPOINT = "http://localhost:8000"

Bearer_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtamItRlNYdnlmNlFFU3pFdlZ5ZFUiLCJleHAiOjE3MTA1NDMwMjZ9.bil7r1oNOcBVfxVy_Bbjt4P216x5_lO0G6zopymK1Ws"


def test_create_todo_item():
    response = httpx.post(
        f"{ENDPOINT}/api/todo/create",
        headers={"Authorization": Bearer_token},
        json={"title": "test title user3", "description": "test description user3"},
    )

    json_response = response.json()
    assert response.status_code == 201
    assert json_response["success"] == True
    pass


def test_update_todo_item():
    response = httpx.post(
        f"{ENDPOINT}/api/todo/create",
        headers={"Authorization": Bearer_token},
        json={"title": "test title2 user2", "description": "test description2 user2"},
    )

    json_response = response.json()
    print("New todo item: \n", json_response["response"])

    id = json_response["response"]["todoId"]
    req_update = httpx.put(
        f"{ENDPOINT}/api/todo/{id}",
        json={"title": "test title2 user2 updated"},
        headers={"Authorization": Bearer_token},
    )
    update_json_response = req_update.json()
    print("Update todo item: \n", update_json_response)

    assert req_update.status_code == 202
    assert update_json_response["success"] == True
    pass


def test_get_todo_list():

    with Client(follow_redirects=True) as client:
        response = client.get(
            f"{ENDPOINT}/api/todo", headers={"Authorization": Bearer_token}
        )

    json_response = response.json()
    print("Get all todo response: \n", json_response)
    assert response.status_code == 200
    assert json_response["success"] == True
    pass


def test_delete_todo_item():
    req_create_todo = httpx.post(
        f"{ENDPOINT}/api/todo/create",
        headers={"Authorization": Bearer_token},
        json={"title": "test title3 user2", "description": "test description3 user2"},
    )

    json_response = req_create_todo.json()
    print("New todo item: \n", json_response["response"])
    id = json_response["response"]["todoId"]

    req_delete_todo = httpx.delete(
        f"{ENDPOINT}/api/todo/{id}", headers={"Authorization": Bearer_token}
    )

    delete_json_response = req_delete_todo.json()

    assert req_delete_todo.status_code == 200
    assert delete_json_response["success"] == True
    pass
