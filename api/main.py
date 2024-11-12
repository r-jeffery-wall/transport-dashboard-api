from fastapi import FastAPI
from typing import List
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

from .api_getters import main_api_getters
from ..draw.img_generator import draw_dashboard

app = FastAPI()

class StopDetails(BaseModel):
    stop_type: str
    id: str
    coordinates: str | None

class RawDataSettings(BaseModel):
    lat_long: str
    stops: List[StopDetails]

class SVGSettings(BaseModel):
    width: int
    height: int
    lat_long: str
    stops: List[StopDetails]

@app.get("/")
async def root():
    return HTMLResponse("""
    <h1>Transport Dashboard API</h1>
    <p>This API generates data for a transport dashboard by pulling data from various transport APIs and generating an SVG file that can be displayed on various displays.</p>
    <p>There are two endpoints: '/RawData' and '/PNG'. The first pulls data in JSON format that you can do what you like with, the second generates an PNG for display. Both endpoints respond to POST requests with the following request schema: </p>
    <pre>
    <code>
    {
        "width": #The width of the SVG image to be displayed. (not needed for RawData requests)
        "height": #The height of the SVG image to be displayed. (not needed for RawData requests)
        "latlong": #The coordinates for the weather display.
        "stops": [ # A list containing the stops that you want to be displayed on the dashboard (max 4)
            {
                "stop_type": #The type of the stop. For available types, see the GitHub Readme.
                "id": # The ID of the stop to pull, this will depend on the stop type. See the GitHub Readme.
            }
        ]
    }
    </code>
    </pre>
    """)

@app.post("/RawData")
async def get_data(query_settings: RawDataSettings):
    return main_api_getters(query_settings)

@app.post("/PNG")
async def generate_svg(query_settings: SVGSettings):
    main_data = main_api_getters(query_settings)
    request_data = {
        'width': query_settings.width,
        'height': query_settings.height,
        'date_time': main_data['date_time'],
        'weather': main_data['weather'],
        'stops': main_data['stops']
    }
    draw_dashboard(request_data) #This creates an SVG file in the current directory called 'dashboard.png'
    return FileResponse('dashboard.png', media_type='image/png')

