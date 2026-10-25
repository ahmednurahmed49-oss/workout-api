from app import app, db
from models import Workout, Exercise, WorkoutExercise


def seed_data():
    with app.app_context():
        # Create the tables if they do not exist
        db.create_all()

        # Avoid inserting the same sample records repeatedly
        workout = Workout.query.filter_by(name="Full Body Workout").first()
        if workout is None:
            workout = Workout(name="Full Body Workout")
            db.session.add(workout)

        exercises_data = [
            {
                "name": "Push-ups",
                "description": "A bodyweight exercise for the chest, shoulders, and triceps."
            },
            {
                "name": "Squats",
                "description": "A lower-body exercise targeting the legs and glutes."
            },
            {
                "name": "Plank",
                "description": "A core exercise that builds stability and endurance."
            }
        ]

        exercises = []
        for item in exercises_data:
            exercise = Exercise.query.filter_by(name=item["name"]).first()

            if exercise is None:
                exercise = Exercise(**item)
                db.session.add(exercise)

            exercises.append(exercise)

        db.session.flush()

        # Connect each sample exercise to the workout only once
        for exercise in exercises:
            existing = WorkoutExercise.query.filter_by(
                workout_id=workout.id,
                exercise_id=exercise.id
            ).first()

            if existing is None:
                db.session.add(
                    WorkoutExercise(
                        workout=workout,
                        exercise=exercise,
                        sets=3,
                        reps=10
                    )
                )

        db.session.commit()
        print("Seed data added successfully!")


if __name__ == "__main__":
    seed_data()