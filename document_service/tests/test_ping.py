def test_ping(client):
    response = client.get('/document/ping')
    assert response.status_code == 200
    assert b'is alive' in response.data
