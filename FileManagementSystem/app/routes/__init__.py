from .users import users_bp
from .auth import auth_bp
from .root import root_bp

def register_routes(api):
    api.register_blueprint(root_bp)
    api.register_blueprint(auth_bp)
    api.register_blueprint(users_bp)
