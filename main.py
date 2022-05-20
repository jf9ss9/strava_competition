import json
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import requests
import random
from datetime import timedelta, datetime
from data.access.helpers.get_data import (
    get_distance_for_groups_daily,
    get_distance_sum_by_groups,
)

app = dash.Dash(__name__)


def line_plot():
    df = get_distance_for_groups_daily()
    fig = px.line(df, x="workout_date", y="cumulative_distance", color="group_name")
    return fig


def bar_plot():
    df = get_distance_sum_by_groups()
    fig = px.bar(df, x="group_name", y="summa")
    return fig


app.layout = html.Div(
    id="parent",
    children=[
        html.H1(
            id="H1",
            children="Team contest",
            style={"textAlign": "center", "marginTop": 40, "marginBottom": 40},
        ),
        dcc.Graph(id="line_plot", figure=line_plot()),
        html.H1(
            id="H11",
            children="Team contest bar plot",
            style={"textAlign": "center", "marginTop": 40, "marginBottom": 40},
        ),
        dcc.Graph(id="bar_plot", figure=bar_plot()),
    ],
)


def get_activities():
    token = "e6cc95c23bdcfe1fe371cbd2f582e47ea0a6c064"
    headers = {"Authorization": f"Bearer {token}"}
    result = requests.get(
        url="https://www.strava.com/api/v3/athlete/activities", headers=headers
    )
    if result.status_code == 200:
        print(json.dumps(result.json(), indent=4))


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


if __name__ == "__main__":
    app.run_server()
