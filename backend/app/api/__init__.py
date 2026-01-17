from .auth import bp as auth_bp
from .users import bp as users_bp
from .projects import bp as projects_bp
from .test_cases import bp as test_cases_bp
from .executions import bp as executions_bp
from .attachments import bp as attachments_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(test_cases_bp)
    app.register_blueprint(executions_bp)
    app.register_blueprint(attachments_bp)
