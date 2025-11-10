# Add this fixture to reset the activities state between tests
import pytest
from src.app import activities

@pytest.fixture(autouse=True)
def reset_activities_state():
    # Store original state
    original_state = activities.copy()
    
    # Let the test run
    yield
    
    # Restore original state after test
    activities.clear()
    activities.update(original_state)