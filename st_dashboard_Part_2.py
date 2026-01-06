import os
import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit.components.v1 as components

# ---------------------- Config ----------------------
st.set_page_config(page_title="CitiBike Strategy Dashboard", layout="wide")

KEPLER_HTML = "CitiBike_Top500_Kepler.html"


REDUCED_CANDIDATES = [
    "Data/Processed/reduced_data_to_plot.csv",
    "data/Processed/reduced_data_to_plot.csv",
]


DAILY_CANDIDATES = [
    "data/Processed/daily_2022_rides_temp.csv",
    "Data/Processed/daily_2022_rides_temp.csv",
]

TOP20_CANDIDATES = [
    "top20_sample.csv",
    "Data/Processed/top20_sample.csv",
    "data/Processed/top20_sample.csv",
]

def first_existing(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None

reduced_path = first_existing(REDUCED_CANDIDATES)
daily_path = first_existing(DAILY_CANDIDATES)
top20_path = first_existing(TOP20_CANDIDATES)

# ---------------------- Load reduced sample ----------------------
if reduced_path is None:
    st.error(
        "I can’t find your reduced dataset.\n\n"
        "Expected one of these paths:\n"
        f"- {REDUCED_CANDIDATES[0]}\n"
        f"- {REDUCED_CANDIDATES[1]}\n\n"
        "Go back to your Step 3 notebook and save the reduced sample to Data/Processed/reduced_data_to_plot.csv."
    )
    st.stop()

df = pd.read_csv(reduced_path)

# Parse date
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Validating key columns
required_cols = {
    "date", "avgTemp",
    "start_station", "end_station",
    "start_lat", "start_lng", "end_lat", "end_lng"
}
missing = required_cols - set(df.columns)
if missing:
    st.error(
        "Your reduced dataset is missing required columns:\n"
        + ", ".join(sorted(missing))
        + "\n\nFix: In the notebook, rename start_station_name -> start_station and end_station_name -> end_station before saving."
    )
    st.stop()

# ---------------------- Sidebar: Pages ----------------------
st.sidebar.header("Pages")
page = st.sidebar.selectbox(
    "Choose a page",
    [
        "Introduction",
        "Dual-axis line chart",
        "Top stations bar chart",
        "Kepler map",
        "Extra Insight (Top routes)",
        "Recommendations",
    ],
)

st.sidebar.markdown("---")
top_n = st.sidebar.slider("Top N", min_value=10, max_value=30, value=20)

# ---------------------- Data for charts ----------------------
if daily_path is not None:
    daily = pd.read_csv(daily_path, parse_dates=["date"])
else:
    daily = (
        df.dropna(subset=["date"])
          .groupby("date", as_index=False)
          .agg(
              bike_rides_daily=("start_station", "count"),
              avgTemp=("avgTemp", "mean")
          )
          .sort_values("date")
    )

# Top stations
if top20_path is not None:
    top_stations = pd.read_csv(top20_path)
    # If file has more than needed, enforce columns
    if "start_station" in top_stations.columns and "trips" in top_stations.columns:
        top_stations = top_stations.sort_values("trips", ascending=False).head(top_n)
    else:
        # fallback compute if file doesn’t match expected structure
        top_stations = (
            df.groupby("start_station", as_index=False)
              .size()
              .rename(columns={"size": "trips"})
              .sort_values("trips", ascending=False)
              .head(top_n)
        )
else:
    top_stations = (
        df.groupby("start_station", as_index=False)
          .size()
          .rename(columns={"size": "trips"})
          .sort_values("trips", ascending=False)
          .head(top_n)
    )

# Extra chart: Top routes (computed from reduced sample)
top_routes = (
    df.groupby(["start_station", "end_station"], as_index=False)
      .size()
      .rename(columns={"size": "trips"})
      .sort_values("trips", ascending=False)
      .head(top_n)
)

# ---------------------- Page: Intro ----------------------
if page == "Introduction":
    st.title("CitiBike Strategy Dashboard (NYC 2022) ")

    st.markdown(
        "**Purpose**\n\n"
        "This dashboard shows how and when Citi Bike is most heavily used, helping identify where bikes are most likely to run low. It highlights busy stations, seasonal changes, and common routes to support more efficient rebalancing and dock planning. \n\n"
        "It helps answer: *When is bike usage highest? Which stations are more likely to experience shortages? Which travel routes are used most consistently?*\n\n"
        "**What you'll see**\n"
        "- Dual-axis line chart: daily rides vs. average temperature\n"
        "- Bar chart: most popular start stations\n"
        "- Kepler map: interactive visualization of trip patterns\n"
        "- Extra Insight: top station-to-station routes\n"
        "- Recommendations: actions based on insights\n\n"
    )

    st.metric("Trips in reduced sample", f"{len(df):,}")
    st.caption(f"Reduced dataset loaded from: {reduced_path}")

# ---------------------- Page: Dual-axis line ----------------------
elif page == "Dual-axis line chart":
    st.header("Daily Citi Bike Rides vs Temperature (Dual-axis line chart)")

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=daily["date"],
            y=daily["bike_rides_daily"],
            name="Daily Bike Rides",
            mode="lines",
            line=dict(width=3, color="blue") ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=daily["date"],
            y=daily["avgTemp"],
            name="Avg Temperature",
            mode="lines",
            line=dict(width=3, color="red") ),
        secondary_y=True,
    )

    fig.update_layout(
        title="Daily Citi Bike Rides vs Temperature (NYC 2022)",
        height=650,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    fig.update_yaxes(title_text="Bike rides (count)", secondary_y=False)
    fig.update_yaxes(title_text="Avg temperature (°F)", secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "**Interpretation**\n\n"
        "As temperatures rise from winter into summer, daily bike rides increase, reaching their highest levels during the warmest months. When temperatures begin to drop in the fall and winter, ridership declines, showing that weather is a major factor influencing how often people use Citi Bike. "
        "This suggests bike shortages are more likely during warm-season peaks"
    )

# ---------------------- Page: Top stations bar ----------------------
elif page == "Top stations bar chart":
    st.header("Top Start Stations (Bar Chart)")

    fig = go.Figure(
        go.Bar(
            x=top_stations["start_station"],
            y=top_stations["trips"],
            marker=dict(
                color=top_stations["trips"],
                colorscale="Blues",
                showscale=True
            )
        )
    )

    fig.update_layout(
        title=f"Top {top_n} Most Popular Start Stations (NYC 2022)",
        xaxis_title="Start Station",
        yaxis_title="Number of Trips",
        template="plotly_white",
        height=650,
        margin=dict(l=40, r=40, t=60, b=140),
    )
    fig.update_xaxes(tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "**Interpretation**\n\n"
        "This chart shows that the most popular start stations are concentrated in busy, central areas of the city, especially near transit hubs, commercial districts, and popular destinations. "
        "These stations consistently generate a high number of trips, indicating strong and reliable demand."
    )

# ---------------------- Page: Kepler map ----------------------
elif page == "Kepler map":
    st.header("CitiBike Trips Map (Kepler.gl)")

    if not os.path.exists(KEPLER_HTML):
        st.warning(
            f"Kepler file not found: {KEPLER_HTML}\n\n"
            "Make sure CitiBike_Top500_Kepler.html is in the same folder as st_dashboard_Part_2.py."
        )
    else:
        with open(KEPLER_HTML, "r", encoding="utf-8") as f:
            html_data = f.read()
        components.html(html_data, height=1000, scrolling=True)

    st.markdown(
        "**Interpretation**\n\n"
        "The map shows that Citi Bike trips are heavily concentrated in Manhattan. The dense clusters of routes indicate frequent, repeat travel between nearby stations, suggesting strong demand for short trips and commuting. These patterns help identify where bike availability, station capacity, and rebalancing efforts should be prioritized. These patterns help identify areas where bikes frequently move and where shortages may occur. "
    )

# ---------------------- Page: Extra chart (Top routes) ----------------------
elif page == "Extra Insight (Top routes)":
    st.header("Extra Insight: Most Frequent Routes (Start → End)")

    routes_plot = top_routes.copy()
    routes_plot["route"] = routes_plot["start_station"] + " → " + routes_plot["end_station"]

    fig = go.Figure(
        go.Bar(
            x=routes_plot["route"],
            y=routes_plot["trips"],
        )
    )
    fig.update_layout(
        title=f"Top {top_n} Routes (NYC 2022)",
        xaxis_title="Route",
        yaxis_title="Trips",
        height=650,
        margin=dict(l=40, r=40, t=60, b=180),
    )
    fig.update_xaxes(tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "**Interpretation**\n\n"
        "This chart shows that the most frequent Citi Bike routes are concentrated around Central Park, major transit hubs, and waterfront areas. Many of the top routes are short, repeat trips between the same start and end stations, suggesting that riders often use Citi Bike for commuting, leisure loops, and last-mile travel."
        "The consistency of these routes indicates predictable demand patterns, which can help prioritize bike availability and rebalancing along these key corridors."
    )

# ---------------------- Page: Recommendations ----------------------
else:
    st.header("Recommendations")

    st.markdown("""
### Recommendations & Insights

**1) Prepare for peak seasons**  
- Bike demand increases in warmer months, so staffing levels and rebalancing frequency should be adjusted accordingly.

**2) Prioritize high-demand stations**  
- Focus monitoring and restocking efforts on the top start stations with consistently high trip volume.  
- Evaluate dock capacity upgrades at stations that regularly experience supply pressure.

**3) Apply corridor insights to operations**  
- Repeated routes and dense corridors indicate where bikes are likely to accumulate or run short.  
- Use these patterns to plan efficient truck routes and proactive rebalancing schedules.

**4) Establish a weekly operations plan**  
- Combine insights from top stations, seasonal trends, and corridor hotspots into a weekly priority list.  
- Align rebalancing resources with this list to improve overall bike availability.
""")
