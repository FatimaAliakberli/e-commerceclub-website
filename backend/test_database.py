from app.database import SessionLocal, engine
from app.models import User, Event, Registration
from sqlalchemy import inspect

def test_connection():
    """Test database connection"""
    try:
        # Test connection
        with engine.connect() as conn:
            print(" Database connection successful")
        
        # Check tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\n Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table}")
        
        # Test session
        db = SessionLocal()
        print("\n Database session created successfully")
        db.close()
        
        return True
    except Exception as e:
        print(f" Database test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing database setup...\n")
    if test_connection():
        print("\n Database setup complete!")
    else:
        print("\n  Database setup incomplete")