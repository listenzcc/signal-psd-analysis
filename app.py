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
import pandas as pd
import plotly.express as px

from dash import Dash, html, dcc, callback, Output, Input

from load_data import ch_names
from analysis import window_names, compute_psd


# %%
# Dash setup and layout
external_stylesheets = [
    "/assets/style.css",
]
app = Dash(__name__, external_scripts=external_stylesheets)

channel_selector = html.Div(
    [
        html.H2(children="Channel Name:"),
        dcc.Dropdown(ch_names, ch_names[0], id="dropdown-selection-1"),
    ]
)

welch_options = html.Div(
    [
        html.Div(
            [
                html.H2(children="Welch Options A:"),
                dcc.Dropdown(
                    window_names,
                    "hann" if "hann" in window_names else window_names[0],
                    id="dropdown-selection-a-2",
                ),
                html.H3(children="nperseg"),
                dcc.Slider(min=100, max=500, value=200, id="slider-a-1"),
                html.H3(children="noverlap_ratio"),
                dcc.Slider(min=0.2, max=0.8, value=0.2, id="slider-a-2"),
            ],
            className="narrowDiv",
        ),
        html.Div(
            [
                html.H2(children="Welch Options B:"),
                dcc.Dropdown(
                    window_names,
                    "hann" if "hann" in window_names else window_names[0],
                    id="dropdown-selection-b-2",
                ),
                html.H3(children="nperseg"),
                dcc.Slider(min=100, max=500, value=200, id="slider-b-1"),
                html.H3(children="noverlap_ratio"),
                dcc.Slider(min=0.2, max=0.8, value=0.8, id="slider-b-2"),
            ],
            className="narrowDiv",
        ),
    ],
    className="flexLayout",
)

graph_a = html.Div(
    [
        html.H2(children="Graph A"),
        dcc.Graph(id="graph-content-a"),
    ],
    className="wideDiv",
)

graph_b = html.Div(
    [
        html.H2(children="Graph B"),
        dcc.Graph(id="graph-content-b"),
    ],
    className="wideDiv",
)

graph_c = html.Div(
    [
        html.H2(children="Graph Diff(A, B)"),
        dcc.Graph(id="graph-content-c"),
    ],
    className="wideDiv",
)

graph_d = html.Div(
    [
        html.H2(children="Graph Diff(A, B) mean"),
        dcc.Graph(id="graph-content-d"),
    ],
    className="wideDiv",
)

graph = html.Div([graph_a, graph_b, graph_c, graph_d], className="flexLayout")

app.layout = html.Div(
    [
        html.H1(children="Automatic PSD analysis", style={"textAlign": "center"}),
        channel_selector,
        graph,
        welch_options,
    ]
)

# %% ---- 2024-03-04 ------------------------
# Function and class


def compute_psd_and_fig(ch_name, window_name, nperseg, noverlap_ratio):
    noverlap = int(nperseg * noverlap_ratio)
    f, Pxx_den, df = compute_psd(window_name, nperseg=nperseg, noverlap=noverlap)
    title = f"Welch output: {ch_name}, {window_name} | {nperseg} | {noverlap}"
    select = df[df.ch_name == ch_name]
    fig = px.scatter(
        select,
        x="freq",
        y="value",
        log_y=True,
        range_y=[1e-20, 1e-10],
        color="epoch_idx",
        title=title,
    )
    return df, fig


@callback(
    Output("graph-content-a", "figure"),
    Output("graph-content-b", "figure"),
    Output("graph-content-c", "figure"),
    Output("graph-content-d", "figure"),
    # --------------------
    Input("dropdown-selection-1", "value"),
    # --------------------
    Input("dropdown-selection-a-2", "value"),
    Input("slider-a-1", "value"),
    Input("slider-a-2", "value"),
    # --------------------
    Input("dropdown-selection-b-2", "value"),
    Input("slider-b-1", "value"),
    Input("slider-b-2", "value"),
)
def update_graph(
    ch_name,
    window_name_a,
    nperseg_a,
    noverlap_ratio_a,
    window_name_b,
    nperseg_b,
    noverlap_ratio_b,
):
    df_a, fig_a = compute_psd_and_fig(
        ch_name, window_name_a, nperseg_a, noverlap_ratio_a
    )
    df_b, fig_b = compute_psd_and_fig(
        ch_name, window_name_b, nperseg_b, noverlap_ratio_b
    )

    # --------------------
    df_1 = df_a.copy()
    df_2 = df_b.copy()
    df = df_1.merge(df_2, on=["epoch_idx", "ch_name", "freq"])
    df["value_diff"] = df["value_x"] - df["value_y"]
    df["value_diff"] = df["value_diff"].abs()

    fig_c = px.scatter(
        df,
        x="freq",
        y="value_diff",
        log_y=True,
        range_y=[1e-20, 1e-10],
        color="epoch_idx",
        title="Diff",
    )

    # --------------------

    def _compute(df_1, df_2, segment="1-14"):
        group1 = df_1.groupby("freq")
        df_1 = group1.mean("value")
        df_1["freq"] = df_1.index
        df_1.index.name = None

        group2 = df_2.groupby("freq")
        df_2 = group2.mean("value")
        df_2["freq"] = df_2.index
        df_2.index.name = None

        df = df_1.merge(df_2, on=["epoch_idx", "freq"])
        df["value_diff"] = df["value_x"] - df["value_y"]
        df["value_diff"] = df["value_diff"].abs()
        df["segment"] = segment

        return df

    df_1 = df_a[df_a.epoch_idx < 14].copy()
    df_2 = df_b[df_b.epoch_idx < 14].copy()
    df1 = _compute(df_1, df_2, segment="1-14")

    df_1 = df_a[df_a.epoch_idx > 14].copy()
    df_2 = df_b[df_b.epoch_idx > 14].copy()
    df2 = _compute(df_1, df_2, segment="15-28")

    df = pd.concat([df1, df2])

    print(df)

    fig_d = px.scatter(
        df,
        x="freq",
        y="value_diff",
        color="segment",
        log_y=True,
        range_y=[1e-20, 1e-10],
        # color="epoch_idx",
        title="Diff (mean)",
    )

    return fig_a, fig_b, fig_c, fig_d


# %% ---- 2024-03-04 ------------------------
# Play ground
if __name__ == "__main__":
    app.run("0.0.0.0", 8050, debug=True)


# %% ---- 2024-03-04 ------------------------
# Pending


# %% ---- 2024-03-04 ------------------------
# Pending
