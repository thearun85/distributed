from chat_server.main import create_app
from chat_server.db import Base, engine


def get_client():
    app = create_app()
    return app.test_client()


def test_user_registration_success():
    client = get_client()
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "alice",
            "password": "secret123",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "alice"
    assert data["user_id"] > 0
    assert "created_at" in data


def test_request_missing():
    client = get_client()
    response = client.post("/api/v1/auth/register", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "username and password is required"


def test_username_missing():
    client = get_client()
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "",
        },
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "username is required"


def test_password_missing():
    client = get_client()
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "alice",
            "password": "",
        },
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "password is required"


def test_username_short():
    client = get_client()
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "hi",
            "password": "secret",
        },
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "username must be between 3 and 50 characters"


def test_username_long():
    client = get_client()
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "asdfghjkloasdfghjkloasdfghjkloasdfghjkloasdfghjkloasdfghjklo",
            "password": "secret",
        },
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "username must be between 3 and 50 characters"


def test_password_short():
    client = get_client()
    response = client.post(
        "/api/v1/auth/register", json={"username": "alice", "password": "sec"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "password must be atleast 6 characters"


def test_duplicate_username():
    client = get_client()
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "alice",
            "password": "secret123",
        },
    )
    assert response.status_code == 201
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "alice",
            "password": "secret123",
        },
    )
    assert response.status_code == 409
