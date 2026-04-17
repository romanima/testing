import pytest

@pytest.mark.parametrize("endpoint,method", [
    ("/clients", "GET"),
    ("/parkings", "GET")
])
def test_get_methods_return_200(client, endpoint, method):
    if method == "GET":
        response = client.get(endpoint)
    else:
        pytest.skip(f"Method {method} not tested here")
    assert response.status_code == 200

# Альтернативный вариант — отдельный тест для GET
def test_get_clients(client):
    response = client.get('/clients')
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)

def test_get_parkings(client):
    response = client.get('/parkings')
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)
