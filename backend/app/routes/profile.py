from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.profile import (
    ProfileResponse,
    ProfileUpdate,
    PasswordChange,
    DeleteAccount,
    EmailChangeRequest,
    MessageResponse
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


@router.post(
    "/change-email",
    response_model=MessageResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def request_email_change(
    payload: EmailChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await ProfileService.request_email_change(
        db=db,
        user=current_user,
        new_email=str(payload.new_email),
    )
    return {"message": "Verification email sent"}

@router.get("/confirm-email-change", response_model=MessageResponse
)
def confirm_email_change(
    token: str,
    db: Session = Depends(get_db)
):
    return ProfileService.confirm_email_change(db, token)
