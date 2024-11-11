from dataclasses import dataclass
from dotenv import load_dotenv
import requests
import os

@dataclass
class TrainArrival(object):
    operator: str
    destination: str
    departure_time: str

load_dotenv()
# Env variables
base_url = "https://api.rtt.io/api/v1/json/search/"
api_username = os.environ["RTT_API_USERNAME"]
api_password = os.environ["RTT_API_PASSWORD"]

def format_departure_time(time):
    return f"{time[:2]}:{time[2:]}"

def get_train_station_name(station):
    request_url = base_url + station

    request = requests.get(request_url, auth=(api_username, api_password))
    data = request.json()

    return data["location"]["name"]

def get_train_departures_for_station_code(station):
    request_url = base_url + station

    request = requests.get(request_url, auth=(api_username, api_password))
    data = request.json()

    return parse_train_departure_json(data)


def parse_train_departure_json(json): #Parses the JSON data from RTT api into an object.
    departures = []

    for arrival in json["services"]:
        if len(departures) >= 10: # Setting a max size for the departures list.
            break
        if not arrival["isPassenger"]: # Non-passenger services are skipped
            continue
        if arrival["serviceType"] == "train":
            operator_name = arrival["atocCode"]
            destination = arrival["locationDetail"]["destination"][0]["description"]
            departure_time = format_departure_time(arrival["locationDetail"]["realtimeDeparture"])
        elif arrival["serviceType"] == "bus":
            operator_name = "Bus"
            destination = arrival["locationDetail"]["destination"][0]["description"]
            departure_time = format_departure_time(arrival["locationDetail"]["gbttBookedDeparture"])
        else: # 'serviceType' is not recognised. Functionality of this will need to be fleshed out.
            continue

        departures.append(TrainArrival(operator_name, destination, departure_time))

    return departures

# For testing
if __name__ == "__main__":
    print(get_train_departures_for_station_code("BHM"))
