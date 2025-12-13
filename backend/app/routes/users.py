# app/routes/users.py (Conceptual Example)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.dependencies import get_db, get_current_user # Assuming you have get_current_user
from app.schemas.user import UserResponse
from app.models.user import User as UserModel

router = APIRouter(
    
    tags=["users"],
)

# Endpoint 1: Get the current user's profile (Requires authentication)
@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: UserModel = Depends(get_current_user), # Dependency checks JWT and fetches user object
    db: Session = Depends(get_db)
):
    """
    Returns the full profile of the currently authenticated user.
    The UserResponse model ensures the is_admin field is included.
    """
    # The current_user object is already loaded by the dependency (get_current_user)
    return current_user 

# You might already have a version of this function, but ensure it exists
# and returns the full user object needed by the UserResponse schema.