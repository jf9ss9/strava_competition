from data.models.models import Groups
from data.access.database import session


def insert_group(group_name: str) -> None:
    """
    Insert a group in the database with the given group name if it's not present yet.
    :param group_name: group name as string
    """
    if session.query(Groups).filter(Groups.group_name == group_name).all() is not None:
        return
    group = Groups(group_name=group_name)

    session.add(group)
    session.commit()
