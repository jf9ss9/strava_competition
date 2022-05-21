from data.models.models import Workouts
from data.access.database import session


def insert_workouts(workouts_json: dict) -> None:
    """
    Inserts each workout into the database from the response json.
    :param workouts_json: json returned by the strava list activities API endpoint
    """
    for workout in workouts_json:
        insert_workout(
            user_id=workout["athlete"]["id"],
            workout_type=workout["type"],
            workout_name=workout["name"],
            elapsed_time=workout["elapsed_time"],
            workout_date=workout["start_date"],
            distance=workout["distance"],
        )


def insert_workout(
    user_id: int,
    workout_type: str,
    distance: float,
    workout_name: str,
    elapsed_time: int,
    workout_date: str,
) -> None:
    """
    Inserts a single Workout object in the database.
    :param user_id: the user's id from the user table as integer
    :param workout_type: the workout's type (e.g: Run, Cycling, etc.)
    :param distance: the distance of the workout as float
    :param workout_name: the workout's name (e.g: Morning run)
    :param elapsed_time: elapsed time as integer
    :param workout_date: workout's start date as string
    """
    workout = Workouts(
        user_id=user_id,
        workout_type=workout_type,
        distance=distance,
        workout_name=workout_name,
        elapsed_time=elapsed_time,
        workout_date=workout_date,
    )

    session.add(workout)
    session.commit()
