from flask_smorest import Blueprint

root_bp = Blueprint(
    "root",
    "root",
    url_prefix="/",
    description="Service root"
)

@root_bp.route("/")
def root():
    return {
        "service": "FileManagementSystem",
        "status": "running",
        "docs": "/swagger"
    }
