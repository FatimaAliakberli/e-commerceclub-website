from app.models.user import User
from app.utils.auth import hash_password
import uuid

def create_user(db, email=None, password="Test123!"):
    if email is None:
        email = f"user_{uuid.uuid4()}@test.com"

    user = User(
        email=email,
        hashed_password=hash_password(password),
        full_name="Test User",
        is_active=True,
        is_admin=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(client, email, password):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_get_profile(auth_client):
    response = auth_client.get("/api/profile/me")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_update_profile(auth_client):
    response = auth_client.put(
        "/api/profile/me",
        json={"phone_number": "1234567890"},
    )
    assert response.status_code == 200
    assert response.json()["phone_number"] == "1234567890"


def test_change_password(auth_client):
    response = auth_client.put(
        "/api/profile/change-password",
        json={
            "current_password": "Password123!",
            "new_password": "NewPassword123!"
        }
    )
    assert response.status_code == 204


def test_change_password_wrong_current(auth_client):
    response = auth_client.put(
        "/api/profile/change-password",
        json={
            "current_password": "WrongPassword",
            "new_password": "NewPassword123!"
        }
    )
    assert response.status_code == 400


def test_delete_account(auth_client):
    response = auth_client.request(
        "DELETE","/api/profile/me",
        json={"confirm": True},
    )
    assert response.status_code == 204
