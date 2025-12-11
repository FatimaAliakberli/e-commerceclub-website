from app.database import SessionLocal
from app.models.user import User
from app.utils.auth import hash_password

def test_user_retrieval():
    """Test that we can retrieve a user and validate flags."""

    db = SessionLocal()

    # Create test user
    user = User(
        email="dependency_test@example.com",
        hashed_password=hash_password("Test123!"),
        full_name="Dependency Test",
        is_active=True,
        is_admin=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Assertions
    assert user.id is not None
    assert user.is_active is True
    assert user.is_admin is False

    # Cleanup
    db.delete(user)
    db.commit()
    db.close()
