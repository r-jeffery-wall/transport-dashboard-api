from fastapi import FastAPI
from typing import List
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
    return {"message": "Hello World"}

@app.post("/")
async def get_data(query_settings: Settings):
    return main_api_getters(query_settings)
