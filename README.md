Workout API

A RESTful backend API for managing workouts and reusable exercises, built with Flask, SQLAlchemy, Flask-Migrate, and Marshmallow.

Features

* Create, view, and delete workouts.
* Create, view, and delete exercises.
* Add exercises to workouts with sets, reps, or duration.
* Validate incoming data using Marshmallow.
* Enforce database constraints and prevent duplicate exercises within a workout.
* Seed the database with sample workout and exercise data.

Technologies

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Migrate and Alembic
* Marshmallow
* SQLite
* Pipenv

Setup

1. Clone or download this repository.
2. Install dependencies:

pipenv install

3. Apply database migrations:

pipenv run flask --app app db upgrade

4. Add sample data:

pipenv run python seed.py

5. Start the development server:

pipenv run python app.py

The API will be available at http://127.0.0.1:5000.

API Endpoints

Method	Endpoint	Purpose
GET	/	Check that the API is running
GET	/workouts	List all workouts
GET	/workouts/<workout_id>	Retrieve one workout and its exercise entries
POST	/workouts	Create a workout
DELETE	/workouts/<workout_id>	Delete a workout
GET	/exercises	List all exercises
GET	/exercises/<exercise_id>	Retrieve one exercise
POST	/exercises	Create an exercise
DELETE	/exercises/<exercise_id>	Delete an exercise
POST	/workout-exercises	Add an exercise to a workout

Example Requests

Create a workout:

{
  "name": "Morning Workout"
}

Create an exercise:

{
  "name": "Push-ups",
  "description": "A bodyweight exercise for the chest, shoulders, and triceps."
}

Add an exercise to a workout:

{
  "workout_id": 1,
  "exercise_id": 1,
  "sets": 3,
  "reps": 10
}

Requests that create resources should use JSON request bodies. Successful creations return HTTP 201; validation errors return 400; missing resources return 404.

Seed Data

Run pipenv run python seed.py to populate the database with sample workouts and exercises.

Testing

Run the development server and test the endpoints using a REST client, or use Flask’s test client to verify responses and validation.

Author

Developed as a Flask backend API project.