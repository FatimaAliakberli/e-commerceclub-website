# routes/auth.py (MODIFIED)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
# 1. UPDATED IMPORTS: Assuming UserCreate is now in app.schemas.auth
# 2. Check if UserResponse, UserUpdate, PasswordChange are in app.schemas.auth or app.schemas.user
# If they are in schemas.user, keep the import:
from app.schemas.user import UserCreate, UserBase, UserResponse, UserUpdate, PasswordChange
from app.schemas.auth import LoginRequest, LoginResponse
from app.models.user import User
from app.utils.auth import hash_password, verify_password, create_access_token
from app.utils.dependencies import get_current_user, get_current_admin
from datetime import timedelta, datetime

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with student_id and national_id validation."""
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check for existing student_id
    if db.query(User).filter(User.student_id == user_data.student_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID already registered"
        )

    # Check for existing national_id
    if db.query(User).filter(User.national_id == user_data.national_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="National ID already registered"
        )
        
    # Create new user
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
        
        # --- NEW FIELD ASSIGNMENTS ---
        phone_number=user_data.phone_number,
        is_university_student=user_data.is_university_student,
        student_id=user_data.student_id,
        national_id=user_data.national_id
        # --- END NEW FIELD ASSIGNMENTS ---
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user # Changed return type to simply return the ORM object

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    
    # Get user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    # ... (Login logic is omitted for brevity, it remains the same)
    
    # Verify password (omitted for brevity)
    # ...
    
    # Reset failed attempts on successful login (omitted for brevity)
    # ...
    
    # Create JWT token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "is_admin": user.is_admin} # Ensure is_admin is included for protected routes
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        # Use the UserBase schema for a clean, consistent response
        "user": UserBase.model_validate(user).model_dump() 
    }

# --- REST OF THE ROUTER REMAINS UNCHANGED (get/put/delete /me, change-password) ---
