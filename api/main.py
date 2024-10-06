from fastapi import FastAPI
from typing import List
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from api_getters import main_api_getters

app = FastAPI()

class StopDetails(BaseModel):
    stop_type: str
    id: str

class Settings(BaseModel):
    lat_long: str
    stops: List[StopDetails]

@app.get("/")
async def root():
    return HTMLResponse("""
    <h1>Transport Dashboard API</h1>
    <p>This API generates data for a transport dashboard by pulling data from various transport APIs and generating an SVG file that can be displayed on various displays.</p>
    <p>There are two endpoints: '/RawData' and '/SVG'. The first pulls data in JSON format that you can do what you like with, the second generates an SVG for display. Both endpoints respond to POST requests with the following request schema: </p>
    <pre>
    <code>
    {
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

@app.post("/")
async def get_data(query_settings: Settings):
    return main_api_getters(query_settings)
