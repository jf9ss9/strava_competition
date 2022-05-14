from data.models.models import Users
from data.access.database import session


def insert_user(user_id: int, group_id: int = 1) -> None:
    """
    Insert a user in database if it doesn't exist yet.
    :param user_id: user_id from the User table
    :param group_id: group_id from the User table
    """
    if session.query(Users).filter(Users.id == user_id).all() is not None:
        return
    user = Users(user_id=user_id, group_id=group_id)

    session.add(user)
    session.commit()
