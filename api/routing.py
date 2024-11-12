import requests
from dotenv import load_dotenv
import math
import os

# Env variables
load_dotenv()
api_key = os.environ["OPENROUTE_TOKEN"]

# API variables
base_url = f"https://api.openrouteservice.org/v2/directions/foot-walking?api_key={api_key}"


def get_travel_time_between_points(latlong_start, latlong_end):
    request_url = f"{base_url}&start={latlong_start}&end={latlong_end}"

    request = requests.get(request_url)
    data = request.json()

    time_seconds = data['features'][0]['properties']['summary']['duration']
    return str(round(time_seconds / 60))
# For testing
if __name__ == "__main__":
    print(get_travel_time_between_points("8.681495,49.41461", "8.687872,49.420318"))
