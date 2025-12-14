from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.profile import ProfileUpdate
from app.utils.auth import verify_password, hash_password
from app.services.email import send_verification_email
from app.utils.tokens import create_email_verification_token, verify_email_verification_token
from jose import JWTError

class ProfileService:

    @staticmethod
    def get_profile(user: User) -> User:
        return user

    @staticmethod
    def update_profile(
        db: Session,
        user: User,
        data: ProfileUpdate
    ) -> User:
        if data.email:
            user.email = data.email

        if data.phone_number:
            user.phone = data.phone_number

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def change_password(
        db: Session,
        user: User,
        current_password: str,
        new_password: str
    ) -> None:
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )

        user.hashed_password = hash_password(new_password)
        db.commit()

    @staticmethod
    def delete_account(
        db: Session,
        user: User,
        confirm: bool
    ) -> None:
        if not confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account deletion not confirmed"
            )

        db.delete(user)
        db.commit()

    @staticmethod
    async def request_email_change(
        db: Session,
        user: User,
        new_email: str
    ):
        existing = db.query(User).filter(User.email == new_email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )

        token = create_email_verification_token(user.id, new_email)

        await send_verification_email(
        email=new_email,
        verification_token=token,
        user_name = user.full_name
    )
    @staticmethod
    def confirm_email_change(db: Session, token: str):
        try:
            payload = verify_email_verification_token(token)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token"
            )

        if payload.get("type") != "email_change":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type"
            )

        user_id = int(payload["sub"])
        new_email = payload["new_email"]

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.email = new_email
        db.commit()

        return {"message": "Email updated successfully"}

