from datetime import datetime, timedelta
from jose import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"
EMAIL_TOKEN_EXPIRE_MINUTES = 60


def create_email_verification_token(user_id: int, new_email: str) -> str:
    payload = {
        "sub": str(user_id),
        "email": new_email,
        "type": "email_verification",
        "exp": datetime.utcnow() + timedelta(minutes=EMAIL_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_email_verification_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])