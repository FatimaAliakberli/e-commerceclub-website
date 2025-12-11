from app.utils.auth import hash_password, verify_password, create_access_token, verify_token

def test_password_hashing():
    password = "Test123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)

def test_jwt_functions():
    token = create_access_token({"sub": "123", "email": "test@example.com"})
    payload = verify_token(token)

    assert payload is not None
    assert payload["sub"] == "123"
    assert payload["email"] == "test@example.com"

    # invalid token must return None
    assert verify_token("invalid_token") is None
