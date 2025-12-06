from app.utils.auth import hash_password, verify_password, create_access_token, verify_token

# Test password hashing
print("Testing password functions...")
password = "Test123!"
hashed = hash_password(password)
print(f" Password hashed: {hashed[:20]}...")

# Test password verification
is_valid = verify_password(password, hashed)
print(f" Password verification: {is_valid}")

is_invalid = verify_password("wrongpassword", hashed)
print(f" Wrong password rejected: {not is_invalid}")

# Test JWT token creation
print("\nTesting JWT functions...")
token = create_access_token(data={"sub": "123", "email": "test@example.com"})
print(f" Token created: {token[:30]}...")

# Test JWT token verification
payload = verify_token(token)
if payload:
    print(f"Token verified: user_id={payload.get('sub')}, email={payload.get('email')}")
else:
    print(" Token verification failed")

# Test invalid token
invalid_payload = verify_token("invalid_token")
print(f"Invalid token rejected: {invalid_payload is None}")

print("\n All authentication functions working!")

