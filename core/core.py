import datetime
import requests
import time
from data.access.helpers.tokens import (
    refresh_expired_tokens,
    get_latest_token_update,
    get_tokens,
)
from data.access.helpers.workouts import insert_workouts


def get_activities(after: int) -> None:
    """
    Gets the activities from the API endpoint for each user and saves it in the database.
    :param after: list the activities after a unix timestamp, integer
    """
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
            print(result.json())


def get_new_workouts() -> None:
    """
    Gets the latest token update and if it's not the current date,
    then calls the get_activities after the last token update date.
    """
    last_date = get_latest_token_update()
    if datetime.datetime.now().strftime("%Y-%m-%d") == last_date.strftime("%Y-%m-%d"):
        return
    last_date_unix = int(time.mktime(last_date.timetuple()))
    get_activities(after=last_date_unix)


def refresh_stats() -> None:
    """
    Main function which is scheduled. First refreshes the expired tokens,
    then gets the new workouts.
    """
    refresh_expired_tokens()
    get_new_workouts()
