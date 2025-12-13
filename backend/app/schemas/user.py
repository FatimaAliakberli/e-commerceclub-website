from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime
import re
import uuid

# --- 1. USERBASE (Clean Model for ORM/Response Structure) ---
# This model is the foundation for UserResponse and MUST NOT have strict patterns/lengths
# so it can handle the long 'DUMMY' strings without validation errors.
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

    model_config = {
        "from_attributes": True  # Crucial for ORM loading
    }
    
    phone_number: Optional[str] = None
    is_university_student: bool = True 
    student_id: Optional[str] = None
    national_id: Optional[str] = None

# --- 2. USERIN (Strict Validation for Request Body) ---
# This model is used to validate the data that comes directly from the frontend.
class UserIn(BaseModel):
    # Re-apply the strict validation rules here
    email: EmailStr = Field(..., max_length=255)
    full_name: str = Field(..., max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    is_university_student: bool = True 
    
    # Strict 5-digit pattern is only applied on INPUT
    student_id: Optional[str] = Field(
        None, max_length=5, pattern=r'^\d{5}$',
        description="Must be exactly 5 digits."
    )
    # Strict 7-alphanumeric pattern is only applied on INPUT
    national_id: Optional[str] = Field(
        None, max_length=7, pattern=r'^[a-zA-Z0-9]{7}$',
        description="Must be exactly 7 alphanumeric characters."
    )

# --- 3. USERCREATE (Conditional Validation & Dummy Substitution) ---
# This model inherits strict validation from UserIn and adds password and custom logic.
class UserCreate(UserIn):
    password: str = Field(..., min_length=8)
    
    # Conditional Check: Ensures EITHER student_id or national_id is provided, but not both.
    @model_validator(mode='after')
    def validate_conditional_ids(self):
        is_uni = self.is_university_student
        
        # We need a unique placeholder, guaranteed not to clash with a real ID/pattern.
        # We use the email which is already guaranteed unique by the DB.
        UNIQUE_SUFFIX = str(uuid.uuid4())[:8] 
        DUMMY_NATIONAL_ID = f"DN-{UNIQUE_SUFFIX}" # e.g., DN-a1b2c3d4
        DUMMY_STUDENT_ID = f"DS-{UNIQUE_SUFFIX}" # e.g., DS-a1b2c3d4
        
        # --- Validation (Requires input based on is_uni) ---
        if is_uni:
            if not self.student_id:
                raise ValueError("Student ID is required for university students.")
            if self.national_id:
                raise ValueError("National ID must be empty if registering as a university student.")
        else: # is NOT a university student
            if not self.national_id:
                raise ValueError("National ID is required for non-university users.")
            if self.student_id:
                raise ValueError("Student ID must be empty if registering as a non-university user.")
        # --- End Validation ---
        
        # --- FIX: Substitute NULL with a unique, non-NULL dummy value (Database requirement) ---
        if is_uni:
            # Uni student has no national ID, set dummy value for the DB unique constraint
            self.national_id = DUMMY_NATIONAL_ID 
        else:
            # Non-uni student has no student ID, set dummy value for the DB unique constraint
            self.student_id = DUMMY_STUDENT_ID
            
        return self

    # Password validation (Using Python's standard re module for strength check)
    @field_validator('password', mode='after')
    @classmethod
    def password_strength(cls, v: str):
        """Validate password strength (8+ chars, 1 U/L/D/S)"""
        
        # Full complexity regex check
        complexity_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+=-`~?/><,.;:\'\"\[\]\{\}\\|]).*$'

        if not re.search(complexity_regex, v):
            raise ValueError(
                'Password must be 8+ chars and contain: 1 uppercase, 1 lowercase, 1 number, and 1 symbol.'
            )
            
        return v
    
# --- 4. USERRESPONSE (API Output Model) ---
# This inherits the clean structure from UserBase and adds required DB-generated fields.
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    # model_config inherited from UserBase, but kept here for clarity if needed:
    model_config = {"from_attributes": True}

# --- OTHER UTILITY MODELS ---
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
    
    @field_validator('new_password')
    @classmethod
    def password_strength(cls, v):
        """Validate new password strength (uppercase, lowercase, number, symbol)"""
        
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain uppercase')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain lowercase')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain number')
            
        symbols = "!@#$%^&*()_+=-`~?/><,.;:'\"[]{}\\|"
        if not any(char in symbols for char in v):
            raise ValueError('Password must contain at least one symbol (e.g., @, #, $)')
            
        return v
