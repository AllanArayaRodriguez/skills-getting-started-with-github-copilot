from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_duplicate_signup_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up"}


def test_full_activity_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    activity = activities[activity_name]
    original_participants = list(activity["participants"])
    activity["participants"] = [f"student{i}@mergington.edu" for i in range(activity["max_participants"])]

    try:
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        assert response.json() == {"detail": "Activity is full"}
    finally:
        activity["participants"] = original_participants
