import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from tensorflow.keras.models import load_model
import joblib
import os
import pickle
from utils import fetch_weather_data

# Set random seed for reproducibility
np.random.seed(42)
import tensorflow as tf
tf.random.set_seed(42)

# City name to code and coordinates mapping
city_details = {
    "Chennai": (0, 13.0827, 80.2707),
    "Delhi": (1, 28.6139, 77.2090),
    "Mumbai": (2, 19.0760, 72.8777),
    "Bangalore": (3, 12.9716, 77.5946),
    "Hyderabad": (4, 17.3850, 78.4867)
}

# Cache settings
CACHE_FILE = 'weather_cache.pkl'
CACHE_LIFETIME = 3600  # Cache data for 1 hour (3600 seconds)

def load_cached_weather_data():
    # Check if cache file exists
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            cached_data = pickle.load(f)
        
        # Check if cache is still valid (not expired)
        if time.time() - cached_data['timestamp'] < CACHE_LIFETIME:
            return cached_data['weather_data']

    # If no valid cache, fetch fresh data
    return None

def save_weather_data_to_cache(weather_data):
    cached_data = {'weather_data': weather_data, 'timestamp': time.time()}
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cached_data, f)

def run_forecast(city_name="Chennai"):
    if city_name not in city_details:
        raise ValueError("City not supported.")

    city_code, lat, lon = city_details[city_name]

    # ==== Load models ====
    model1 = load_model("model_1_180_rain.h5")
    scaler1 = joblib.load("model_1_180_rain.pkl")

    model2 = load_model("model_2_temp_hum_press.h5")
    scaler2 = joblib.load("model_2_scaler.pkl")

    # ==== Try to load cached weather data ====
    cached_weather = load_cached_weather_data()

    if cached_weather is None:
        # Fetch latest weather data if no valid cache
        print("Fetching fresh weather data...")
        df = fetch_weather_data(lat, lon)
        # Save fetched data to cache for future use
        save_weather_data_to_cache(df)
    else:
        print("Using cached weather data...")
        # Use cached data
        df = cached_weather

    df['city'] = city_code

    # ==== Model 1 - Predict Weather Conditions ====
    X1 = df[['temperature_2m', 'relative_humidity_2m', 'pressure_msl', 'windspeed_10m', 'city']]
    X1_scaled = scaler1.transform(X1)
    X1_input = X1_scaled.reshape(1, 120, 5)

    y_pred_proba = model1.predict(X1_input)
    y_classes = np.argmax(y_pred_proba, axis=-1)[0]
    label_map = {0: "Sunny", 1: "Cloudy", 2: "Rainy"}
    predicted_labels = [label_map[i] for i in y_classes]

    df['Predicted_Weather'] = predicted_labels
    df[['time', 'Predicted_Weather']].to_csv("forecast_weather_condition.csv", index=False)

    # ==== Model 2 - Predict Features ====
    X2 = df[['temperature_2m', 'relative_humidity_2m', 'pressure_msl', 'windspeed_10m', 'city']]
    X2_scaled = scaler2.transform(X2)
    X2_input = X2_scaled.reshape(1, 120, 5)

    predicted_scaled = model2.predict(X2_input)[0]

    # Add city column back before inverse transform
    dummy_city = np.full((120, 1), city_code)
    predicted_full = np.concatenate((predicted_scaled, dummy_city), axis=1)

    predicted_original = scaler2.inverse_transform(predicted_full)[:, :4]
    future_times = pd.date_range(start=df['time'].iloc[0], periods=120, freq='H')

    pred_df = pd.DataFrame(predicted_original, columns=['temperature_2m', 'relative_humidity_2m', 'pressure_msl', 'windspeed_10m'])
    pred_df['time'] = future_times
    pred_df.to_csv("forecast_weather_features.csv", index=False)

