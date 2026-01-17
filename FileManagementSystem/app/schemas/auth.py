from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    tester_id: int
    email: EmailStr
    tester_type_id: int

class LoginRequest(BaseModel):
    email: EmailStr
    password: str