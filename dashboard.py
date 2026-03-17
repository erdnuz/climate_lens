from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output

from climate_lens.config import DEFAULT_COUNTRIES, METRIC_LABELS, POLLUTANT_OPTIONS, THEME, TOP10_OPTIONS
from climate_lens.data.loader import load_datasets
from climate_lens.data.transform import aggregate_by_subregion, compute_global_kpis
from climate_lens.viz.figures import build_choropleth, build_pie_distribution, build_time_series, build_top10

datasets = load_datasets()
aq = datasets["aq"]
climate = datasets["climate"]
co2 = datasets["co2"]
co2_forecast = datasets["co2_forecast"]

all_countries = sorted(co2["country_name"].dropna().unique())
kpis = compute_global_kpis(co2, climate)

app = Dash(__name__)
app.title = "Climate Lens"

dark_style = {
    "backgroundColor": THEME["page_bg"],
    "color": THEME["font"],
    "font-family": "Arial, sans-serif",
    "padding": "20px",
    "overflowX": "hidden",
    "box-sizing": "border-box",
}

dropdown_style = {
    "marginBottom": "15px",
}

subregion_df = aggregate_by_subregion(co2, climate, aq)
table = dash_table.DataTable(
    columns=[
        {"name": col, "id": col, "type": "numeric"} if col != "Region" else {"name": col, "id": col}
        for col in subregion_df.columns
    ],
    data=subregion_df.fillna("-").to_dict("records"),
    sort_action="native",
    style_header={
        "backgroundColor": THEME["card_bg"],
        "color": THEME["font"],
        "fontWeight": "bold",
        "textAlign": "center",
        "borderBottom": "1px solid #2a2f3b",
    },
    style_cell={
        "backgroundColor": THEME["page_bg"],
        "color": THEME["font"],
        "textAlign": "center",
        "padding": "8px",
        "border": "none",
    },
    style_table={
        "overflowX": "auto",
        "width": "100%",
        "border": f"1px solid {THEME['border']}",
        "borderRadius": "8px",
        "marginTop": "20px",
    },
)
# ------------------------------
# Layout
# ------------------------------
# ------------------------------
# Layout
# ------------------------------
app.layout = html.Div(style=dark_style, children=[
    # KPI Cards
    # KPI Cards
    html.Div(style={"display": "flex", "gap": "20px", "margin-bottom": "20px", "justify-content": "center"}, children=[
        html.Div(style={"background": THEME["card_bg"], "padding": "20px", "border-radius": "8px",
                        "text-align": "center", "border": f"1px solid {THEME['border']}", "flex": "1"}, children=[
            "Global CO2 per Capita", html.Br(), html.B(f"{(kpis['co2_pc_latest'] * 1e3):.2f} T"),
            html.Br(), html.Span(f"Trend: {kpis['co2_pc_trend']:+.2f}%", style={"color": THEME["danger"] if kpis["co2_pc_trend"] > 0 else THEME["success"]})
        ]),
        html.Div(style={"background": THEME["card_bg"], "padding": "20px", "border-radius": "8px",
                        "text-align": "center", "border": f"1px solid {THEME['border']}", "flex": "1"}, children=[
            "Total CO2", html.Br(), html.B(f"{(kpis['co2_total_latest'] / 1e6):.2f} Gt"),
            html.Br(), html.Span(f"Trend: {kpis['co2_total_trend']:+.2f}%", style={"color": THEME["danger"] if kpis["co2_total_trend"] > 0 else THEME["success"]})
        ]),
        html.Div(style={"background": THEME["card_bg"], "padding": "20px", "border-radius": "8px",
                        "text-align": "center", "border": f"1px solid {THEME['border']}", "flex": "1"}, children=[
            "Global Avg Max Temperature", html.Br(), html.B(f"{kpis['temp_max_latest']:.2f} C"),
            html.Br(), html.Span(f"Trend: {kpis['temp_max_trend']:+.2f}%", style={"color": THEME["danger"] if kpis["temp_max_trend"] > 0 else THEME["success"]})
        ])
    ]),

    # ------------------------------
    # Row 1: Time series & AQ choropleth
    # ------------------------------
    html.Div(style={"display": "flex", "gap": "20px", "margin-bottom": "20px", "justify-content": "center", "background": THEME["card_bg"],
                        "padding": "10px", "border-radius": "8px", "border": f"1px solid {THEME['border']}"}, children=[
        html.Div(style={"flex": "1", "min-width": "300px", "max-width": "700px"}, children=[
            html.Label("Select countries:", style={"color": THEME["font"]}),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': c, 'value': c} for c in all_countries],
                value=DEFAULT_COUNTRIES,
                multi=True,
                searchable=True,
                style=dropdown_style,
                clearable=False,
                className='cl-select',
            ),
            html.Label("Select metric:", style={"color": THEME["font"], "margin-top": "10px"}),
            dcc.Dropdown(
                id='metric-dropdown',
                options=[{'label': v, 'value': k} for k, v in METRIC_LABELS.items()],
                value='co2',
                searchable=False,
                clearable=False,
                style=dropdown_style,
                className='cl-select',
            ),
            dcc.Graph(
                id='ts-graph', 
                style={'height': '400px', 'margin-top': '10px'}, 
                config={
                "displayModeBar": True,
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "select2d",
                    "lasso2d",
                    "autoScale2d",
                    "toggleSpikelines",
                    "hoverClosestCartesian",
                    "hoverCompareCartesian",
                    "toImage", 
                    "zoom2d",
                ],
                "modeBarButtonsToAdd": [
                    "pan2d",

                ],
            }),
        ]),
        html.Div(style={"flex": "1", "min-width": "300px", "max-width": "600px"}, children=[
            html.Label("Select Pollutant Variable:", style={"color": THEME["font"]}),
            dcc.Dropdown(
                id='aq-dropdown',
                options=[{"label": k, "value": k} for k in POLLUTANT_OPTIONS],
                value="Air Quality Index",
                searchable=False,
                clearable=False,
                style=dropdown_style,
                className='cl-select',
            ),
            dcc.Graph(id='choro-graph', style={'height': '500px', 'margin-top': '10px'}, config={
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            "select2d",
            "lasso2d",
            "autoScale2d",
            "resetScale2d",
            "toggleSpikelines",
            "hoverClosestCartesian",
            "hoverCompareCartesian",
            "toImage"
        ],
        "modeBarButtonsToAdd": [
            "pan2d",
            "reset2d"
        ],
    })
        ])
    ]),

    # ------------------------------
# Row 2: Pie & Top 10 Bar charts
# ------------------------------
html.Div(style={"display": "flex", "gap": "20px", "margin-bottom": "20px", "justify-content": "center", "background": THEME["card_bg"],
                    "padding": "10px", "border-radius": "8px", "border": f"1px solid {THEME['border']}"}, children=[
    # Pie Chart
    html.Div(style={'flex': '1', 'min-width': '300px', 'max-width': '600px'}, children=[
        dcc.Graph(
            id='pie-graph',
            config={"displayModeBar": False},

            style={'height': '600px', 'width': '100%'},  # increase height
        )
    ]),

    # Top 10 Bar Chart
    html.Div(style={'flex': '1', 'min-width': '300px', 'max-width': '600px'}, children=[
    html.Div(style={'display': 'flex', 'gap': '10px', 'margin-bottom': '15px'}, children=[
        html.Div(style={'flex': '1'}, children=[
            html.Label("Select Metric:", style={"color": THEME["font"]}),
            dcc.Dropdown(
                id='top10-dropdown',
                options=TOP10_OPTIONS,
                value='co2',
                searchable=False,
                clearable=False,
                style=dropdown_style,
                className='cl-select',
            )
        ]),
        html.Div(style={'flex': '1'}, children=[
            html.Label("Select Ranking Order:", style={"color": THEME["font"]}),
            dcc.Dropdown(
                id='top10-order-dropdown',
                options=[
                    {'label': 'Highest', 'value': 'best'},
                    {'label': 'Lowest', 'value': 'worst'}
                ],
                value='best',
                searchable=False,
                clearable=False,
                style=dropdown_style,
                className='cl-select',
            )
        ])
    ]),
    dcc.Graph(id='top10-graph', config={"displayModeBar": False}, style={'height': '500px'})
])

]),


    # ------------------------------
    # Row 3: Table
    # ------------------------------
    html.Div(style={'display': 'flex', 'gap': '20px', 'margin-bottom': '20px', 'justify-content': 'center'}, children=[
        html.Div(style={'flex': '1', 'min-width': '300px', 'background': THEME["card_bg"],
                        'padding': '10px', 'border-radius': '8px', 'border': f"1px solid {THEME['border']}"}, children=[
            table
        ])
    ])
])

@app.callback(
    Output('ts-graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('metric-dropdown', 'value')
)
def update_ts(selected_countries, selected_metric):
    return build_time_series(selected_countries, selected_metric, co2_forecast, climate)

@app.callback(
    Output('pie-graph', 'figure'),
    Input('metric-dropdown', 'value')
)
def update_pie(metric):
    return build_pie_distribution(co2)




@app.callback(
    Output('top10-graph', 'figure'),
    Input('top10-dropdown', 'value'),
    Input('top10-order-dropdown', 'value')
)
def update_top10(metric, order):
    return build_top10(metric, order, co2, climate, aq)




@app.callback(
    Output('choro-graph', 'figure'),
    Input('aq-dropdown', 'value')
)
def update_choro(selected_var):
    return build_choropleth(selected_var, aq)

# ------------------------------
# Run server
# ------------------------------
if __name__ == "__main__":
    app.run(debug=False)
