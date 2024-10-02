from transport.tfl_bus import get_bus_stop_name
from transport.tfl_common import get_departures
from transport.tfl_tube import get_tube_station_name
from transport.rtt_train import get_train_departures_for_station_code
from date_time import get_date_time_string
from weather import get_weather_data_for_latlong


def main_api_getters(settings): # This function will take the API request and return the JSON data that will be used to generate the SVG.
    lat, long = settings["lat_long"].split(", ")
    stops = [get_stop_data(**stop) for stop in settings["stops"]]

    return {
        "date_time": get_date_time_string(),
        "weather": get_weather_data_for_latlong(lat, long),
        "stops": stops
    }

def get_stop_data(stop_type, id): #Takes a stop object and grabs the data from the relevant API.
    # We will determine what API to use based on the 'type' variable of the stop.
    print(stop_type, id)
    if stop_type == 'train':
        return {
            "type": 'train',
            "data": get_train_departures_for_station_code(id)
        }
    elif stop_type == 'tfl_bus':
        return {
            'type': 'tfl_bus',
            'data': {
                'name': get_bus_stop_name(id),
                'departures': get_departures(id)
        }
    }
    elif stop_type == 'tfl_tube':
        return {
            'type': 'tfl_tube',
            'data': {
                'name': get_tube_station_name(id),
                'departures': get_departures(id)
        }
    }
    # We can continue adding other types of stop here...
    else:
        return {
            'type': 'error',
            'data': {
                'message': 'Stop type is not recognised!'
            }
        }

# For testing:
if __name__ == "__main__":
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
