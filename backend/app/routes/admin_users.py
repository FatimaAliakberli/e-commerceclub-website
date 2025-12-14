# routes/admin_users.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.utils.dependencies import get_current_admin
from pydantic import BaseModel, Field

# Define a Schema for the Admin actions
class AdminRoleUpdate(BaseModel):
    is_admin: bool = Field(..., description="The new administrative status for the user.")

class AdminActiveUpdate(BaseModel):
    is_active: bool = Field(..., description="The new active status for the user.")


router = APIRouter(prefix="/users", tags=["Admin - Users"])

@router.get("/", response_model=List[UserResponse])
async def list_all_users(
    # Only an admin can access this route
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all users in the system. (Admin only)
    """
    users = db.query(User).all()
    # We use UserResponse for security to prevent sending sensitive data like hashed_password
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific user by ID. (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.patch("/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: int,
    role_update: AdminRoleUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Update a user's admin privileges (is_admin). (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # 🛑 SECURITY CHECK: Prevent admin from revoking their own admin status
    if user.id == current_admin.id and not role_update.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot revoke your own admin privileges."
        )

    user.is_admin = role_update.is_admin
    db.commit()
    db.refresh(user)
    return user

@router.patch("/{user_id}/active", response_model=UserResponse)
async def update_user_active_status(
    user_id: int,
    active_update: AdminActiveUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Update a user's active status (e.g., deactivating a user). (Admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 🛑 SECURITY CHECK: Prevent admin from deactivating themselves
    if user.id == current_admin.id and not active_update.is_active:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account."
        )

    user.is_active = active_update.is_active
    db.commit()
    db.refresh(user)

    return user
