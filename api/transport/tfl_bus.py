import requests

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

# For testing:
if __name__ == "__main__":
    print(get_bus_stop_name("490000173RG"))
