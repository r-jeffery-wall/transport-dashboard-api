import os
from datetime import date, datetime, timedelta
import math
from PIL import Image, ImageDraw, ImageFont

# This module will handle the drawing of the final image from the JSON data.

img_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img')

# Fonts
font24 = ImageFont.truetype(os.path.join(img_dir, 'Font.ttc'), 24)
font16 = ImageFont.truetype(os.path.join(img_dir, 'Font.ttc'), 16)
font14 = ImageFont.truetype(os.path.join(img_dir, 'Font.ttc'), 14)
font12 = ImageFont.truetype(os.path.join(img_dir, 'Font.ttc'), 12)

# Colours
white = (255, 255, 255)
black = (0, 0, 0)

# Images
lunderground = Image.open(os.path.join(img_dir, 'LondonUnderground.png'))
nat_rail = Image.open(os.path.join(img_dir, 'NatRail.png'))
bus = Image.open(os.path.join(img_dir, 'bus.png'))
walking = Image.open(os.path.join(img_dir, 'walking.png'))

def draw_dashboard(JSON_data):
    width, height = JSON_data['width'], JSON_data['height']
    dashboard = Image.new('RGB', (width, height), white) # The base image is a white background with the specified height and width.
    draw = ImageDraw.Draw(dashboard)

    # Set up basic layout.
    # Layout coordinate variables
    status_line = (0, math.floor(height * 0.2), width, math.floor(height * 0.2))
    weather_divider = (math.floor(width * 0.65), 0, math.floor(width * 0.65), math.floor(height * 0.2))
    grid_vertical = (math.floor(width / 2), math.floor(height * 0.2), math.floor(width / 2), height)
    grid_horizontal = (0, math.floor(height * 0.6), width, math.floor(height * 0.6))
    date_time_pos = (5, math.floor(height * 0.1))
    stop_dimensions = (math.floor(width / 2) - 2, math.floor(height * 0.4) - 2)
    weather_dimensions = (math.floor(width * 0.35) - 2, math.floor(height * 0.2) - 2)
    stop_1 = (0, status_line[1] + 2) 
    stop_2 = (grid_vertical[0] + 2, status_line[1] + 2)
    stop_3 = (0, grid_horizontal[1] + 2)
    stop_4 = (grid_vertical[0] + 2, grid_horizontal[1] + 2)
    
    # Draw layout
    draw.line(status_line, fill=0, width=2)
    draw.line(weather_divider, fill=0, width=2)
    draw.line(grid_vertical, fill=0, width=2)
    draw.line(grid_horizontal, fill=0, width=2)

    # Print Date and Time
    draw.text(date_time_pos, text=JSON_data['date_time'], font=font24, anchor="lm", fill=black)

    #Print weather
    dashboard.paste(draw_weather(weather_dimensions, JSON_data['weather']), (weather_divider[0] + 2, 0))

    # Stop 1
    dashboard.paste(draw_departure_information_for_stop(stop_dimensions, JSON_data['stops'][0]), stop_1)

    # Stop 2
    dashboard.paste(draw_departure_information_for_stop(stop_dimensions, JSON_data['stops'][1]), stop_2)

    # Stop 3
    dashboard.paste(draw_departure_information_for_stop(stop_dimensions, JSON_data['stops'][2]), stop_3)

    # Stop 4
    dashboard.paste(draw_departure_information_for_stop(stop_dimensions, JSON_data['stops'][3]), stop_4)

    dashboard.save('dashboard.png')

    return 

def draw_weather(dimensions,weather_settings):
    weather = Image.new('RGB', dimensions, white)
    draw = ImageDraw.Draw(weather)
    image = Image.open(os.path.join(img_dir, "OpenWeather", f"{weather_settings['weather_icon']}.png"))

    draw.text((10, 15), text=weather_settings['location'], font=font16, anchor="lm", fill=black)
    weather.paste(image, (75, 25))
    draw.text((160, 50), text=str(weather_settings['temp']) + '°C', font=font16, anchor="lm", fill=black)
    draw.text((100, 80), text=weather_settings['weather'], font=font12, anchor='mm', fill=black)

    return weather

def draw_departure_information_for_stop(dimensions, stop): # This function takes a starting x/y coordinate and handles the drawing of one of the four sections of the stop grid.
    departure_info = Image.new('RGB', dimensions, white)
    draw = ImageDraw.Draw(departure_info)
    #Variables
    header_line = (0, math.floor(dimensions[1] * 0.21), dimensions[0], math.floor(dimensions[1] * 0.21))
    header_dimensions = (dimensions[0], math.floor(dimensions[1] * 0.2))
    departures_start_x = 3
    departures_start_y = header_line[1] + 8
    # Draw basic layout.
    draw.line(header_line, fill=0, width=2)

    if not stop:
        draw.text((5, 20), text="No stop information provided!", font=font14, anchor='lm', fill=black)
    elif stop['type'] == 'train':
        departure_info.paste(draw_station_header(header_dimensions, stop['name'], stop['time_to_walk'], nat_rail), (0, 0))
        if len(stop['departures']) == 0:
            departure_info.paste(no_departures(header_dimensions), (departures_start_x, departures_start_y))
        departure_y = departures_start_y
        for departure in stop['departures']:
            draw_departure(draw, departure_info, departures_start_x, departure_y, departure.operator, departure.destination, check_departure_with_walking_time(departure.departure_time, stop['time_to_walk']), departure.departure_time)
            departure_y += 15
    elif stop['type'] == 'tfl_bus':
        departure_info.paste(draw_station_header(header_dimensions, stop['name'], stop['time_to_walk'] ,bus), (0, 0))
        if len(stop['departures']) == 0:
            departure_info.paste(no_departures(header_dimensions), (departures_start_x, departures_start_y))
        departure_y = departures_start_y
        for departure in stop['departures']:
            draw_departure(draw, departure_info, departures_start_x, departure_y, departure.line, departure.destination, check_departure_with_walking_time(departure.time_to_arrival, stop['time_to_walk']), departure.time_to_arrival)
            departure_y += 15
    elif stop['type'] == 'tfl_tube':
        departure_info.paste(draw_station_header(header_dimensions, stop['name'], stop['time_to_walk'],lunderground), (0, 0))
        if len(stop['departures']) == 0:
            departure_info.paste(no_departures(header_dimensions), (departures_start_x, departures_start_y))
        departure_y = departures_start_y
        for departure in stop['departures']:
            draw_departure(draw, departure_info, departures_start_x, departure_y, departure.line, departure.destination, check_departure_with_walking_time(departure.time_to_arrival, stop['time_to_walk']), departure.time_to_arrival)
            departure_y += 15
        

    return departure_info

def no_departures(dimensions):
    message = Image.new('RGB', dimensions, white)
    draw = ImageDraw.Draw(message)

    draw.text((3, 10), text="There are currently no scheduled departures!", font=font14, anchor="lm", fill=black)

    return message

def draw_station_header(dimensions, station_name, time_to_station, logo):
    header = Image.new('RGB', dimensions, white)
    draw = ImageDraw.Draw(header)

    draw.text((5, 20), text=station_name, font=font16, anchor='lm', fill=black)
    draw.text((215, 20), text=time_to_station, font=font16, anchor='lm', fill=black)
    header.paste(walking, (240, 5))
    header.paste(logo, (280, 5))

    return header

def draw_departure(draw, image, x_pos, y_pos, line, destination, time_warning, time):
    draw.text((x_pos, y_pos), text=line, font=font12, anchor='lm', fill=black)
    draw.text((x_pos + 85, y_pos), text=destination, font=font12, anchor='lm', fill=black)
    if time_warning:
        draw.text((x_pos + 270, y_pos), text='!', font=font12, anchor='lm', fill=black)
    draw.text((x_pos + 280, y_pos), text=time, font=font12, anchor='lm', fill=black)

def check_departure_with_walking_time(departure_time, time_to_walk):
    time_to_walk_timestamp = datetime.now() + timedelta(minutes = int(time_to_walk))
    departure_time_timestamp = parse_departure_time(departure_time)

    if departure_time_timestamp < time_to_walk_timestamp:
        return True # Time warning will be shown
    else:
        return False

# Parses the departure time into a format for time/date comparison.
def parse_departure_time(departure_time):
    if len(departure_time) <= 3: # This means the departure time is not already formatted in HH:MM format.
        if departure_time == 'due':
            return datetime.now()
        else:
            return datetime.now() + timedelta(minutes= int(departure_time))
    else:
        return datetime.strptime(departure_time, '%H:%M')

# For testing
if __name__ == "__main__":
    draw_dashboard({
    "width": 648,
    "height": 480,
        "date_time": "Wednesday 9 October 2024  21:06",
    "weather": {
        "temp": 13,
        "location": "London",
        "weather": "Clouds",
        "weather_icon": "04n"
    },
    "stops": [
        {
            "type": "train",
            "data": {
                "station_name": "Birmingham New Street",
                "station_code": "BHM",
                "departures": [
                    {
                        "operator": "LM",
                        "destination": "Lichfield Trent Valley",
                        "departure_time": "21:08"
                    },
                    {
                        "operator": "VT",
                        "destination": "Crewe",
                        "departure_time": "21:07"
                    },
                    {
                        "operator": "LM",
                        "destination": "Wolverhampton",
                        "departure_time": "21:11"
                    },
                    {
                        "operator": "VT",
                        "destination": "London Euston",
                        "departure_time": "21:27"
                    },
                    {
                        "operator": "XC",
                        "destination": "Bristol Temple Meads",
                        "departure_time": "22:08"
                    },
                    {
                        "operator": "LM",
                        "destination": "Redditch",
                        "departure_time": "21:15"
                    },
                    {
                        "operator": "LM",
                        "destination": "Rugeley Trent Valley",
                        "departure_time": "21:15"
                    },
                    {
                        "operator": "LM",
                        "destination": "Northampton",
                        "departure_time": "21:15"
                    },
                    {
                        "operator": "LM",
                        "destination": "Four Oaks",
                        "departure_time": "21:16"
                    },
                    {
                        "operator": "AW",
                        "destination": "Chester",
                        "departure_time": "21:22"
                    }
                ]
            }
        },
        {
            "type": "tfl_bus",
            "data": {
                "name": "Oxford Circus Station (RG)",
                "departures": [
                    {
                        "line": "22",
                        "destination": "Putney Common",
                        "time_to_arrival": "14"
                    },
                    {
                        "line": "22",
                        "destination": "Putney Common",
                        "time_to_arrival": "2"
                    },
                    {
                        "line": "139",
                        "destination": "Waterloo Station",
                        "time_to_arrival": "20"
                    },
                    {
                        "line": "94",
                        "destination": "Piccadilly Circus",
                        "time_to_arrival": "21"
                    },
                    {
                        "line": "94",
                        "destination": "Piccadilly Circus",
                        "time_to_arrival": "24"
                    },
                    {
                        "line": "22",
                        "destination": "Putney Common",
                        "time_to_arrival": "25"
                    },
                    {
                        "line": "94",
                        "destination": "Piccadilly Circus",
                        "time_to_arrival": "27"
                    },
                    {
                        "line": "139",
                        "destination": "Waterloo Station",
                        "time_to_arrival": "6"
                    },
                    {
                        "line": "94",
                        "destination": "Oxford Circus",
                        "time_to_arrival": "6"
                    }
                ]
            }
        },
        {
            "type": "tfl_tube",
            "data": {
                "name": "Oval ",
                "departures": []
            }
        }
    ]
})
