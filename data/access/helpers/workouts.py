from data.models.models import Workouts
from data.access.database import session


def insert_workout(user_id: int, workout_type: str, distance: float,
                   workout_name: str, elapsed_time: int) -> None:
    workout = Workouts(user_id=user_id, workout_type=workout_type, distance=distance,
                       workout_name=workout_name, elapsed_time=elapsed_time)

    session.add(Workouts)
    session.commit()
