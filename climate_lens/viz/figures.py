"""Plotly figure builder functions."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objs as go

from climate_lens.config import FIGURE_LAYOUT, FORECAST_START_YEAR, METRIC_LABELS, THEME


def build_time_series(selected_countries, selected_metric, co2_forecast, climate):
    fig = go.Figure()
    palette = [
        "#4aa8ff",
        "#7bd389",
        "#f7b267",
        "#f48498",
        "#a78bfa",
        "#22d3ee",
        "#facc15",
        "#fb7185",
    ]

    for idx, country in enumerate(selected_countries):
        color = palette[idx % len(palette)]
        if selected_metric in ["co2", "co2_per_capita"]:
            d = co2_forecast[co2_forecast["country_name"] == country].sort_values("year")
            d_solid = d[d["year"] <= FORECAST_START_YEAR]
            d_dashed = d[d["year"] >= FORECAST_START_YEAR]

            if not d_solid.empty:
                fig.add_trace(
                    go.Scatter(
                        x=d_solid["year"],
                        y=d_solid[selected_metric],
                        mode="lines+markers",
                        name=country,
                        legendgroup=country,
                        line={"dash": "solid", "color": color, "width": 2.5},
                        marker={"color": color, "size": 6},
                    )
                )
            if not d_dashed.empty:
                fig.add_trace(
                    go.Scatter(
                        x=d_dashed["year"],
                        y=d_dashed[selected_metric],
                        mode="lines+markers",
                        name=country,
                        legendgroup=country,
                        showlegend=False,
                        line={"dash": "dot", "color": color, "width": 2.5},
                        marker={"color": color, "size": 6},
                    )
                )
        else:
            d = (
                climate[climate["country_name"] == country]
                .groupby("year")
                .agg({"temp_min": "min", "temp_max": "max", "R1": "mean"})
                .reset_index()
            )
            fig.add_trace(
                go.Scatter(
                    x=d["year"],
                    y=d[selected_metric],
                    mode="lines+markers",
                    name=country,
                    legendgroup=country,
                    line={"dash": "solid", "color": color, "width": 2.5},
                    marker={"color": color, "size": 6},
                )
            )

    x_end = 2027 if selected_metric in ["co2", "co2_per_capita"] else 2022
    fig.update_layout(
        **FIGURE_LAYOUT,
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "center",
            "x": 0.5,
            "bgcolor": "rgba(0,0,0,0)",
        },
        margin={"l": 0, "r": 0, "t": 60, "b": 0},
        xaxis={"range": [2005, x_end]},
        xaxis_title="Year",
        yaxis_title=METRIC_LABELS[selected_metric],
    )
    return fig


def build_pie_distribution(co2: pd.DataFrame):
    last_year = co2["year"].max()
    first_year = last_year - 4
    df_last5 = co2[(co2["year"] >= first_year) & (co2["year"] <= last_year)]

    df_mean = df_last5.groupby("country_name")["co2"].mean().reset_index()
    df_top5 = df_mean.nlargest(5, "co2")
    other_mean = df_mean[~df_mean["country_name"].isin(df_top5["country_name"])]["co2"].sum()
    df_pie = pd.concat([df_top5, pd.DataFrame({"country_name": ["Other"], "co2": [other_mean]})], ignore_index=True)

    colors = ["#4aa8ff", "#2f72c4", "#1c4f8c", "#14365e", "#0b1f33", "#050a19"][: len(df_pie)]

    fig = go.Figure(
        go.Pie(
            labels=df_pie["country_name"],
            values=df_pie["co2"],
            hole=0.3,
            marker={"colors": colors},
            textinfo="label",
            hovertemplate="%{label}: %{percent:.1%}<extra></extra>",
        )
    )
    fig.update_layout(
        **FIGURE_LAYOUT,
        showlegend=False,
        title={
            "text": "CO2 Emissions Distribution",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"color": THEME["font"], "size": 18},
        },
    )
    return fig


def build_top10(metric: str, order: str, co2: pd.DataFrame, climate: pd.DataFrame, aq: pd.DataFrame):
    latest_year_co2 = co2["year"].max()
    latest_year_climate = climate["year"].max()
    latest_year_aq = aq["year"].max() if "year" in aq.columns else None

    if metric in ["co2", "co2_per_capita"]:
        df_latest = co2[co2["year"] == latest_year_co2].copy()
        if metric == "co2_per_capita":
            df_latest["population"] = df_latest["co2"] / df_latest["co2_per_capita"]
            df_latest["co2_per_capita"] = df_latest["co2"] / df_latest["population"]
    elif metric in ["temp_max", "temp_min", "R1"]:
        df_latest = climate[climate["year"] == latest_year_climate].copy()
    else:
        df_latest = aq.copy()
        if latest_year_aq is not None:
            df_latest = df_latest[df_latest["year"] == latest_year_aq]

    grouped = df_latest.groupby("country_name")[metric].mean().reset_index()
    df_top10 = grouped.nlargest(10, metric) if order == "best" else grouped.nsmallest(10, metric)
    df_top10 = df_top10.iloc[::-1]

    fig = go.Figure(
        go.Bar(
            x=df_top10[metric],
            y=df_top10["country_name"],
            orientation="h",
            marker={"color": THEME["accent"]},
        )
    )
    fig.update_layout(
        **FIGURE_LAYOUT,
        xaxis_title=METRIC_LABELS.get(metric, "Air Quality Index" if metric == "aq" else metric),
        yaxis_title="Country",
        margin={"l": 20, "r": 0, "t": 0, "b": 0},
        yaxis={"tickangle": -30, "ticklabelstandoff": 10},
    )
    return fig


def build_choropleth(selected_var: str, aq: pd.DataFrame):
    map_vars = {"Air Quality Index": "aq", "PM2.5": "PM2.5", "PM10": "PM10"}
    col = map_vars[selected_var]

    q1 = aq[col].quantile(0.25)
    q3 = aq[col].quantile(0.75)
    iqr = q3 - q1
    vmin = max(aq[col].min(), q1 - 1.5 * iqr)
    vmax = min(aq[col].max(), q3 + 1.5 * iqr)

    fig = go.Figure(
        go.Choropleth(
            locations=aq["country_code"],
            z=aq[col],
            locationmode="ISO-3",
            colorscale="blugrn",
            zmin=vmin,
            zmax=vmax,
            text=aq["country_name"],
            hovertemplate="<b>%{text}</b><br>" + selected_var + ": %{z:.2f}<extra></extra>",
            marker_line_width=0,
            showscale=False,
        )
    )
    fig.update_layout(
        **FIGURE_LAYOUT,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        geo={
            "projection_type": "natural earth",
            "showcountries": False,
            "showland": True,
            "showframe": True,
            "showlakes": False,
            "landcolor": "#111317",
            "bgcolor": "rgba(0,0,0,0)",
        },
    )
    return fig
