from datetime import datetime, timedelta

def test_create_event(client):
    login_response = client.post(
        "/api/auth/login",
        json={"email": "admin@test.com", "password": "Admin123!"}
    )
    token = login_response.json()["access_token"]

    event_data = {
        "title": "Test Event",
        "description": "A test event",
        "event_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        "registration_deadline": (datetime.utcnow() + timedelta(days=5)).isoformat(),
        "event_time": "18:00",
        "location": "Test Hall",
        "capacity": 50
    }

    res = client.post(
        "/api/events/",
        json=event_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 201
