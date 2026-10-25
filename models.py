from datetime import date

from app import db


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)

    # Relationship: one workout can have many exercise entries
    exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Workout {self.name}>"


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)

    # Relationship: one exercise can appear in many workouts
    workouts = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Exercise {self.name}>"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    # Database constraints go here, inside the class
    __table_args__ = (
        db.UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="unique_workout_exercise"
        ),
        db.CheckConstraint(
            "sets IS NULL OR sets > 0",
            name="positive_sets"
        ),
        db.CheckConstraint(
            "reps IS NULL OR reps > 0",
            name="positive_reps"
        ),
        db.CheckConstraint(
            "duration_minutes IS NULL OR duration_minutes > 0",
            name="positive_duration"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False
    )

    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)

    # Relationships back to the parent models
    workout = db.relationship(
        "Workout",
        back_populates="exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workouts"
    )