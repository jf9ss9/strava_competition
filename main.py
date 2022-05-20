import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from data.access.helpers.get_data import (
    get_distance_for_groups_daily,
    get_distance_sum_by_groups,
    get_top_n_users_df,
)
from core.core import refresh_stats



app = dash.Dash(__name__)


def line_plot():
    df = get_distance_for_groups_daily()
    fig = px.line(df, x="workout_date", y="cumulative_distance", color="group_name")
    return fig


def bar_plot():
    df = get_distance_sum_by_groups()
    fig = px.bar(df, x="group_name", y="summa")
    return fig


def bar_plot2():
    df = get_top_n_users_df()
    fig = px.bar(df, x="user_id", y="distance")
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
        html.H1(
            id="H12",
            children="Team contest bar plot2",
            style={"textAlign": "center", "marginTop": 40, "marginBottom": 40},
        ),
        dcc.Graph(id="bar_plot2", figure=bar_plot2()),
    ],
)


if __name__ == "__main__":
    app.run_server()
