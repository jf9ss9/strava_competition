import datetime
import time
import json
import requests
from .users import insert_user
from data.access.database import session
from data.models.models import Users, Tokens

CLIENT_SECRET = "f84c85e32c0a329a2995dd5e2beed8296218df6a"
CLIENT_ID = 84444


def refresh_expired_tokens() -> None:
    """
    Refresh tokens for each expired token.
    """
    expired_tokens = (
        session.query(Tokens).filter(Tokens.expires_at >= int(time.time())).all()
    )

    for token in expired_tokens:
        refresh_tokens(token)


def refresh_tokens(token: Tokens) -> None:
    """
    Refreshes the tokens for the requested user.
    :param token: token belonging to user with user_id
    """
    user_id = session.query(Users).filter(Users.id == token.user_id).first().id
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": token.refresh_token,
    }
    result = requests.post(
        url="https://www.strava.com/api/v3/oauth/token", params=params
    )
    if result.status_code == 200:
        update_tokens(user_id, result.json())
    else:
        print("ERROR: BAD REQUEST")
        print(result.json())


def update_tokens(user_id: int, result_json: dict) -> None:
    """
    Updates the tokens of the specific user.
    :param user_id: The id of the user whose token will be updated
    :param result_json: The result json returned by the strava oauth token API
    """
    session.query(Tokens).filter(Tokens.user_id == user_id).update(
        {
            Tokens.refresh_token: result_json["refresh_token"],
            Tokens.access_token: result_json["access_token"],
            Tokens.expires_in: result_json["expires_in"],
            Tokens.expires_at: result_json["expires_at"],
        }
    )

    session.commit()


def exchange_code_for_token(code: str) -> None:
    """
    Exchanges the code given as parameter for tokens by calling the oath token API.
    :param code: the code which will be exchanged for tokens
    """
    params = {
        "client_id": 84444,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
    }
    result = requests.post(
        url="https://www.strava.com/api/v3/oauth/token", params=params
    )

    if result.status_code == 200:
        print(json.dumps(result.json(), indent=4))
        insert_token(result.json())
    else:
        print("ERROR: BAD REQUEST")


def insert_token(result_json: dict) -> None:
    """
    Inserts a token record in the database based on the request's result/
    :param result_json: the request's result as json
    """
    athlete_info = result_json["athlete"]
    # TODO: insert group too
    insert_user(user_id=athlete_info["id"], name="Edy")
    user_id = (
        session.query(Users.id).filter(Users.user_id == athlete_info["id"]).first()[0]
    )
    token = Tokens(
        user_id=user_id,
        access_token=result_json["access_token"],
        refresh_token=result_json["refresh_token"],
        expires_in=result_json["expires_in"],
        expires_at=result_json["expires_at"],
    )
    session.add(token)
    session.commit()


def get_latest_update() -> datetime.datetime:
    last_date = (
        session.query(Tokens)
        .filter(Tokens.updated_at.is_not(None))
        .order_by(Tokens.updated_at.desc())
        .first()
        .updated_at
    )
    return last_date


def get_tokens() -> list[Tokens]:
    tokens = session.query(Tokens).all()
    return tokens


def get_user_from_token(token: Tokens) -> Users:
    user = session.query(Users).filter(Users.id == token.user_id).first()
    return user
