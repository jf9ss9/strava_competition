import pandas as pd
from ..database import engine


def get_distance_sum_by_groups() -> pd.DataFrame:
    """
    Function which returns the total distance for each group type.
    :return: dataframe containing the data
    """
    df = pd.read_sql(
        "select g.group_name, sum(w.distance) as summa from (users u join "
        '"groups" g on u.group_id=g.id) join workouts w '
        "on w.user_id=u.id group by g.group_name order by summa",
        engine,
    )
    return df


def get_distance_for_groups_daily() -> pd.DataFrame:
    """
    Function which returns the distance for each date for each group type and the cumulative distance for each group.
    :return: dataframe containing the data
    """
    df = pd.read_sql(
        'select g.group_name, w.workout_date, sum(w.distance) as distance from (users u join "groups" g '
        "on u.group_id=g.id) join workouts w on w.user_id=u.id "
        "group by g.group_name, w.workout_date order by w.workout_date",
        engine,
    )
    df["cumulative_distance"] = df.groupby(["group_name"])["distance"].cumsum()
    return df
