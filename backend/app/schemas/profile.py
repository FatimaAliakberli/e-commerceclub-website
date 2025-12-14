from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional

class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone: Optional[str] = Field(None, alias="phone_number")
    is_verified: Optional[bool] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

class ProfileUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, alias="phone_number")
    full_name: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)

class PasswordChange(BaseModel):
    current_password: str
    new_password: str


class DeleteAccount(BaseModel):
    confirm: bool
