import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

class Weather:
    
    @staticmethod
    def fetchWeather():
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 60.4518,
            "longitude": 22.2666,
            "hourly": ["temperature_2m", "rain", "wind_speed_10m", "uv_index"],
            "wind_speed_unit": "ms",
            "forecast_days": 1
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_rain = hourly.Variables(1).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
        hourly_uv_index = hourly.Variables(3).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
        )}

        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["rain"] = hourly_rain
        hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
        hourly_data["uv_index"] = hourly_uv_index

        hourly_dataframe = pd.DataFrame(data = hourly_data)
        print(hourly_dataframe)

        # Calculate max temperature and its time
        max_temp = hourly_dataframe['temperature_2m'].max()
        max_temp_time = hourly_dataframe.loc[hourly_dataframe['temperature_2m'].idxmax()]['date']

        # Calculate max wind speed and its time
        max_wind_speed = hourly_dataframe['wind_speed_10m'].max()
        max_wind_speed_time = hourly_dataframe.loc[hourly_dataframe['wind_speed_10m'].idxmax()]['date']

        # Calculate max amount of rain and its time
        max_rain = hourly_dataframe['rain'].max()
        max_rain_time = hourly_dataframe.loc[hourly_dataframe['rain'].idxmax()]['date']

        # Calculate max UV index and its time
        max_uv_index = hourly_dataframe['uv_index'].max()
        max_uv_index_time = hourly_dataframe.loc[hourly_dataframe['uv_index'].idxmax()]['date']

        return max_temp, max_temp_time, max_wind_speed, max_wind_speed_time, max_rain, max_rain_time, max_uv_index, max_uv_index_time
        #output_file = "hourly_weather_data.txt"
        #hourly_dataframe.to_csv(output_file, sep='\t', index=False)
        #print(f"Data saved to {output_file}")