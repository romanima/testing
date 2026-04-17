import pytest

from app.models import Client, Parking


@pytest.mark.parametrize("url", [
    "/clients",
    "/parkings"
])
def test_get_methods_return_200(client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_create_client(client, db):
    data = {
        'name': 'Test Client',
        'surname': 'Test Surname',
        'credit_card': '1234567890123456',
        'car_number': 'A123BC'
    }
    response = client.post('/clients', json=data)
    assert response.status_code == 201
    client_data = response.get_json()
    assert 'id' in client_data


def test_create_parking(client, db):
    data = {
        'address': 'Test Address',
        'opened': True,
        'count_places': 10
    }
    response = client.post('/parkings', json=data)
    assert response.status_code == 201
    parking_data = response.get_json()
    assert 'id' in parking_data


@pytest.mark.parking
def test_exit_parking(client, db):
    # Создаём клиента
    client_data = {
        'name': 'John',
        'surname': 'Doe',
        'credit_card': '1234',
        'car_number': 'B123CD'
    }
    client_response = client.post('/clients', json=client_data)
    client_id = client_response.get_json()['id']

    # Создаём парковку
    parking_data = {
        'address': 'Main Street',
        'opened': True,
        'count_places': 5
    }
    parking_response = client.post('/parkings', json=parking_data)
    parking_id = parking_response.get_json()['id']

    # Заезд на парковку
    enter_data = {'client_id': client_id, 'parking_id': parking_id}
    enter_response = client.post('/client_parkings', json=enter_data)
    assert enter_response.status_code == 201

    # Выезд с парковки
    exit_data = {'client_id': client_id, 'parking_id': parking_id}
    response = client.delete('/client_parkings', json=exit_data)
    assert response.status_code == 200

    # Проверяем, что количество свободных мест увеличилось
    parking = Parking.query.get(parking_id)
    assert parking.count_available_places == 5


# Тесты с использованием Factory Boy
def test_create_client_with_factory(client, db_session):
    from tests.factories import ClientFactory, set_session

    set_session(db_session)  # Устанавливаем сессию для фабрик
    client_factory = ClientFactory()

    response = client.post('/clients', json={
        'name': client_factory.name,
        'surname': client_factory.surname,
        'credit_card': client_factory.credit_card,
        'car_number': client_factory.car_number
    })
    assert response.status_code == 201

    created_client = Client.query.filter_by(
        name=client_factory.name, surname=client_factory.surname
    ).first()
    assert created_client is not None


def test_create_parking_with_factory(client, db_session):
    from tests.factories import ParkingFactory, set_session

    set_session(db_session)  # Устанавливаем сессию для фабрик
    parking_factory = ParkingFactory()

    response = client.post('/parkings', json={
        'address': parking_factory.address,
        'opened': parking_factory.opened,
        'count_places': parking_factory.count_places
    })
    assert response.status_code == 201

    created_parking = (
        Parking.query.filter_by(address=parking_factory.address).first())
    assert created_parking is not None
