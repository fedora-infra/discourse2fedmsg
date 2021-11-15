def test_healthz_liveness(client):
    """Test the /healthz/live check endpoint"""
    response = client.get("/healthz/live")
    assert response.status_code == 200
    assert response.data == b'{"status": 200, "title": "OK"}'


def test_healthz_readiness_ok(client):
    """Test the /healthz/ready check endpoint"""
    response = client.get("/healthz/ready")
    print(response.data)
    assert response.status_code == 200
    assert response.data == b'{"status": 200, "title": "OK"}'
