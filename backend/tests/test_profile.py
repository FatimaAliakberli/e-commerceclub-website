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


def test_get_profile(client, db):
    user = create_user(db)
    token = login_user(client, user.email, "Test123!")

    response = client.get(
        "/api/profile/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email
    assert data["full_name"] == "Test User"


def test_update_profile(client, db):
    user = create_user(db)
    token = login_user(client, user.email, "Test123!")

    response = client.put(
        "/api/profile/me",
        json={"phone": "1234567890"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["phone"] == "1234567890"


def test_change_password(client, db):
    user = create_user(db)
    token = login_user(client, user.email, "Test123!")

    response = client.put(
        "/api/profile/change-password",
        json={
            "current_password": "Test123!",
            "new_password": "NewPass123!"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    # Login with new password works
    login = client.post(
        "/api/auth/login",
        json={"email": user.email, "password": "NewPass123!"}
    )
    assert login.status_code == 200


def test_change_password_wrong_current(client, db):
    user = create_user(db)
    token = login_user(client, user.email, "Test123!")

    response = client.put(
        "/api/profile/change-password",
        json={
            "current_password": "WrongPassword",
            "new_password": "NewPass123!"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400


def test_delete_account(client, db):
    user = create_user(db)
    token = login_user(client, user.email, "Test123!")

    response = client.delete(
        "/api/profile/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    # User can no longer log in
    login = client.post(
        "/api/auth/login",
        json={"email": user.email, "password": "Test123!"}
    )
    assert login.status_code == 401
