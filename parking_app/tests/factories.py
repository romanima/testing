import factory
from faker import Faker
from app.models import Client, Parking

fake = Faker()

class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = factory.LazyAttribute(lambda _: fake.credit_card_number() if fake.pybool() else None)
    car_number = factory.LazyAttribute(lambda _: f"{fake.bothify('???-###')}")

class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking

    address = factory.Faker('address')
    opened = factory.Faker('pybool')
    count_places = factory.Faker('random_int', min=1, max=50)
    count_available_places = factory.LazyAttribute(lambda obj: obj.count_places)
