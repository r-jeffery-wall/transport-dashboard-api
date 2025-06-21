from dataclasses import dataclass
from datetime import datetime, timedelta
import requests

@dataclass
class TfLArrival(object):
    line: str
    destination: str
    time_to_arrival: str

# API variables
base_url = "https://api.tfl.gov.uk/StopPoint/"

# This module contains common functions for accessing the TfL API.
def get_tfl_departures(stop):
    request_url = base_url + stop + "/Arrivals"

    request = requests.get(request_url)
    data = request.json()

    data.sort(key=lambda x: x['timeToStation'], reverse=False) # This sorts the list in ascending order by arrival time.

    return parse_departure_json(data)


def parse_departure_json(json): #Parses the JSON data from TFL API into an object.
    arrivals = []

    for prediction in json:
        arrivals.append(TfLArrival(prediction["lineName"], format_destination_name(prediction["destinationName"]), format_predicted_time(prediction["timeToStation"])))


    return arrivals

def format_destination_name(name):
    if "Underground Station" in name:
        return name[:-19]
    elif "Rail Station" in name:
        return name[:-12]
    else:
        return name

def format_predicted_time(arrival_time):
    arrival_minutes = int(arrival_time / 60)

    if arrival_minutes == 0:
        return "due"
    elif arrival_minutes < 30: # Predicted arrivals sooner than 30 minutes are displayed as minutes, longer than that will display a timestamp.
        return str(arrival_minutes)
    else:
        current_time = datetime.now()
        return (current_time + timedelta(minutes=arrival_minutes)).strftime('%H:%M')

def get_tfl_latlong(stop):
    request_url = base_url + stop

    request = requests.get(request_url)
    data = request.json()

    return f"{data['lon']},{data['lat']}"

# For testing:
if __name__ == "__main__":
    print("Bus:")
    print(get_tfl_departures("490000173RG"))
    print("Tube:")
    print(get_tfl_departures("940GZZLUOVL"))
