from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo

app = Flask(__name__)

# Dark theme template for all charts
dark_template = dict(
    layout=go.Layout(
        paper_bgcolor="#1a1d24",
        plot_bgcolor="#1a1d24",
        font=dict(color="#e0e6ed"),
        xaxis=dict(color="#e0e6ed", gridcolor="#2a2f3a"),
        yaxis=dict(color="#e0e6ed", gridcolor="#2a2f3a"),
    )
)

@app.route("/")
def index():
    # Sample data
    dates = pd.date_range(start="2024-01-01", periods=12, freq="M")
    co2 = [100, 120, 130, 125, 140, 160, 155, 170, 165, 180, 190, 200]
    sectors = ["Transport", "Industry", "Residential", "Agriculture"]
    sector_vals = [40, 35, 15, 10]
    df = pd.DataFrame({
        'country_code': ["CAN", "USA", "MEX"],
        'value': [300, 500, 200]
    })

    # Overview KPIs
    total_emissions = sum(co2)
    emissions_trend = co2[-1] - co2[0]
    average_monthly = total_emissions / len(co2)

    # Time series chart
    ts_fig = go.Figure(
        data=[go.Scatter(
            x=dates, y=co2, mode="lines+markers",
            line=dict(width=2, color="#4aa8ff"),
            marker=dict(color="#4aa8ff")
        )],
        layout=dark_template["layout"]
    )
    ts_html = pyo.plot(ts_fig, include_plotlyjs=False, output_type="div")

    # Choropleth chart (2D, zoom-only)
    q1 = df['value'].quantile(0.25)
    q3 = df['value'].quantile(0.75)
    iqr = q3 - q1
    vmin = max(df['value'].min(), q1 - 1.5 * iqr)
    vmax = min(df['value'].max(), q3 + 1.5 * iqr)

    choro_fig = go.Figure(
        data=go.Choropleth(
            locations=df['country_code'],
            z=df['value'],
            locationmode='ISO-3',
            colorscale=[[0, '#0d253f'], [0.33, '#1e3a5f'], [0.66, '#3b82f6'], [1, '#60a5fa']],
            zmin=vmin,
            zmax=vmax,
            colorbar=dict(title='Value', tickfont=dict(color='#e0e6ed'), outlinewidth=0),
            hovertemplate='<b>%{location}</b><br>Value: %{z}<extra></extra>'
        ),
        layout=go.Layout(
            paper_bgcolor="#1a1d24",
            plot_bgcolor="#1a1d24",
            font=dict(color="#e0e6ed"),
            margin=dict(l=40, r=40, t=40, b=40),
            geo=dict(
                projection_type='natural earth',
                showcountries=True,
                showland=True,
                landcolor='#111317',
                countrycolor='rgba(255,255,255,0.2)',
                bgcolor='rgba(0,0,0,0)'
            ),
            dragmode=False  # disables all drag/pan
        )
    )

    choro_html = pyo.plot(
        choro_fig,
        include_plotlyjs=False,
        output_type="div",
        config=dict(
            scrollZoom=True,  # enable zoom
            displayModeBar=True,
            displaylogo=False,
            modeBarButtonsToRemove=[
                'pan2d', 'select2d', 'lasso2d',
                'zoomIn2d', 'zoomOut2d',
                'autoScale2d', 'resetScale2d',
                'hoverClosestCartesian', 'hoverCompareCartesian'
            ],
            doubleClick='reset'
        )
    )

    # Pie chart
    pie_fig = go.Figure(
        data=[go.Pie(
            labels=sectors,
            values=sector_vals,
            marker=dict(colors=["#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe"])
        )],
        layout=dark_template['layout']
    )
    pie_html = pyo.plot(pie_fig, include_plotlyjs=False, output_type="div")

    # Bar chart
    bar_fig = go.Figure(
        data=[go.Bar(x=sectors, y=sector_vals, marker=dict(color="#4aa8ff"))],
        layout=dark_template['layout']
    )
    bar_html = pyo.plot(bar_fig, include_plotlyjs=False, output_type="div")

    # Table
    table_fig = go.Figure(
        data=[go.Table(
            header=dict(values=["Month", "CO2"], fill_color="#1f2937", font=dict(color="#e0e6ed")),
            cells=dict(values=[dates.strftime("%Y-%m"), co2], fill_color="#111317", font=dict(color="#e0e6ed"))
        )],
        layout=dark_template['layout']
    )
    table_html = pyo.plot(table_fig, include_plotlyjs=False, output_type="div")

    return render_template(
        "dashboard.html",
        total_emissions=total_emissions,
        emissions_trend=emissions_trend,
        average_monthly=average_monthly,
        ts_html=ts_html,
        choro_html=choro_html,
        pie_html=pie_html,
        bar_html=bar_html,
        table_html=table_html
    )


def load_dfs():
    aq = pd.read_csv('data/aq_imputed.csv')
    countries = pd.read_csv('data/country_map.csv')
    climate = pd.read_csv('data/climate.csv')
    co2 = pd.read_csv('data/co2.csv')




if __name__ == "__main__":

    load_dfs()
    app.run(debug=True)
