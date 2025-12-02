from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    is_university_student: bool = True
    id_code: Optional[str] = None  # Required for non-university users

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        return v
    
    @validator('id_code')
    def validate_id_code(cls, v, values):
        """Require ID code for non-university users"""
        if not values.get('is_university_student') and not v:
            raise ValueError('ID code is required for non-university users')
        return v

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows converting SQLAlchemy models to Pydantic

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    full_name: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    
    @validator('new_password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain uppercase')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain lowercase')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain number')
        return v