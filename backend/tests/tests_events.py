# backend/tests/test_events.py
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models.user import User
from app.models.event import Event
from app.utils.auth import hash_password
from datetime import datetime, timedelta

client = TestClient(app)

def setup_test_data():
    """Create test admin and event"""
    db = SessionLocal()
    
    # Create admin
    admin = User(
        email="admin@test.com",
        hashed_password=hash_password("Admin123!"),
        full_name="Test Admin",
        is_admin=True
    )
    db.add(admin)
    db.commit()
    
    db.close()

def test_create_event():
    """Test creating an event as admin"""
    # Login as admin
    login_response = client.post(
        "/api/auth/login",
        json={"email": "admin@test.com", "password": "Admin123!"}
    )
    token = login_response.json()["access_token"]
    
    # Create event
    event_data = {
        "title": "Test Event",
        "description": "A test event",
        "event_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        "event_time": "18:00",
        "location": "Test Hall",
        "capacity": 50,
        "registration_deadline": (datetime.utcnow() + timedelta(days=5)).isoformat()
    }
    
    response = client.post(
        "/api/events/",
        json=event_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    assert response.json()["title"] == "Test Event"

def test_list_events():
    """Test listing events"""
    response = client.get("/api/events/")
    assert response.status_code == 200
    assert "events" in response.json()

def test_register_for_event():
    """Test user registration for event"""
    # Create and login as regular user
    # Register for event
    # Assert success
    pass  # Implement full test

# Run: pytest tests/test_events.py -v