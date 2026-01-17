from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.auth import Token, LoginRequest
from app.services.auth import authenticate_tester, login_tester

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    tester = authenticate_tester(
        db,
        email=login_data.email,
        password=login_data.password
    )
    if not tester:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return login_tester(db, tester)

@router.post("/test-token", dependencies=[Depends(HTTPBearer())])
def test_token():
    """Test if token is valid"""
    return {"msg": "Token is valid"}