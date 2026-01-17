from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import abort
from ..models import User

def require_user_type(*allowed):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or user.user_type.name not in allowed:
                abort(403, "Insufficient permissions")
            return fn(*args, **kwargs)
        return wrapper
    return decorator
