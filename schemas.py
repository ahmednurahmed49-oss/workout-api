from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    date = fields.Date(load_default=None, allow_none=True)


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    description = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )
    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )
    duration_minutes = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1)
    )

    @validates_schema
    def validate_exercise_details(self, data, **kwargs):
        if not any(
            data.get(field) is not None
            for field in ("sets", "reps", "duration_minutes")
        ):
            raise ValidationError(
                "Provide at least one of sets, reps, or duration_minutes."
            )