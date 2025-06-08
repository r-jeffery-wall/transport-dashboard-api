import requests

# API variables
base_url = "https://api.tfl.gov.uk/StopPoint/"

# The Stop ID can be found using https://api.tfl.gov.uk/StopPoint/Search/{StopName}

def get_tube_station_name(stop):
    request_url = base_url + stop

    request = requests.get(request_url)
    data = request.json()

    if "Undergound Station" in data["commonName"]:
        return data["commonName"][:-19] # The TfL API appends 'Undergound Station' to tube station names. We don't want this so remove it from the string returned from the API.
    elif "Rail Station" in data["commonName"]:
        return data["commonName"][:12]
    else:
        return data["commonName"]

# For testing:
if __name__ == "__main__":
    print(get_tube_station_name("940GZZLUOVL"))
