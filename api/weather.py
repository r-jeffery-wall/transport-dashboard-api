from dataclasses import dataclass
from dotenv import load_dotenv
from scipy.constants import convert_temperature
from math import floor
import requests
import json
import os

# Initialise env variables.
load_dotenv()

# API Variables
base_url = "https://api.openweathermap.org/data/2.5/weather"
api_key = os.environ["OPENWEATHER_API_KEY"]

def get_weather_data_for_latlong(lat, lon):
    request_url = f"{base_url}?lat={lat}&lon={lon}&appid={api_key}"

    request = requests.get(request_url)

    data = request.json()

    return {
        "temp": floor(convert_temperature(data["main"]["temp"], 'Kelvin', 'Celsius')),
        "weather": data["weather"][0]["main"],
        "weather_icon": data["weather"][0]["icon"]
    }

# For testing:
if __name__ == "__main__":
    print(get_weather_data_for_latlong("51.501349", "-0.141668"))
