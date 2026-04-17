from flask import Flask
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import register_routes
    register_routes(app)
    return app
