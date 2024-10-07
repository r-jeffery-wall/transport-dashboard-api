import drawsvg as draw

# This module will handle the drawing of the final image from the JSON data.

def draw_dashboard(JSON_data):
    width, height = JSON_data['width'], JSON_data['height']
    dashboard = draw.Drawing(width, height, origin='top-left')

    # Set up basic layout.
    # Variables
    status_line = (0, height * 0.2, width, height * 0.2)
    weather_divider = (width * 0.55, 0, width * 0.55, height * 0.2)
    grid_vertical = (width / 2, height * 0.2, width / 2, height)
    grid_horizontal = (0, height / 2, width, height / 2)
    date_time_y = height * 0.1
    # Draw layout
    dashboard.append(draw.Line(status_line[0], status_line[1], status_line[2], status_line[3], stroke='black', stroke_width=2))
    dashboard.append(draw.Line(weather_divider[0], weather_divider[1], weather_divider[2], weather_divider[3], stroke='black', stroke_width=2))
    dashboard.append(draw.Line(grid_vertical[0], grid_vertical[1], grid_vertical[2], grid_vertical[3], stroke='black', stroke_width=2))
    dashboard.append(draw.Line(grid_horizontal[0], grid_horizontal[1], grid_horizontal[2], grid_horizontal[3], stroke='black', stroke_width=2))

    # Print Date and Time
    dashboard.append(draw.Text(JSON_data['date_time'], 24, 5, date_time_y, text_anchor='start', fill='black'))


    dashboard.save_svg('dashboard.svg')
    return 

