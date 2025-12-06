{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "33f5383d-f4de-40c3-8f27-fd531cfb7845",
   "metadata": {},
   "source": [
    "🔍 Project Objectives\n",
    "Understand where CitiBike rides start most frequently\n",
    "Analyze seasonality and how weather impacts ride volume\n",
    "Compare rider types (member vs casual) in terms of trip duration and patterns\n",
    "Apply data cleaning and visualization techniques using Python, Pandas, Matplotlib, and Seaborn\n",
    "📂 Data Sources\n",
    "CitiBike NYC Trip Data:\n",
    "Subset of 2022 ride data (CSV)\n",
    "Includes ride timestamps, station locations, rider type, and coordinates\n",
    "Weather Data:\n",
    "Daily NYC weather data merged with trip data\n",
    "Includes average temperature (°F)\n",
    "Note: Raw files are temporarily excluded from the repository due to GitHub’s 25MB limit. Only cleaned + prepared datasets are included when under size limits.\n",
    "🛠 Tools & Libraries\n",
    "Tool\tPurpose\n",
    "Python\tCore analysis & cleaning\n",
    "Pandas\tData wrangling and transformation\n",
    "Seaborn & Matplotlib\tData visualization\n",
    "JupyterLab\tInteractive analysis & narrative\n",
    "Git / GitHub\tVersion control & submission\n",
    "🧹 Data Preparation Highlights\n",
    "Converted timestamps to datetime format\n",
    "Engineered new fields:\n",
    "month\n",
    "trip_duration_min\n",
    "Merged external weather data using date key\n",
    "Filtered out extreme trip durations (likely errors)\n",
    "📊 Key Visualizations & Insights\n",
    "🔹 Top 20 Starting Stations (Bar Chart)\n",
    "Usage is heavily concentrated in central Manhattan\n",
    "High demand near subway stations, workplaces, and tourist areas\n",
    "Suggests need for bike rebalancing strategies\n",
    "🔹 Seasonality of Ride Demand (Dual-Axis Line Chart)\n",
    "Ride volume rises significantly during warmer months\n",
    "Strong correlation between temperature and ridership\n",
    "Winter shows low usage due to harsh weather\n",
    "🔹 Trip Duration by Rider Type (Box Plot)\n",
    "Casual riders have longer and more varied trip durations\n",
    "Members take shorter, more consistent rides — likely commuters\n",
    "Indicates different motivations for using CitiBike\n",
    "🔹 Distribution of Trip Duration by Rider Type (FacetGrid)\n",
    "Members cluster around short trips\n",
    "Casual riders show a long-tail distribution, including leisure rides\n",
    "Reinforces behavioral differences between rider groups\n",
    "📁 Repository Structure\n",
    "├─ Data/\n",
    "│  ├─ Prepared/            # Cleaned / merged files\n",
    "│  └─ Raw/ (local only)    # Large original data files (excluded from repo)\n",
    "├─ Notebooks/\n",
    "│  └─ citibike_analysis.ipynb\n",
    "└─ README.md\n",
    "🧠 What I Learned\n",
    "Working with large datasets and optimizing storage for GitHub\n",
    "Creating meaningful visualizations that tell a story\n",
    "Improving readability and interpretation with thoughtful design choices\n",
    "Understanding real-world transportation patterns using dat"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5c0cd3ef-ca65-4c9b-a519-ed0fad74f5f0",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (citibike)",
   "language": "python",
   "name": "citibike"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.18"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
