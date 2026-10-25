from datetime import date

from sqlalchemy.orm import validates

from extensions import db


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)

    # One workout can contain multiple exercise entries.
    exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Workout name cannot be empty")

        value = value.strip()

        if len(value) > 100:
            raise ValueError("Workout name cannot exceed 100 characters")

        return value

    def __repr__(self):
        return f"<Workout {self.name}>"


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)

    # One exercise can be reused in multiple workouts.
    workouts = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    @validates("name", "description")
    def validate_text(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key.capitalize()} cannot be empty")

        value = value.strip()
        max_length = 100 if key == "name" else 255

        if len(value) > max_length:
            raise ValueError(f"{key.capitalize()} cannot exceed {max_length} characters")

        return value

    def __repr__(self):
        return f"<Exercise {self.name}>"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

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

    # Relationships back to the parent models.
    workout = db.relationship(
        "Workout",
        back_populates="exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workouts"
    )

    @validates("sets", "reps", "duration_minutes")
    def validate_positive_values(self, key, value):
        if value is not None and (
            not isinstance(value, int)
            or isinstance(value, bool)
            or value <= 0
        ):
            raise ValueError(f"{key.capitalize()} must be a positive integer")

        return value

    def __repr__(self):
        return (
            f"<WorkoutExercise workout_id={self.workout_id} "
            f"exercise_id={self.exercise_id}>"
        )