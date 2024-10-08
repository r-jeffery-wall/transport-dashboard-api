import drawsvg as draw

# This module will handle the drawing of the final image from the JSON data.

def draw_dashboard(JSON_data):
    width, height = JSON_data['width'], JSON_data['height']
    dashboard = draw.Drawing(width, height, origin='top-left')

    # Set up basic layout.
    # Variables
    status_line = (0, height * 0.2, width, height * 0.2)
    weather_divider = (width * 0.65, 0, width * 0.65, height * 0.2)
    grid_vertical = (width / 2, height * 0.2, width / 2, height)
    grid_horizontal = (0, height * 0.6, width, height * 0.6)
    date_time_y = height * 0.1
    stop_1 = (0, status_line[1] + 2) 
    # Draw layout
    dashboard.append(draw.Line(status_line[0], status_line[1], status_line[2], status_line[3], stroke='black', stroke_width=2))
    dashboard.append(draw.Line(weather_divider[0], weather_divider[1], weather_divider[2], weather_divider[3], stroke='black', stroke_width=2))
    dashboard.append(draw.Line(grid_vertical[0], grid_vertical[1], grid_vertical[2], grid_vertical[3], stroke='black', stroke_width=2))
    dashboard.append(draw.Line(grid_horizontal[0], grid_horizontal[1], grid_horizontal[2], grid_horizontal[3], stroke='black', stroke_width=2))

    # Print Date and Time
    dashboard.append(draw.Text(JSON_data['date_time'], 24, 5, date_time_y, text_anchor='start', fill='black'))

    #Print weather
    dashboard.append(draw_weather(weather_divider[0], JSON_data['weather']))

    # Stop 1
    dashboard.append(draw_departure_information_for_stop(stop_1[0], stop_1[1], JSON_data['stops'][0]))
    dashboard.save_svg('dashboard.svg')
    return 

def draw_weather(weather_divider_pos,weather_settings):
    weather = draw.Group(fill='black')

    weather.append(draw.Text(weather_settings['location'], 16, weather_divider_pos + 60, 20, text_anchor='center'))
    weather.append(draw.Image(weather_divider_pos + 75, 15, 64, 64, path=f"http://openweathermap.org/img/w/{weather_settings['weather_icon']}.png"))
    weather.append(draw.Text(str(weather_settings['temp']) + '°C', 16, weather_divider_pos + 160, 50, text_anchor='start'))
    weather.append(draw.Text(weather_settings['weather'], 12, weather_divider_pos + 110, 80, text_anchor='center'))

    return weather

def draw_departure_information_for_stop(start_x, start_y, stop): # This function takes a starting x/y coordinate and handles the drawing of one of the four sections of the stop grid.
    departure_info = draw.Group(fill='black')
    #Variables
    header_line = (start_x, start_y + 30, start_x + 324, start_y + 30)
    departures_start_x = start_x + 3
    departures_start_y = header_line[1] + 17
    # Draw basic layout.
    departure_info.append(draw.Line(header_line[0], header_line[1], header_line[2], header_line[3], stroke='black', stroke_width=2))

    if stop['type'] == 'train':
        departure_info.append(draw_station_header(start_x + 5, start_y + 20, stop['data'].station_name, "https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-thumbnail/s3/042012/500px-national_rail_logo.svg_.png?itok=pKr_e9Hq"))
        departure_y = departures_start_y
        for departure in stop['data'].departures:
            departure_info.append(draw_departure(departures_start_x, departure_y, departure.operator, departure.destination, departure.departure_time))
            departure_y += 15

        

    return departure_info


def draw_station_header(x_pos, y_pos, station_name, path_to_logo):
    header = draw.Group(fill='black')

    header.append(draw.Text(station_name, 16, x_pos, y_pos, text_anchor='start'))
    header.append(draw.Image(x_pos + 295, y_pos - 20, 28, 28, path=path_to_logo))

    return header

def draw_departure(x_pos, y_pos, line, destination, time):
    departure = draw.Group(fill='black')

    departure.append(draw.Text(line, 12, x_pos, y_pos, text_anchor='start'))
    departure.append(draw.Text(destination, 12, x_pos + 125, y_pos, text_anchor='start'))
    departure.append(draw.Text(time, 12, x_pos + 280, y_pos, text_anchor='start'))

    return departure

# For testing
if __name__ == "__main__":
    draw_dashboard({
    "width": 648,
    "height": 480,
    "date_time": "Tuesday 8 October 2024  20:09",
    "weather": {
        "temp": 14,
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
                        "departure_time": "20:22"
                    },
                    {
                        "operator": "LM",
                        "destination": "Wolverhampton",
                        "departure_time": "20:11"
                    },
                    {
                        "operator": "XC",
                        "destination": "Plymouth",
                        "departure_time": "20:12"
                    },
                    {
                        "operator": "LM",
                        "destination": "Rugeley Trent Valley",
                        "departure_time": "20:15"
                    },
                    {
                        "operator": "LM",
                        "destination": "Redditch",
                        "departure_time": "20:15"
                    },
                    {
                        "operator": "LM",
                        "destination": "Four Oaks",
                        "departure_time": "20:16"
                    },
                    {
                        "operator": "VT",
                        "destination": "London Euston",
                        "departure_time": "20:21"
                    },
                    {
                        "operator": "XC",
                        "destination": "Cambridge",
                        "departure_time": "20:22"
                    },
                    {
                        "operator": "AW",
                        "destination": "Aberystwyth",
                        "departure_time": "20:22"
                    },
                    {
                        "operator": "LM",
                        "destination": "Bromsgrove",
                        "departure_time": "20:23"
                    }
                ]
            }
        }
    ]
})
