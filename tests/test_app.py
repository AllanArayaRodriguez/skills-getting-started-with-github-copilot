from pathlib import Path

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


def test_activity_cards_render_participants_list():
    app_js = (Path(__file__).resolve().parents[1] / "src" / "static" / "app.js").read_text()

    assert "Participants" in app_js
    assert "participantsList" in app_js


def test_remove_participant_from_activity():
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"
    activity = activities[activity_name]
    original_participants = list(activity["participants"])

    try:
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        assert response.status_code == 200
        assert email not in activity["participants"]
        assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    finally:
        activity["participants"] = original_participants
