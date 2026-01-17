from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, ma
from .api import register_blueprints
from .swagger import init_swagger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)

    register_blueprints(app)
    init_swagger(app)

    return app
