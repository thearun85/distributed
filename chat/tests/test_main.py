from chat_server.main import create_app

def test_health():
    app = create_app()
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    data = response.get_json()
    assert data['app'] == 'distributed-chat'
    assert data['version'] == '0.1.0'
    assert data['status'] == 'healthy'
      
