# utils.py

import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_weather_data(lat, lon):
    start_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=120)

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,"
        f"pressure_msl,windspeed_10m,weathercode&timezone=UTC"
        f"&start_date={start_time.date()}&end_date={end_time.date()}"
    )

    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data['hourly'])
    df['time'] = pd.to_datetime(df['time'])
    df = df.sort_values('time').head(120).reset_index(drop=True)
    return df
