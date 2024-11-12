from .routing import get_travel_time_between_points
from .transport.tfl_bus import get_bus_stop_name
from .transport.tfl_common import get_tfl_departures, get_tfl_latlong
from .transport.tfl_tube import get_tube_station_name
from .transport.rtt_train import get_train_departures_for_station_code, get_train_station_name
from .date_time import get_date_time_string
from .weather import get_weather_data_for_latlong
import json


# Gets cached stop info
with open('./stop_info_cache.json', 'r') as file:
    data  = json.load(file)
    cache = data['cache']

def main_api_getters(settings): # This function will take the API request and return the JSON data that will be used to generate the SVG.
    lat, long = settings.lat_long.split(", ")
    lat_long_for_routing = f"{long},{lat}"
    stops = [get_stop_data(stop, lat_long_for_routing) for stop in settings.stops]
    write_cache_to_file(cache)

    return {
        "date_time": get_date_time_string(),
        "weather": get_weather_data_for_latlong(lat, long),
        "stops": stops
    }

def get_stop_data(stop, routing_start_point): #Takes a stop object and grabs the data from the relevant API.
    # We first need to check if the stop exists in the already cached stop information
    found_stop =  find_stop_in_cache(stop.id)
    if found_stop:
        stop_info = found_stop

        return {**stop_info, "departures": get_departures_for_stop(stop.id, stop.stop_type)}
    # If the stop is not in the cache we will call the API to get the information and then write it to the cache file.
    # We will determine what API to use based on the 'type' variable of the stop.
    else:
        return get_stop_data_and_cache(stop, routing_start_point)
        

def get_stop_data_and_cache(stop, routing_start_point):
    if stop.stop_type == 'train':
            stop_info = {
                "type": 'train',
                "id": stop.id,
                "name": get_train_station_name(stop.id),
                "time_to_walk": get_travel_time_between_points(routing_start_point, stop.coordinates)
            }
            cache.append(stop_info)

            stop_info_with_departures = {**stop_info, "departures": get_train_departures_for_station_code(stop.id)}
            return stop_info_with_departures
    elif stop.stop_type == 'tfl_bus':
        stop_info = {
            'type': 'tfl_bus',
            "id": stop.id,
            "name": get_bus_stop_name(stop.id),
            "time_to_walk": get_travel_time_between_points(routing_start_point, get_tfl_latlong(stop.id))
        }
        cache.append(stop_info)

        stop_info_with_departures = {**stop_info, "departures": get_tfl_departures(stop.id)}
        return stop_info_with_departures

    elif stop.stop_type == 'tfl_tube':
        stop_info = {
            'type': 'tfl_tube',
            "id": stop.id,
            "name": get_tube_station_name(stop.id),
            "time_to_walk": get_travel_time_between_points(routing_start_point, get_tfl_latlong(stop.id))
        }
        cache.append(stop_info)

        stop_info_with_departures = {**stop_info, "departures": get_tfl_departures(stop.id)}
        return stop_info_with_departures

    # We can continue adding other types of stop here...
    else:
        return {
            'type': 'error',
            'data': {
                'message': 'Stop type is not recognised!'
            }
    }

def get_departures_for_stop(id, type):
    if type == 'train':
        return get_train_departures_for_station_code(id)
    elif type == 'tfl_bus' or type == 'tfl_tube':
        return get_tfl_departures(id)
    

def find_stop_in_cache(id):
    for stop in cache:
        if stop['id'] == id:
            return stop
    else:
        return None

def write_cache_to_file(cache):
    output = json.dumps({
        "cache": cache
    })
    with open('stop_info_cache.json', 'w') as outfile:
        outfile.write(output)

# For testing:
if __name__ == "__main__":
    print(cache)
    print(main_api_getters({
        "lat_long": "51.501349, -0.141668",
        "stops": [{
            'stop_type': 'train',
            'id': 'BHM'
        },
        {
            'stop_type': 'tfl_bus',
            'id': '490000173RG'
        },
        {
            'stop_type': 'tfl_tube',
            'id': '940GZZLUOVL'
        }]
    }))
