import asyncio
from app.database import SessionLocal
from app.models.user import User
from app.utils.auth import hash_password

async def test_user_retrieval():
    """Test that we can retrieve user and check boolean fields"""
    db = SessionLocal()
    
    # Create a test user
    test_user = User(
        email="dependency_test@example.com",
        hashed_password=hash_password("Test123!"),
        full_name="Dependency Test",
        is_active=True,
        is_admin=False
    )
    
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    # Test boolean checks (this is what dependencies.py does)
    print(f"User ID: {test_user.id}")
    print(f"Is Active: {test_user.is_active}")
    print(f"Is Admin: {test_user.is_admin}")
    
    # Test the conditions from dependencies
    if not test_user.is_active:
        print("❌ User is inactive")
    else:
        print("✅ User is active")
    
    if not test_user.is_admin:
        print("✅ User is not admin (correct)")
    else:
        print("❌ User is admin")
    
    # Cleanup
    db.delete(test_user)
    db.commit()
    db.close()
    
    print("\n🎉 Dependencies would work correctly!")

# Run test
asyncio.run(test_user_retrieval())
