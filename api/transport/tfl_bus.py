from dataclasses import dataclass
from datetime import datetime, timedelta
import requests
import json
import os

@dataclass
class BusArrival(object):
    line: str
    destination: str
    time_to_arrival: str

# API variables
base_url = "https://api.tfl.gov.uk/StopPoint/"

# The Stop ID is the NaptanID of the stop, this can be found by using https://api.tfl.gov.uk/StopPoint/Search/{StopName}

def get_bus_stop_name(stop):
    request_url = base_url + stop

    request = requests.get(request_url)
    data = request.json()

    if data["stopLetter"]:
        return f"{data["commonName"]} ({data["stopLetter"]})"
    return data["commonName"]

def get_bus_departures(stop):
    request_url = base_url + stop + "/Arrivals"

    request = requests.get(request_url)
    data = request.json()

    return parse_bus_departure_json(data)


def parse_bus_departure_json(json): #Parses the JSON data from TFL API into an object.
    arrivals = []

    for prediction in json:
        arrivals.append(BusArrival(prediction["lineName"], prediction["destinationName"], format_predicted_time(prediction["timeToStation"])))

    arrivals.sort(key=lambda x: x.time_to_arrival, reverse=False) # This sorts the list in ascending order by arrival time.

    return arrivals

def format_predicted_time(arrival_time):
    arrival_minutes = int(arrival_time / 60)

    if arrival_minutes == 0:
        return "due"
    elif arrival_minutes < 30: # Predicted arrivals sooner than 30 minutes are displayed as minutes, longer than that will display a timestamp.
        return str(arrival_minutes)
    else:
        current_time = datetime.now()
        return (current_time + timedelta(minutes=arrival_minutes)).strftime('%H:%M')

# For testing:
if __name__ == "__main__":
    print(get_bus_stop_name("490000173RG"))
    print(get_bus_departures("490000173RG"))
