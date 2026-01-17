from flask_jwt_extended import create_access_token
from ..models import User
from ..utils.hashing import verify_password
from datetime import datetime
from ..extensions import db

class AuthService:

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email, active=True).first()
        if not user or not verify_password(password, user.password):
            raise ValueError("Invalid credentials")

        user.last_login_at = datetime.utcnow()
        db.session.commit()

        return create_access_token(identity=user.id)
