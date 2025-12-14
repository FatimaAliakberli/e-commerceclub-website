from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models.user import User
from app.utils.auth import hash_password
import pytest

client = TestClient(app)

def create_user(email="user@test.com", password="Test123!"):
    db = SessionLocal()

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
    db.close()

    return user


def login_user(email="user@test.com", password="Test123!"):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

def test_get_profile():
    create_user()
    token = login_user()

    response = client.get(
        "/api/profile/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@test.com"
    assert data["full_name"] == "Test User"

def test_update_profile():
    create_user()
    token = login_user()

    response = client.put(
        "/api/profile/me",
        json={"phone": "1234567890"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["phone"] == "1234567890"

def test_change_password():
    create_user()
    token = login_user()

    response = client.put(
        "/api/profile/change-password",
        json={
            "current_password": "Test123!",
            "new_password": "NewPass123!"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    # login should work with new password
    login = client.post(
        "/api/auth/login",
        json={"email": "user@test.com", "password": "NewPass123!"}
    )
    assert login.status_code == 200

def test_change_password_wrong_current():
    create_user()
    token = login_user()

    response = client.put(
        "/api/profile/change-password",
        json={
            "current_password": "WrongPassword",
            "new_password": "NewPass123!"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400

def test_delete_account():
    create_user()
    token = login_user()

    response = client.delete(
        "/api/profile/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    # user should no longer be able to log in
    login = client.post(
        "/api/auth/login",
        json={"email": "user@test.com", "password": "Test123!"}
    )
    assert login.status_code == 401
