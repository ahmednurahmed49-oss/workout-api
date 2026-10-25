import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "Workout API is running!"


def test_get_workouts(client):
    response = client.get("/workouts")

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_exercises(client):
    response = client.get("/exercises")

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_missing_workout_returns_404(client):
    response = client.get("/workouts/999999")

    assert response.status_code == 404


def test_invalid_exercise_returns_400(client):
    response = client.post(
        "/exercises",
        json={"name": "", "description": "Invalid exercise"}
    )

    assert response.status_code == 400