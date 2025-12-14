from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.profile import (
    ProfileResponse,
    ProfileUpdate,
    PasswordChange,
    DeleteAccount
)
from app.services.profile_service import ProfileService
from app.utils.dependencies import get_current_user
from app.models.user import User


router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.get("/me", response_model=ProfileResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return ProfileService.get_profile(current_user)


@router.put("/me", response_model=ProfileResponse)
def update_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ProfileService.update_profile(db, current_user, data)


@router.put("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ProfileService.change_password(
        db,
        current_user,
        data.current_password,
        data.new_password
    )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    payload: DeleteAccount,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ProfileService.delete_account(
        db=db,
        user=current_user,
        confirm=payload.confirm,
    )

@router.post("/change-email")
async def change_email(
    new_email: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await ProfileService.request_email_change(db, current_user, new_email)

@router.get("/verify-email")
def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    return ProfileService.confirm_email_change(db, token)
