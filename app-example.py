"""
File: app.py
Author: Chuncheng Zhang
Date: 2024-03-04
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Dash app for analysis

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""

# %% ---- 2024-03-04 ------------------------
# Requirements and constants
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(children="Title of Dash App", style={"textAlign": "center"}),
        dcc.Dropdown(df.country.unique(), "Canada", id="dropdown-selection"),
        dcc.Graph(id="graph-content"),
    ]
)


@callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff, x="year", y="pop")


if __name__ == "__main__":
    app.run(debug=True)

# %% ---- 2024-03-04 ------------------------
# Function and class


# %% ---- 2024-03-04 ------------------------
# Play ground


# %% ---- 2024-03-04 ------------------------
# Pending


# %% ---- 2024-03-04 ------------------------
# Pending
