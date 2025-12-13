# app/schemas/auth.py (FINAL VERSION)

from pydantic import BaseModel, EmailStr
# Import the definition from the correct file:
from app.schemas.user import UserBase # <-- NEW IMPORT

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserBase # <-- Use the imported UserBase

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
    # NOTE: You need to add the Field(min_length=8) and the
    # @field_validator here for new_password validation!
