import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200  # OK with redirect
    assert response.url.path == "/static/index.html"  # Check final URL after redirect

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    # Test structure of an activity
    first_activity = next(iter(activities.values()))
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity
    assert isinstance(first_activity["participants"], list)

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up test@mergington.edu for Chess Club"
    
    # Verify student was added
    activities = client.get("/activities").json()
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]
    
    # Test duplicate signup
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()

def test_signup_nonexistent_activity():
    response = client.post("/activities/NonexistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_unregister_from_activity():
    # First sign up a test student
    email = "unregister_test@mergington.edu"
    client.post(f"/activities/Chess Club/signup?email={email}")
    
    # Test successful unregistration
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"
    
    # Verify student was removed
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]
    
    # Test unregistering when not registered
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"].lower()

def test_unregister_from_nonexistent_activity():
    response = client.delete("/activities/NonexistentClub/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()