import os
import logging
import json
import requests
#import epd5in83_V2
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

host = "localhost:8000" #TODO: implement host in env vars.

def main(): # Settings for the query will be stored locally in a JSON file.
    with open("./settings.json") as file:
        settings = json.load(file)

    # Getting API data.
    image = requests.post(f"http://{host}/SVG", json=settings)
    return image

# For testing:
if __name__ == "__main__":
    print(main())
