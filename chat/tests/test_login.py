from chat_server.main import create_app
from chat_server.routes import active_tokens

def get_client():
    app = create_app()
    return app.test_client()

def test_login_success():
    client = get_client()
    response = client.post("/api/v1/auth/register", json={
        "username": "alice", "password": "test123"
    })
    assert response.status_code == 201

    login_response = client.post("/api/v1/auth/login", json={
        "username": "alice", "password": "test123"
    })
    assert login_response.status_code == 200
    data = login_response.get_json()
    assert data['username'] == "alice"
    assert "token" in data
    assert "user_id" in data

def test_login_request_missing():
    client = get_client()
    login_response = client.post("/api/v1/auth/login", json={})
    assert login_response.status_code == 400
    data = login_response.get_json()
    assert "error" in data
    assert data["error"] == "username and password is required"

def test_login_username_missing():
    client = get_client()
    login_response = client.post("/api/v1/auth/login", json={
        "username": ""
    })
    assert login_response.status_code == 400
    data = login_response.get_json()
    assert "error" in data
    assert data["error"] == "username is required"

def test_login_password_missing():
    client = get_client()
    login_response = client.post("/api/v1/auth/login", json={
        "username": "alice", "password": ""
    })
    assert login_response.status_code == 400
    data = login_response.get_json()
    assert "error" in data
    assert data["error"] == "password is required"

def test_login_username_nonexistent():
    client = get_client()
    login_response = client.post("/api/v1/auth/login", json={
        "username": "alice", "password": "test123"
    })
    assert login_response.status_code == 401
    data = login_response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid credentials"

def test_login_username_nonexistent():
    client = get_client()
    response = client.post("/api/v1/auth/register", json={
        "username": "alice", "password": "test123"
    })
    assert response.status_code == 201
    
    login_response = client.post("/api/v1/auth/login", json={
        "username": "alice", "password": "test1234"
    })
    assert login_response.status_code == 401
    data = login_response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid credentials"

def test_login_token_stored():
    client = get_client()
    response = client.post("/api/v1/auth/register", json={
        "username": "alice", "password": "test123"
    })
    assert response.status_code == 201
    
    login_response = client.post("/api/v1/auth/login", json={
        "username": "alice", "password": "test123"
    })
    assert login_response.status_code == 200
    data = login_response.get_json()
    assert "token" in data
    token = data['token']
    assert token in active_tokens
