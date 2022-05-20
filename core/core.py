import datetime

import requests
import time
from datetime import timedelta
import random
from data.access.helpers.tokens import (
    refresh_tokens,
    get_latest_update,
    get_tokens,
)
from data.access.helpers.workouts import insert_workouts


def get_activities(after: int) -> None:
    for token in get_tokens():
        headers = {"Authorization": f"Bearer {token.access_token}"}
        params = {"after": after}
        result = requests.get(
            url="https://www.strava.com/api/v3/athlete/activities",
            headers=headers,
            params=params,
        )
        if result.status_code == 200:
            insert_workouts(result.json())
        else:
            print("BAD REQUEST")


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def get_new_workouts() -> None:
    last_date = get_latest_update()
    if datetime.datetime.now().strftime("%Y-%m-%d") == last_date.strftime("%Y-%m-%d"):
        return
    last_date_unix = int(time.mktime(last_date.timetuple()))
    get_activities(after=last_date_unix)


def refresh_stats() -> None:
    """
    Main
    :return:
    """
    refresh_tokens()
    get_new_workouts()
