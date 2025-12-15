import pytest
from unittest.mock import patch

from app.models.user import User
from app.utils.tokens import create_email_verification_token


# REQUEST EMAIL CHANGE

def test_request_email_change(auth_client):
    with patch("app.services.profile_service.send_verification_email") as mock_send:
        response = auth_client.post(
            "/api/profile/change-email",
            json={"new_email": "newemail@test.com"},
        )

    assert response.status_code == 202
    assert response.json()["message"] == "Verification email sent"
    mock_send.assert_called_once()


def test_request_email_change_duplicate(auth_client, db):
    # Create another user with same email
    existing = User(
        email="duplicate@test.com",
        hashed_password="hashed",
        full_name="Existing User",
        is_active=True,
        is_admin=False,
    )
    db.add(existing)
    db.commit()

    response = auth_client.post(
        "/api/profile/change-email",
        json={"new_email": "duplicate@test.com"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already in use"


# CONFIRM EMAIL CHANGE

def test_confirm_email_change(auth_client, db, test_user):
    new_email = "confirmed@test.com"

    token = create_email_verification_token(
        user_id=test_user.id,
        new_email=new_email,
        token_type="email_change",
    )

    response = auth_client.get(
        "/api/profile/confirm-email-change",
        params={"token": token},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Email updated successfully"

    db.refresh(test_user)
    assert test_user.email == new_email


def test_confirm_email_change_invalid_token(auth_client):
    response = auth_client.get(
        "/api/profile/confirm-email-change",
        params={"token": "invalid.token.here"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired token"
