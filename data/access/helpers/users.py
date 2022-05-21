from data.models.models import Users, Workouts
from data.access.database import session
from sqlalchemy import func, desc


def insert_user(user_id: int, name: str, group_id: int = 1) -> None:
    """
    Insert a user in database if it doesn't exist yet.
    :param name: Name of the user as string
    :param user_id: user_id from the User table
    :param group_id: group_id from the User table
    """
    if len(session.query(Users).filter(Users.user_id == user_id).all()) != 0:
        return
    user = Users(user_id=user_id, group_id=group_id, name=name)

    session.add(user)
    session.commit()


def get_top_n_user(top_n: int) -> list[Users]:
    """
    Returns the top n users by total distance.
    :param top_n: num of top users as integer
    :return: list containing at most the top n Users objects
    """
    users = (
        session.query(Users.user_id, func.sum(Workouts.distance).label("distance"))
        .join(Workouts, Users.id == Workouts.user_id)
        .group_by(Users.user_id)
        .order_by(desc("distance"))
        .all()
    )
    return users[:top_n]
