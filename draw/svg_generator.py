import drawsvg as draw

# This module will handle the drawing of the final image from the JSON data.

def draw_dashboard(JSON_data):
    width, height = JSON_data['width'], JSON_data['height']
    dashboard = draw.Drawing(width, height, origin='top-left')

    # Print Date and Time
    dashboard.append(draw.Text(JSON_data['date_time'], 24, 0, 15, text_anchor='start', fill='black'))


    dashboard.save_svg('dashboard.svg')
    return 

