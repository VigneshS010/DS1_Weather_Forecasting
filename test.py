# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from automate_forecast import run_forecast

# ⚡ Automatically run forecast to generate latest 5-day data
run_forecast()

# Set page config
st.set_page_config(
    page_title="5-Day Weather Forecast Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for style
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
        }
        .title {
            text-align: center;
            font-size: 3em;
            font-weight: bold;
            color: #4b6cb7;
            padding-bottom: 0.5em;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>☁️ 5-Day Weather Forecast Dashboard</div>", unsafe_allow_html=True)

# Load the prediction and weather data
pred_df = pd.read_csv("forecast_weather_condition.csv")
weather_df = pd.read_csv("forecast_weather_features.csv")

# Convert time to datetime
pred_df['time'] = pd.to_datetime(pred_df['time'])
weather_df['time'] = pd.to_datetime(weather_df['time'])

# Sidebar Filters
st.sidebar.header("🔎 Filter Options")
day_options = pred_df['time'].dt.date.unique()
selected_day = st.sidebar.selectbox("Select a day to view", day_options)

# Filter data by selected day
day_pred = pred_df[pred_df['time'].dt.date == selected_day]
day_weather = weather_df[weather_df['time'].dt.date == selected_day]

# --- Weather Forecast Chart ---
st.subheader(f"Predicted Weather Conditions for {selected_day}")
fig_pred = px.bar(
    day_pred,
    x='time',
    y=[1]*len(day_pred),  # Dummy y-axis to use color as label
    color='Predicted_Weather',
    labels={'x': 'Time', 'y': ''},
    color_discrete_map={
        'Sunny': '#FFD700',
        'Cloudy': '#A9A9A9',
        'Rainy': '#1E90FF'
    },
    title="Hourly Weather Prediction"
)
fig_pred.update_layout(showlegend=True, yaxis={'visible': False}, xaxis_title="Hour")
st.plotly_chart(fig_pred, use_container_width=True)

# --- Weather Parameters Chart ---
st.subheader(f"Weather Features for {selected_day}")
col1, col2 = st.columns(2)

with col1:
    fig_temp = px.line(
        day_weather,
        x='time',
        y='temperature_2m',
        title="Temperature (°C)",
        markers=True,
        line_shape='spline',
        color_discrete_sequence=['#FF6347']
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    fig_press = px.line(
        day_weather,
        x='time',
        y='pressure_msl',
        title="Pressure (hPa)",
        markers=True,
        line_shape='spline',
        color_discrete_sequence=['#4682B4']
    )
    st.plotly_chart(fig_press, use_container_width=True)

with col2:
    fig_humidity = px.line(
        day_weather,
        x='time',
        y='relative_humidity_2m',
        title="Humidity (%)",
        markers=True,
        line_shape='spline',
        color_discrete_sequence=['#20B2AA']
    )
    st.plotly_chart(fig_humidity, use_container_width=True)

    fig_wind = px.line(
        day_weather,
        x='time',
        y='windspeed_10m',
        title="Wind Speed (km/h)",
        markers=True,
        line_shape='spline',
        color_discrete_sequence=['#9370DB']
    )
    st.plotly_chart(fig_wind, use_container_width=True)

# Refresh Button
if st.sidebar.button("🔄 Refresh Forecast"):
    run_forecast()
    st.success("Forecast updated!")
    st.experimental_rerun()

# Footer
st.markdown("""
---
📉 Developed with ❤️ by Vignesh - Powered by Streamlit and Plotly
""")
