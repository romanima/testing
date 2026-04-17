import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        from app import db
        db.create_all()

    yield app

    with app.app_context():
        from app import db
        db.drop_all()
        db.session.remove()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    with app.app_context():
        from app import db as _db
        yield _db


@pytest.fixture
def db_session(db):
    """Фикстура для предоставления активной сессии БД."""
    session = db.session
    yield session
    session.rollback()  # Откат изменений после теста
