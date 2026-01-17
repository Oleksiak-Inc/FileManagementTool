from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.database.session import get_db
from app.database.models import Tester
from app.schemas.auth import TokenData

security = HTTPBearer()

def get_current_tester(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Tester:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        tester_id: int = int(payload.get("sub"))
        if tester_id is None:
            raise credentials_exception
        token_data = TokenData(
            tester_id=tester_id,
            email=payload.get("email"),
            tester_type_id=payload.get("tester_type_id")
        )
    except (JWTError, ValueError):
        raise credentials_exception
    
    tester = db.query(Tester).filter(Tester.id == token_data.tester_id).first()
    if tester is None:
        raise credentials_exception
    if not tester.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive tester"
        )
    return tester

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def require_admin(current_user: Tester = Depends(get_current_tester)):
    if current_user.tester_type_id not in (1, 2):  # super, admin
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user