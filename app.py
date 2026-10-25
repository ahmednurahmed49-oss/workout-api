from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Workout, Exercise, WorkoutExercise
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)


@app.route("/")
def home():
    return {"message": "Workout API is running!"}


# WORKOUTS

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts), 200


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return {"error": "Workout not found"}, 404

    result = workout_schema.dump(workout)
    result["exercises"] = workout_exercises_schema.dump(workout.exercises)
    return result, 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json(silent=True) or {}

    try:
        validated_data = workout_schema.load(data)
    except ValidationError as error:
        return {"errors": error.messages}, 400

    if validated_data.get("date") is None:
        validated_data.pop("date", None)

    workout = Workout(**validated_data)
    db.session.add(workout)
    db.session.commit()

    return workout_schema.dump(workout), 201


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return {"error": "Workout not found"}, 404

    db.session.delete(workout)
    db.session.commit()

    return {"message": "Workout deleted successfully"}, 200


# EXERCISES

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.dump(exercises), 200


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return {"error": "Exercise not found"}, 404

    return exercise_schema.dump(exercise), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json(silent=True) or {}

    try:
        validated_data = exercise_schema.load(data)
    except ValidationError as error:
        return {"errors": error.messages}, 400

    exercise = Exercise(**validated_data)
    db.session.add(exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "An exercise with this name already exists"}, 409

    return exercise_schema.dump(exercise), 201


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return {"error": "Exercise not found"}, 404

    db.session.delete(exercise)
    db.session.commit()

    return {"message": "Exercise deleted successfully"}, 200


# ADD AN EXERCISE TO A WORKOUT

@app.route("/workout-exercises", methods=["POST"])
def add_exercise_to_workout():
    data = request.get_json(silent=True) or {}

    try:
        validated_data = workout_exercise_schema.load(data)
    except ValidationError as error:
        return {"errors": error.messages}, 400

    workout = db.session.get(Workout, validated_data["workout_id"])
    exercise = db.session.get(Exercise, validated_data["exercise_id"])

    if workout is None:
        return {"error": "Workout not found"}, 404

    if exercise is None:
        return {"error": "Exercise not found"}, 404

    entry = WorkoutExercise(**validated_data)
    db.session.add(entry)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {
            "error": "This exercise is already in the workout, or its details violate a database constraint"
        }, 409

    return workout_exercise_schema.dump(entry), 201


if __name__ == "__main__":
    app.run(debug=True)