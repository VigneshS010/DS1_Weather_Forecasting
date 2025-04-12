# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import numpy as np
from pytz import timezone
import chatbot  # Import the chatbot functions
import re  # Import the regular expression module

# Placeholder for run_forecast
@st.cache_data
def run_forecast(city):
    print(f"Simulating forecast run for {city}...")
    time.sleep(2)

    base_time = pd.Timestamp.now().normalize()
    time_range = pd.date_range(base_time, periods=5 * 24, freq='H')

    weather_data = {
        'time': time_range,
        'temperature_2m': np.random.uniform(15, 35, size=len(time_range)),
        'relative_humidity_2m': np.random.uniform(40, 90, size=len(time_range)),
        'pressure_msl': np.random.uniform(1000, 1020, size=len(time_range)),
        'windspeed_10m': np.random.uniform(5, 25, size=len(time_range))
    }
    weather_df_sim = pd.DataFrame(weather_data)
    weather_df_sim['temperature_2m'] += 5 * np.sin(np.linspace(0, 5 * 2 * np.pi, len(time_range)))
    weather_df_sim['relative_humidity_2m'] = np.clip(
        weather_df_sim['relative_humidity_2m'] - 10 * np.sin(np.linspace(0, 5 * 2 * np.pi, len(time_range))), 10, 95
    )
    weather_df_sim.to_csv("forecast_weather_features.csv", index=False)

    conditions = ['Sunny', 'Cloudy', 'Rainy']
    pred_df_sim = pd.DataFrame({
        'time': time_range,
        'Predicted_Weather': np.random.choice(conditions, size=len(time_range), p=[0.6, 0.3, 0.1])
    })
    pred_df_sim.to_csv("forecast_weather_condition.csv", index=False)
    print(f"Dummy forecast data saved for {city}.")

# Set Streamlit page configuration
st.set_page_config(page_title="5-Day Weather Forecast Dashboard", layout="wide")

# Title Styling
st.markdown("<h1 style='text-align: center;'>🌦️ 5-Day Weather Forecast Dashboard</h1>", unsafe_allow_html=True)

# City and date selection below the title
col1, col2 = st.columns(2)
with col1:
    city_list = ["Chennai", "Delhi", "Mumbai", "Bangalore", "Hyderabad"]
    selected_city = st.selectbox("Select City", city_list)

with col2:
    pred_df = pd.read_csv("forecast_weather_condition.csv")
    pred_df['time'] = pd.to_datetime(pred_df['time'])
    day_options = sorted(pred_df['time'].dt.date.unique())
    selected_day = st.selectbox("Select a day to view", day_options)

# Session state for first-time and city change detection
if "city_loaded" not in st.session_state:
    st.session_state.city_loaded = False
    st.session_state.last_city = None

if not st.session_state.city_loaded:
    with st.spinner("Running forecast for Chennai..."):
        run_forecast("Chennai")
    st.success("Forecast completed for Chennai ✅")
    st.session_state.city_loaded = True
    st.session_state.last_city = "Chennai"
elif selected_city != st.session_state.last_city:
    with st.spinner(f"Running forecast for {selected_city}..."):
        run_forecast(selected_city)
    st.success(f"Forecast completed for {selected_city} ✅")
    st.session_state.last_city = selected_city
    # Clear cached data when city changes
    st.cache_data.clear()

# Load forecast data
weather_df = pd.read_csv("forecast_weather_features.csv")
pred_df = pd.read_csv("forecast_weather_condition.csv")

pred_df['time'] = pd.to_datetime(pred_df['time'])
weather_df['time'] = pd.to_datetime(weather_df['time'])

# Get current time and weather at current hour
current_time = pd.Timestamp.now().round('H')
current_hour_weather = weather_df[weather_df['time'] == current_time]
current_hour_pred = pred_df[pred_df['time'] == current_time]

# Convert current time to Indian Standard Time (IST)
india_time = datetime.now(timezone('Asia/Kolkata'))

# Display current weather info
if not current_hour_weather.empty and not current_hour_pred.empty:
    cur_weather = current_hour_weather.iloc[0]
    cur_pred = current_hour_pred.iloc[0]

    weather_icon = {
        'Sunny': '☀️',
        'Cloudy': '☁️',
        'Rainy': '🌧️',
        'Clear': '☀️'
    }
    emoji = weather_icon.get(cur_pred['Predicted_Weather'], '❓')

    st.markdown(f"""
        <div style="background: linear-gradient(to right, #83a4d4, #b6fbff); border-radius: 20px; padding: 30px; margin: 30px auto; max-width: 700px; font-family: 'Segoe UI', sans-serif; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15); animation: fadeIn 0.8s ease-in-out;">
            <h2>🕒 Current Weather in {selected_city}</h2>
            <p><strong>📅 Time:</strong> {india_time.strftime('%A, %d %B %Y %I:%M %p')} (IST)</p>
            <p><strong>🌦️ Condition:</strong> {emoji} {cur_pred['Predicted_Weather']}</p>
            <p><strong>🌡️ Temperature:</strong> {cur_weather['temperature_2m']:.1f}°C</p>
            <p><strong>💧 Humidity:</strong> {cur_weather['relative_humidity_2m']:.0f}%</p>
            <p><strong>🧭 Pressure:</strong> {cur_weather['pressure_msl']:.0f} hPa</p>
            <p><strong>💨 Wind Speed:</strong> {cur_weather['windspeed_10m']:.1f} km/h</p>
        </div>
    """, unsafe_allow_html=True)

    # Center the "Chat with AI" button
    col_button = st.columns([1, 1, 1])[1]
    with col_button:
        if st.button("Chat with AI", key="chat_button"):
            st.session_state.show_chat = True

        if 'show_chat' not in st.session_state:
            st.session_state.show_chat = False

    # Apply custom CSS to increase button size
    st.markdown(
        """
        <style>
        #chat_button {
            padding: 15px 30px;
            font-size: 18px;
            background-color: green;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

day_pred = pred_df[pred_df['time'].dt.date == selected_day]
day_weather = weather_df[weather_df['time'].dt.date == selected_day]

# Predicted Weather Conditions Chart
st.subheader(f"Predicted Weather Conditions for {selected_day}")
if not day_pred.empty:
    fig_pred = px.bar(
        day_pred,
        x='time',
        y=[1] * len(day_pred),
        color='Predicted_Weather',
        labels={'x': 'Time', 'y': ''},
        color_discrete_map={
            'Sunny': '#FFD700',
            'Cloudy': '#A9A9A9',
            'Rainy': '#1E90FF',
            'Clear': '#ADD8E6'
        },
        title=f"Hourly Weather Prediction - {selected_city}"
    )
    fig_pred.update_layout(showlegend=True, yaxis={'visible': False}, xaxis=dict(tickformat='%H:%M'))
    st.plotly_chart(fig_pred, use_container_width=True)
else:
    st.warning("No prediction data available for the selected day.")

# Hourly Weather Boxes
st.subheader("Hourly Weather Details")

st.markdown("""
    <style>
        .scroll-box {
            overflow-x: auto;
            white-space: nowrap;
            background-color: #f9f9f9;
            padding: 20px 10px;
            border-radius: 10px;
            border: 1px solid #ccc;
            margin-bottom: 20px;
        }
        .hour-box-vertical {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            margin-right: 10px;
            display: inline-block;
            width: 160px;
            vertical-align: top;
            text-align: center;
            box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
            font-size: 14px;
            white-space: normal;
            min-height: 150px;
            color: black;
        }
        .hour-box-vertical h4 {
            margin-top: 0;
            margin-bottom: 8px;
            font-size: 16px;
            font-weight: bold;
            color: black;
        }
        .weather-info {
            line-height: 1.4;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

weather_emoji = {'Sunny': '☀️', 'Cloudy': '☁️', 'Rainy': '🌧️', 'Clear': '☀️'}
boxes_html_list = []

for _, row_pred in day_pred.iterrows():
    match = day_weather[day_weather['time'] == row_pred['time']]
    if not match.empty:
        hour_data = match.iloc[0]
        hour_str = row_pred['time'].strftime('%I:%M %p')
        condition = row_pred['Predicted_Weather']
        emoji = weather_emoji.get(condition, '❓')

        box_html = f"""
            <div class='hour-box-vertical'>
                <h4>{hour_str}</h4>
                <div class='weather-info'>
                    {emoji} {condition}<br>
                    🌡️ Temp: {hour_data['temperature_2m']:.1f}°C<br>
                    💧 Hum: {hour_data['relative_humidity_2m']:.0f}%<br>
                    🧭 Press: {hour_data['pressure_msl']:.0f} hPa
                </div>
            </div>
        """
        boxes_html_list.append(box_html.strip())

st.markdown(f"<div class='scroll-box'>{''.join(boxes_html_list)}</div>", unsafe_allow_html=True)

# Line Charts
st.subheader(f"Weather Features for {selected_day}")
col1, col2 = st.columns(2)

with col1:
    fig_temp = px.line(day_weather, x='time', y='temperature_2m', title="Temperature (°C)", markers=True,
                        line_shape='spline', color_discrete_sequence=['#FF6347'])
    st.plotly_chart(fig_temp, use_container_width=True)

    fig_press = px.line(day_weather, x='time', y='pressure_msl', title="Pressure (hPa)", markers=True,
                         line_shape='spline', color_discrete_sequence=['#4682B4'])
    st.plotly_chart(fig_press, use_container_width=True)

with col2:
    fig_hum = px.line(day_weather, x='time', y='relative_humidity_2m', title="Humidity (%)", markers=True,
                     line_shape='spline', color_discrete_sequence=['#20B2AA'])
    st.plotly_chart(fig_hum, use_container_width=True)

    fig_wind = px.line(day_weather, x='time', y='windspeed_10m', title="Wind Speed (km/h)", markers=True,
                        line_shape='spline', color_discrete_sequence=['#8A2BE2'])
    st.plotly_chart(fig_wind, use_container_width=True)

# Sidebar for news
st.sidebar.subheader("Recent Weather/Climate News (This take some time to load 😊)")

# Apply custom CSS to the sidebar
st.sidebar.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: black;
        color: white;
    }
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5, [data-testid="stSidebar"] h6 {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Store news items in session state
if 'news_items' not in st.session_state:
    st.session_state.news_items = []

# Fetch and format news on first load
if not st.session_state.news_items:
    news_prompt = f"Give me 5 very short recent (within the last 7 days) news items about weather or climate in {selected_city} or in India, focusing on agricultural or general climate impacts. If there is a title, put it in bold with **title**."
    news_response = chatbot.get_ai_response(news_prompt, "")
    if news_response:
        lines = news_response.strip().split("\n")

        # Remove the first paragraph (non-news intro)
        if lines and not re.match(r"\d\.", lines[0]):
            while lines and not re.match(r"\d\.", lines[0]):
                lines.pop(0)

        st.session_state.news_items = []
        for line in lines:
            line = line.strip()
            if line:
                # Replace any **bold text** with light blue HTML bold
                line = re.sub(r"\*\*(.*?)\*\*", r"<strong style='color: lightblue;'>\1</strong>", line)
                # Remove s from the end of the line if it's there.
                line = line.rstrip('s')
                st.session_state.news_items.append(line)

# Display news items in styled containers
for news_item in st.session_state.news_items:
    st.sidebar.markdown(
        f"<div style='border: 1px solid #e0e0e0; padding: 10px; margin-bottom: 10px; border-radius: 20px; color: white;'>{news_item}</div>",
        unsafe_allow_html=True,
    )

# Chat section
if st.session_state.show_chat:
    prompt = chatbot.display_chat_ui()

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.text(prompt)

        # Create context from weather data
        if not current_hour_weather.empty and not current_hour_pred.empty:
            weather_context = f"""
            Current weather in {selected_city} on {selected_day}:
            Time: {india_time.strftime('%A, %d %B %Y %I:%M %p')} (IST)
            Condition: {cur_pred['Predicted_Weather']}
            Temperature: {cur_weather['temperature_2m']:.1f}°C
            Humidity: {cur_weather['relative_humidity_2m']:.0f}%
            Pressure: {cur_weather['pressure_msl']:.0f} hPa
            Wind Speed: {cur_weather['windspeed_10m']:.1f} km/h
            """
        else:
            weather_context = f"No current weather data available for {selected_city} on {selected_day}."

        ai_message = chatbot.get_ai_response(prompt, weather_context)
        st.session_state.messages.append({"role": "assistant", "content": ai_message})
        with st.chat_message("assistant"):
            st.write(ai_message)
