from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# ------------------------------
# Load data
# ------------------------------
aq = pd.read_csv("data/aq_imputed.csv")
countries = pd.read_csv("data/country_map.csv")
climate = pd.read_csv("data/climate.csv")
co2 = pd.read_csv("data/co2.csv")

for df in [aq, climate, co2, countries]:
    df["country_code"] = df["country_code"].str.upper()

aq = aq.merge(countries, on="country_code", how="left")
climate = climate.merge(countries, on="country_code", how="left")
co2 = co2.merge(countries, on="country_code", how="left")

all_countries = sorted(co2["country_name"].unique())
metric_labels = {
    "value": "CO₂ Total (Mt)",
    "co2_per_capita": "CO₂ per Capita (t/person)",
    "temp_min": "Yearly Minimum Temperature (°C)",
    "temp_max": "Yearly Maximum Temperature (°C)",
    "R1": "Annual Average Rainfall (mm)"
}


climate_yearly = climate.groupby("year").agg({
    "temp_min": "min",
    "temp_max": "max",
    "R1": "mean"
}).reset_index()

# Compute most recent year
latest_year = co2["year"].max()
prev_year = latest_year - 1
co2["population"] = co2["value"] / co2["co2_per_capita"]

# Latest year
co2_latest = co2[co2["year"] == latest_year]
co2_prev = co2[co2["year"] == prev_year]

# Global Avg CO2 per Capita
co2_pc_latest = co2_latest["value"].sum() / co2_latest["population"].sum()
co2_pc_prev = co2_prev["value"].sum() / co2_prev["population"].sum()
co2_pc_trend = ((co2_pc_latest - co2_pc_prev) / co2_pc_prev * 100) if co2_pc_prev else 0

# Total CO2
co2_total_latest = co2_latest["value"].sum()
co2_total_prev = co2_prev["value"].sum()
co2_total_trend = ((co2_total_latest - co2_total_prev) / co2_total_prev * 100) if co2_total_prev else 0

# Global Avg Max Temperature
temp_max_latest = climate[climate["year"] == latest_year]["temp_max"].mean()
temp_max_prev = climate[climate["year"] == prev_year]["temp_max"].mean()
temp_max_trend = ((temp_max_latest - temp_max_prev) / temp_max_prev * 100) if temp_max_prev else 0




from dash import dash_table


def aggregate_by_subregion():
    # Latest year for timeseries
    latest_year_co2 = co2["year"].max()
    latest_year_climate = climate["year"].max()
    latest_year_aq = aq["year"].max() if "year" in aq.columns else None

    # CO2: latest year
    co2_latest = co2[co2["year"] == latest_year_co2]
    co2_grouped = co2_latest.groupby("sub_region").agg({
        "value": "mean",
        "co2_per_capita": "mean"
    }).reset_index()

    # Climate: latest year
    climate_latest = climate[climate["year"] == latest_year_climate]
    climate_grouped = climate_latest.groupby("sub_region").agg({
        "temp_min": "mean",
        "temp_max": "mean",
        "R1": "mean"
    }).reset_index()

    # AQ: latest year
    if latest_year_aq:
        aq_latest = aq[aq["year"] == latest_year_aq]
    else:
        aq_latest = aq.copy()
    aq_grouped = aq_latest.groupby("sub_region").agg({
        "aq": "mean",
        "PM2.5": "mean",
        "PM10": "mean"
    }).reset_index()

    # Merge all
    df = co2_grouped.merge(climate_grouped, on="sub_region", how="outer")
    df = df.merge(aq_grouped, on="sub_region", how="outer")

    df['co2_per_capita'] = df['co2_per_capita'] * 1000
    df['value'] = df['value'] / 1000
    
    # Round numeric columns to 2 decimals
    for col in df.columns:
        if col != "sub_region":
            df[col] = df[col].round(2)

    

    # Rename columns for display
    df = df.rename(columns={
        "sub_region": "Sub-Region",
        "value": "CO₂ Total (Mt)",
        "co2_per_capita": "CO₂ per Capita (T)",
        "temp_min": "Min Temp (°C)",
        "temp_max": "Max Temp (°C)",
        "R1": "Avg Rainfall (mm)",
        "aq": "AQ Index",
        "PM2.5": "PM2.5",
        "PM10": "PM10"
    })
    return df

# Create styled DataTable
subregion_df = aggregate_by_subregion()
table = dash_table.DataTable(
    columns=[{"name": col, "id": col, "type": "numeric"} if col != "Sub-Region" else {"name": col, "id": col} for col in subregion_df.columns],
    data=subregion_df.to_dict('records'),
    sort_action="native",
    style_header={
        'backgroundColor': '#1a1d24',
        'color': '#e0e6ed',
        'fontWeight': 'bold',
        'textAlign': 'center',
        'borderBottom': '1px solid #2a2f3b'
    },
    style_cell={
        'backgroundColor': '#0f1116',
        'color': '#e0e6ed',
        'textAlign': 'center',
        'padding': '8px',
        'border': 'none'
    },
    style_table={
        'overflowX': 'auto',
        'width': '100%',
        'border': '1px solid #1f2937',
        'borderRadius': '8px',
        'marginTop': '20px'
    }
)


# ------------------------------
# Initialize Dash app
# ------------------------------
app = Dash(__name__)
app.title = "Environmental Dashboard"

# ------------------------------
# Dark theme layout
# ------------------------------
dark_style = {
    'backgroundColor': '#0f1116',
    'color': '#e0e6ed',
    'font-family': 'Arial, sans-serif',
    'padding': '20px',
    'overflowX': 'hidden',  # prevent horizontal scroll
    'box-sizing': 'border-box'
}

dropdown_style = {
    'backgroundColor': '#1a1d24',
    'color': '#e0e6ed',
    'border': '1px solid #2a2f3b',
    'border-radius': '4px',
    'height': '35px',
    'margin-bottom': '15px'
}
# ------------------------------
# Layout
# ------------------------------
# ------------------------------
# Layout
# ------------------------------
app.layout = html.Div(style=dark_style, children=[
    # KPI Cards
    # KPI Cards
    html.Div(style={'display': 'flex', 'gap': '20px', 'margin-bottom': '20px', 'justify-content': 'center'}, children=[
        html.Div(style={'background': '#1a1d24', 'padding': '20px', 'border-radius': '8px',
                        'text-align': 'center', 'border': '1px solid #1f2937', 'flex': '1'}, children=[
            "Global Avg CO₂ per Capita", html.Br(), html.B(f"{(co2_pc_latest*1e3):.2f} T"),
            html.Br(), html.Span(f"Trend: {co2_pc_trend:+.2f}%", style={'color': "#9b9b9b"})
        ]),
        html.Div(style={'background': '#1a1d24', 'padding': '20px', 'border-radius': '8px',
                        'text-align': 'center', 'border': '1px solid #1f2937', 'flex': '1'}, children=[
            "Total CO₂", html.Br(), html.B(f"{(co2_total_latest / 1e6):.2f} Gt"),
            html.Br(), html.Span(f"Trend: {co2_total_trend:+.2f}%", style={'color': "#9b9b9b"})
        ]),
        html.Div(style={'background': '#1a1d24', 'padding': '20px', 'border-radius': '8px',
                        'text-align': 'center', 'border': '1px solid #1f2937', 'flex': '1'}, children=[
            "Global Avg Max Temperature", html.Br(), html.B(f"{temp_max_latest:.2f} °C"),
            html.Br(), html.Span(f"Trend: {temp_max_trend:+.2f}%", style={'color': "#9b9b9b"})
        ])
    ]),

    # ------------------------------
    # Row 1: Time series & AQ choropleth
    # ------------------------------
    html.Div(style={'display': 'flex', 'gap': '20px', 'margin-bottom': '20px', 'justify-content': 'center'}, children=[
        html.Div(style={'flex': '1', 'min-width': '300px', 'max-width': '600px', 'background': '#1a1d24',
                        'padding': '10px', 'border-radius': '8px', 'border': '1px solid #1f2937'}, children=[
            html.Label("Select countries:", style={'color': '#e0e6ed'}),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': c, 'value': c} for c in all_countries],
                value=["Canada", "United States"],
                multi=True,
                style=dropdown_style
            ),
            html.Label("Select metric:", style={'color': '#e0e6ed', 'margin-top': '10px'}),
            dcc.Dropdown(
                id='metric-dropdown',
                options=[{'label': v, 'value': k} for k, v in metric_labels.items()],
                value='value',
                style=dropdown_style
            ),
            dcc.Graph(id='ts-graph', style={'height': '500px', 'margin-top': '10px'})
        ]),
        html.Div(style={'flex': '1', 'min-width': '300px', 'max-width': '600px', 'background': '#1a1d24',
                        'padding': '10px', 'border-radius': '8px', 'border': '1px solid #1f2937'}, children=[
            html.Label("Select AQ Variable:", style={'color': '#e0e6ed'}),
            dcc.Dropdown(
                id='aq-dropdown',
                options=[{'label': k, 'value': k} for k in ["AQ Index", "PM2.5", "PM10"]],
                value="AQ Index",
                style=dropdown_style
            ),
            dcc.Graph(id='choro-graph', style={'height': '500px', 'margin-top': '10px'})
        ])
    ]),

    # ------------------------------
# Row 2: Pie & Top 10 Bar charts
# ------------------------------
html.Div(style={'display': 'flex', 'gap': '20px', 'margin-bottom': '20px', 'justify-content': 'center'}, children=[
    # Pie Chart
    html.Div(style={'flex': '1', 'min-width': '300px', 'max-width': '600px', 'background': '#1a1d24',
                    'padding': '10px', 'border-radius': '8px', 'border': '1px solid #1f2937'}, children=[
        dcc.Graph(
            id='pie-graph',
            style={'height': '400px'}
        )
    ]),

    # Top 10 Bar Chart
    html.Div(style={'flex': '1', 'min-width': '300px', 'max-width': '600px', 'background': '#1a1d24',
                'padding': '10px', 'border-radius': '8px', 'border': '1px solid #1f2937'}, children=[
    html.Div(style={'display': 'flex', 'gap': '10px', 'margin-bottom': '15px'}, children=[
        html.Div(style={'flex': '1'}, children=[
            html.Label("Select Metric:", style={'color': '#e0e6ed'}),
            dcc.Dropdown(
                id='top10-dropdown',
                options=[
                    {'label': 'Air Quality Index', 'value': 'aq'},
                    {'label': 'PM2.5', 'value': 'PM2.5'},
                    {'label': 'PM10', 'value': 'PM10'},
                    {'label': 'Annual Rainfall', 'value': 'R1'},
                    {'label': 'CO₂ per Capita', 'value': 'co2_per_capita'},
                    {'label': 'Total CO₂', 'value': 'value'}
                ],
                value='value',
                style=dropdown_style
            )
        ]),
        html.Div(style={'flex': '1'}, children=[
            html.Label("Select Ranking Order:", style={'color': '#e0e6ed'}),
            dcc.Dropdown(
                id='top10-order-dropdown',
                options=[
                    {'label': 'Top 10 (Best)', 'value': 'best'},
                    {'label': 'Top 10 (Worst)', 'value': 'worst'}
                ],
                value='best',
                style=dropdown_style
            )
        ])
    ]),
    dcc.Graph(id='top10-graph', style={'height': '500px'})
])

]),


    # ------------------------------
    # Row 3: Table
    # ------------------------------
    html.Div(style={'display': 'flex', 'gap': '20px', 'margin-bottom': '20px', 'justify-content': 'center'}, children=[
        html.Div(style={'flex': '1', 'min-width': '300px', 'max-width': '1200px', 'background': '#1a1d24',
                        'padding': '10px', 'border-radius': '8px', 'border': '1px solid #1f2937'}, children=[
            table
        ])
    ])
])


forecast_start = 2010

@app.callback(
    Output('ts-graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('metric-dropdown', 'value')
)
def update_ts(selected_countries, selected_metric):
    fig = go.Figure()

    for country in selected_countries:
        if selected_metric in ["value", "co2_per_capita"]:
            # CO2 metrics per country
            d = co2[co2["country_name"] == country].sort_values("year")

            # Solid line for years before forecast
            d_solid = d[d["year"] < forecast_start]
            if not d_solid.empty:
                fig.add_trace(go.Scatter(
                    x=d_solid["year"],
                    y=d_solid[selected_metric],
                    mode='lines+markers',
                    name=country,
                    line=dict(dash='solid')
                ))

            # Dashed line for years >= forecast_start
            d_dashed = d[d["year"] >= forecast_start]
            if not d_dashed.empty:
                fig.add_trace(go.Scatter(
                    x=d_dashed["year"],
                    y=d_dashed[selected_metric],
                    mode='lines+markers',
                    name=f"{country}*",
                    showlegend=True,  # avoid duplicate legend
                    line=dict(dash='dash')
                ))

        else:
            # Climate metrics per country (no dashed line)
            d = climate[climate["country_name"] == country].groupby("year").agg({
                "temp_min": "min",
                "temp_max": "max",
                "R1": "mean"
            }).reset_index()
            fig.add_trace(go.Scatter(
                x=d["year"],
                y=d[selected_metric],
                mode='lines+markers',
                name=country,
                line=dict(dash='solid')
            ))

    fig.update_layout(
        paper_bgcolor="#1a1d24",
        plot_bgcolor="#1a1d24",
        font=dict(color="#e0e6ed"),
        xaxis_title="Year",
        yaxis_title=metric_labels[selected_metric]
    )

    return fig

@app.callback(
    Output('pie-graph', 'figure'),
    Input('metric-dropdown', 'value')  # or another input if you want dynamic metric
)
def update_pie(metric):
    # Last 5 years
    last_year = co2["year"].max()
    first_year = last_year - 4
    df_last5 = co2[(co2["year"] >= first_year) & (co2["year"] <= last_year)]
    
    # Compute mean CO₂ per country
    df_mean = df_last5.groupby("country_name")["value"].mean().reset_index()
    
    # Sort top 5
    df_top5 = df_mean.nlargest(5, "value")
    
    # Aggregate the rest as 'Other'
    other_mean = df_mean[~df_mean["country_name"].isin(df_top5["country_name"])]["value"].sum()
    df_pie = pd.concat([df_top5, pd.DataFrame({"country_name": ["Other"], "value": [other_mean]})], ignore_index=True)
    
    fig = go.Figure(go.Pie(
        labels=df_pie["country_name"],
        values=df_pie["value"],
        hole=0.3  # optional for donut
    ))
    
    fig.update_layout(
        paper_bgcolor="#1a1d24",
        plot_bgcolor="#1a1d24",
        font=dict(color="#e0e6ed"),
    )
    
    return fig



@app.callback(
    Output('top10-graph', 'figure'),
    Input('top10-dropdown', 'value'),
    Input('top10-order-dropdown', 'value')
)
def update_top10(metric, order):
    # Determine latest year
    latest_year_co2 = co2["year"].max()
    latest_year_climate = climate["year"].max()
    latest_year_aq = aq["year"].max() if "year" in aq.columns else None

    # Select the correct dataframe
    if metric in ["value", "co2_per_capita"]:
        df_latest = co2[co2["year"] == latest_year_co2].copy()
        if metric == "co2_per_capita":
            df_latest["population"] = df_latest["value"] / df_latest["co2_per_capita"]
            df_latest["co2_per_capita"] = df_latest["value"] / df_latest["population"]
    elif metric in ["temp_max", "temp_min", "R1"]:
        df_latest = climate[climate["year"] == latest_year_climate].copy()
    else:
        df_latest = aq.copy()
        if latest_year_aq:
            df_latest = df_latest[df_latest["year"] == latest_year_aq]

    # Group by country
    grouped = df_latest.groupby("country_name")[metric].mean().reset_index()

    # Sort according to order
    if order == "best":
        df_top10 = grouped.nlargest(10, metric)
    else:
        df_top10 = grouped.nsmallest(10, metric)

    # Reverse so #1 is at the top in horizontal bar
    df_top10 = df_top10.iloc[::-1]

    fig = go.Figure(go.Bar(
        x=df_top10[metric],
        y=df_top10["country_name"],
        orientation='h',
        marker=dict(color="#4aa8ff")
    ))

    fig.update_layout(
        paper_bgcolor="#1a1d24",
        plot_bgcolor="#1a1d24",
        font=dict(color="#e0e6ed"),
        xaxis_title=metric,
        yaxis_title="Country",
        margin=dict(l=100, r=20, t=20, b=20)
    )

    return fig




@app.callback(
    Output('choro-graph', 'figure'),
    Input('aq-dropdown', 'value')
)
def update_choro(selected_var):
    map_vars = {"AQ Index": "aq", "PM2.5": "PM2.5", "PM10": "PM10"}
    col = map_vars[selected_var]

    def compute_bounds(series):
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        vmin = max(series.min(), q1 - 1.5 * iqr)
        vmax = min(series.max(), q3 + 1.5 * iqr)
        return vmin, vmax

    vmin, vmax = compute_bounds(aq[col])

    fig = go.Figure(go.Choropleth(
        locations=aq["country_code"],
        z=aq[col],
        locationmode="ISO-3",
        colorscale="blugrn",
        zmin=vmin,
        zmax=vmax,
        text=aq["country_name"],
        hovertemplate="<b>%{text}</b><br>"+selected_var+": %{z:.2f}<extra></extra>",
        marker_line_width=0,
        showscale=False
    ))

    fig.update_layout(
        paper_bgcolor="#1a1d24",
        plot_bgcolor="#1a1d24",
        font=dict(color="#e0e6ed"),
        margin=dict(l=20, r=20, t=20, b=20),
        geo=dict(
            projection_type="natural earth",
            showcountries=False,
            showland=True,
            landcolor="#111317",
            bgcolor="rgba(0,0,0,0)"
        )
    )
    return fig

# ------------------------------
# Run server
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
