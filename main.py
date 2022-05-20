import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from data.access.helpers.get_data import (
    get_distance_for_groups_daily,
    get_distance_sum_by_groups,
)
from core.core import refresh_stats
from data.access.helpers.users import get_top_n_user


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


if __name__ == "__main__":
    # app.run_server()
    # refresh_stats()
    print(get_top_n_user(5))
