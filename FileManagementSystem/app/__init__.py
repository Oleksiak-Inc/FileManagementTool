from flask import Flask
from config import CONFIG
from sql_loader import SQL_COMMANDS

sql_commands = SQL_COMMANDS()
config = CONFIG()

def create_app():
    app = Flask(__name__)

    # Import and register routes
    from .routes import register_routes
    register_routes(app)

    return app
