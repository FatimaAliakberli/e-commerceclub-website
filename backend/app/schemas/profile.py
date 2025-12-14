from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone_number: Optional[str]
    is_verified: bool

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


class DeleteAccount(BaseModel):
    confirm: bool
