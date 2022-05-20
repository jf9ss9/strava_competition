from data.models.models import Users
from data.access.database import session


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
