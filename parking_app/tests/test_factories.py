import pytest
from tests.factories import ClientFactory, ParkingFactory

def test_client_factory(client, db_session):
    client_obj = ClientFactory()
    db_session.commit()  # Явно сохраняем в БД
    assert client_obj.id is not None
    assert isinstance(client_obj.name, str)
    assert len(client_obj.car_number) > 0

def test_parking_factory(client, db_session):
    parking_obj = ParkingFactory()
    db_session.commit()  # Явно сохраняем в БД
    assert parking_obj.id is not None
    assert parking_obj.count_available_places == parking_obj.count_places
    assert isinstance(parking_obj.address, str)
