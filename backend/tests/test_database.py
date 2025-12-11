from app.database import SessionLocal, engine
from app.models import User, Event, Registration
from sqlalchemy import inspect

def test_connection():
    """Test database connection"""
    # Test connection
    with engine.connect() as conn:
        assert conn is not None

    # Check tables exist
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert isinstance(tables, list)
    assert len(tables) > 0

    # Test session creation
    db = SessionLocal()
    assert db is not None
    db.close()
    
if __name__ == "__main__":
    print("Testing database setup...\n")
    if test_connection():
        print("\n Database setup complete!")
    else:
        print("\n  Database setup incomplete")