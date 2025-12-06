# 🚴 CitiBike NYC Data Analysis Project
This project explores CitiBike trips in New York City to uncover insights into rider behavior, seasonal demand patterns, and station popularity. It is part of a larger data analytics learning journey focused on end-to-end data wrangling, visualization, and storytelling.
# 🔍 Project Objectives
- Understand where CitiBike rides start most frequently
- Analyze seasonality and how weather impacts ride volume
- Compare rider types (member vs casual) in terms of trip duration and patterns
- Apply data cleaning and visualization techniques using Python, Pandas, Matplotlib, and Seaborn
# 📂 Data Sources
- CitiBike NYC Trip Data
- Subset of 2022 ride data (CSV)
    - Includes ride timestamps, station locations, rider type, and coordinates
- Weather Data
    - Daily NYC weather data merged with trip data
    - Includes average temperature (°F)
#### Raw files excluded from GitHub due to 25MB size limit.
# 🛠 Tools & Libraries
- Python: core analysis & cleaning
- Pandas: data wrangling and transformation
- Seaborn & Matplotlib: data visualization
- JupyterLab : interactive analysis & narrative
- Git / GitHub: version control & submission
# 🧹 Data Preparation Highlights
- Converted timestamps to datetime
- Engineered fields: month, trip_duration_min
- Merged weather data using date key
# 📊 Key Visualizations & Insights
- 🔹 Top 20 Starting Stations (Bar Chart)
High demand in central Manhattan near transit and tourist hubs
Indicates rebalancing priorities
- 🔹 Seasonality (Dual-Axis Line Chart)
    - Strong correlation between warmer temps and increased ridership
- 🔹 Trip Duration by Rider Type (Box Plot)
    - Casual riders take longer trips (recreation)
Members take shorter trips (commuting)
- 🔹 Trip Duration Distribution (FacetGrid)
      - Casual riders show longer tail of trip duration
Members cluster around short durations
- 📁 Repository Structure
- ├─ data/           # cleaned datasets (raw excluded)
- ├─ notebooks/      # analysis notebooks
- └─ README.md       # project summary