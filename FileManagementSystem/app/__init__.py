from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from config import CONFIG
from .routes import register_routes

config = CONFIG()

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    
    app.config["JWT_SECRET_KEY"] = config["JWT_SECRET_KEY"]
    app.config["API_TITLE"] = "File Management System"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    jwt = JWTManager(app)

    @app.errorhandler(Exception)
    def handle_exception(e):
        return {
            "status": "error",
            "msg": str(e)
        }, 500

    api = Api(app)
    register_routes(api)

    return app
