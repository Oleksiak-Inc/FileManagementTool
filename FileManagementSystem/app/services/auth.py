from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional
from app.database.models import Tester
from app.utils.auth import verify_password
from app.api.dependencies import create_access_token

def authenticate_tester(db: Session, email: str, password: str) -> Optional[Tester]:
    tester = db.query(Tester).filter(Tester.email == email).first()
    if not tester:
        return None
    if not verify_password(password, tester.password):
        return None
    return tester

def login_tester(db: Session, tester: Tester) -> dict:
    # Update last login
    tester.last_login_at = datetime.utcnow()
    db.commit()
    db.refresh(tester)
    
    # Create token
    access_token = create_access_token(
        data={
            "sub": str(tester.id),
            "email": tester.email,
            "tester_type_id": tester.tester_type_id
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }