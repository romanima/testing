import factory
from faker import Faker
from app.models import Client, Parking

fake = Faker()


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = factory.LazyAttribute(lambda x:
                                        fake.credit_card_number()
                                        if fake.pybool() else None)
    car_number = factory.Faker('license_plate')


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session_persistence = 'commit'

    address = factory.Faker('address')
    opened = factory.Faker('pybool')
    count_places = factory.Faker('random_int',
                                 min=1,
                                 max=100)
    count_available_places = factory.LazyAttribute(lambda obj:
                                                   obj.count_places)


# Глобальные переменные для хранения сессии
_session = None


def set_session(session):
    global _session
    _session = session
    ClientFactory._meta.sqlalchemy_session = session
    ParkingFactory._meta.sqlalchemy_session = session
