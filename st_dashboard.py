import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt

# ---------------------- Configuring the page ----------------------
st.set_page_config(page_title="CitiBike Strategy Dashboard", layout="wide")

# ---------------------- Title & Description ----------------------
st.title("CitiBike Strategy Dashboard (NYC 2022, 30% Sample)")
st.markdown(
    "This dashboard shows the most popular CitiBike start stations, daily rider trends, "
    "and how rides relate to temperature."
)

# ---------------------- Importing Data ----------------------
top20 = pd.read_csv("top20.csv")

daily = pd.read_csv("daily_rides_weather_sample_30pct.csv")
daily["date"] = pd.to_datetime(daily["date"], errors="coerce")

# Filter to only include 2022 (so the chart doesn’t show 2021)
daily = daily[daily["date"].dt.year == 2022].copy()

# ---------------------- BAR CHART ----------------------
fig_bar = go.Figure(
    go.Bar(
        x=top20["start_station"],
        y=top20["trips"],
        marker=dict(
            color=top20["trips"],
            colorscale="Blues",
            showscale=True
        )
    )
)

fig_bar.update_layout(
    title="Top 20 Most Popular CitiBike Start Stations (NYC 2022, 30% Sample)",
    xaxis_title="Start Station",
    yaxis_title="Number of Trips",
    template="plotly_white",
    height=600,
    margin=dict(l=40, r=40, t=60, b=140)
)
fig_bar.update_xaxes(tickangle=-45)

st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------- LINE CHART (DUAL AXIS) ----------------------
fig_line = make_subplots(specs=[[{"secondary_y": True}]])

fig_line.add_trace(
    go.Scatter(
        x=daily["date"],
        y=daily["bike_rides_daily"],
        name="Daily Bike Rides",
        mode="lines",
        line=dict(width=3, color="blue")
    ),
    secondary_y=False
)

fig_line.add_trace(
    go.Scatter(
        x=daily["date"],
        y=daily["avgTemp"],
        name="Avg Temperature",
        mode="lines",
        line=dict(width=3, color="red")
    ),
    secondary_y=True
)

fig_line.update_layout(
    title="Daily CitiBike Rides vs Temperature (NYC 2022, 30% Sample)",
    template="plotly_white",
    height=700,
    margin=dict(l=40, r=40, t=60, b=40)
)

fig_line.update_yaxes(title_text="Bike Rides", secondary_y=False)
fig_line.update_yaxes(title_text="Temperature (°F)", secondary_y=True)

st.plotly_chart(fig_line, use_container_width=True)

# ---------------------- MAP (Kepler HTML) ----------------------
st.header("CitiBike Trips Map (Kepler.gl)")

path_to_html = "CitiBike_Top500_Kepler.html"

with open(path_to_html, "r", encoding="utf-8") as f:
    html_data = f.read()

st.components.v1.html(html_data, height=1000, scrolling=True)
