import pytest
from app import create_app, db
from tests.factories import ClientFactory, ParkingFactory

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()  # Создаём таблицы ДО любых операций
            # Передаём сессию фабрикам
            ClientFactory._meta.sqlalchemy_session = db.session
            ParkingFactory._meta.sqlalchemy_session = db.session
        yield client

@pytest.fixture(autouse=True)
def db_session(app):
    """Фикстура для управления сессией БД."""
    with app.app_context():
        yield db.session
        db.session.rollback()  # Откат после каждого теста
