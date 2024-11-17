# Transport dashboard API.
This is a [FastAPI](https://fastapi.tiangolo.com/) based API for gathering up-to-date departure information for a selection of public transport stops that generates an image to be displayed on a dashboard-style display (in my case, a Waveshare E-paper display.) The API also uses routing APIs to work out how long it would take you to walk to a particular station and then show warnings for departures that wou won't be able to get to the station in time for. For this reason, it is recommended to only use stations that are nearby to your location. The API takes a POST request containing settings that define the stops for which information should be gathered.

## Running the API.
This repo contains a Dockerfile for building a container in which to run the server on your LAN. It can then be accessed by a variety of displays. In the `display/` folder I have included my code for drawing the display on a Waveshare E-Paper display, but you can write your own code to interface with the API for other displays.

## Endpoints
There are two API endpoints, `/RawData` and `/PNG`. `/RawData` is for requesting raw JSON data of the upcoming departure information, whereas the `/PNG` endpoint will generate a PNG image for display. Both requests take similar request bodies:
```
{
        "width": #The width of the SVG image to be displayed. (not needed for RawData requests)
        "height": #The height of the SVG image to be displayed. (not needed for RawData requests)
        "latlong": #The coordinates for the weather display.
        "stops": [ # A list containing the stops that you want to be displayed on the dashboard (exactly 4)
            {
                "stop_type": #The type of the stop. For available types, see the GitHub Readme.
                "id": # The ID of the stop to pull, this will depend on the stop type. See the GitHub Readme.
                "coordinates": # This field is used to provide coordinates for the location of a stop, where these are not accessible from an API. Currently, this is only needed for National rail stop types.
            }
        ]
    }
```

## Environment Variables / Settings.json
In order for the API to work, your server must have a valid `.env` file, and your client must have a valid `settings.json` file for its queries. An example of both is provided in the repo.

## Third Party APIs
Currently, the API supports gathering data from the [RealTimeTrains API](https://www.realtimetrains.co.uk/about/developer/) for UK rail departures, and the [TfL API](https://api.tfl.gov.uk/) for London bus and Underground departures. The [OpenWeather API](https://openweathermap.org/) is used to provide weather information alognside departures. The [OpenRouteService](https://openrouteservice.org/) API is used for getting estimated walking times to provided stops. All API getters are stored in the `/api/transport/` folder and follow a common structure. I intend to expand the list of available third party APIs, but feel free to add your own using the available files in the repo as a starting point.

## Further Development
This is an ongoing project, and I intend to continue working on the codebase. A list of my priorities for ths codebase is as follows:
- Work on better error-handling for the client and server side applications.
- Add additional API providers for transport data.
- Work on more intelligent image display logic, e.g: intelligently cutting off or wrapping strings based on their length.
