from io import BytesIO
import os
import logging
import json
import time
import requests
from dotenv import load_dotenv
import epd5in83_V2
from PIL import Image, ImageDraw

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

host = os.environ['HOST'] #TODO: implement host in env vars.

def request_image(settings):
    logging.info("Making API request...")
    image = requests.post(f"http://{host}/PNG", json=settings)

    response = Image.open(BytesIO(image.content))

    return response

def draw_display(image):
    epd = epd5in83_V2.EPD()
    logging.info("Drawing base image...")
    background = Image.new('1', (epd.width, epd.height), 255)

    background.paste(image, (0, 0, epd.width, epd.height))

    return background

def draw_error():
    epd = epd5in83_V2.EPD()
    logging.info("An error occurred, writing error message.")
    error = Image.new('1', (epd.width, epd.height), 255)

    draw = ImageDraw.Draw(error)

    draw.text((10, 10), text="An error occured getting the dashboard image from the API :(", anchor="lm")

    return error

def draw_to_display(image):
    logging.info("Initialising and clearing display.")
    epd = epd5in83_V2.EPD()

    epd.init()
    epd.Clear()
    time.sleep(1)
    epd.init()

    logging.info("Drawing image from API to display...")
    epd.display(epd.getbuffer(image))
    time.sleep(2)

    logging.info("Display goes to sleep...")
    epd.sleep()

    return

def main(): # Settings for the query will be stored locally in a JSON file.
    logging.info("Reading settings.json...")
    with open("./settings.json") as file:
        settings = json.load(file)

    try: # This blocks handles the creation of the image for the display.
        dashboard_image = request_image(settings)
    except:
        image = draw_error()
    else:
        image = draw_display(dashboard_image)
    finally:
        draw_to_display(image)


    return

if __name__ == "__main__":
    main()
