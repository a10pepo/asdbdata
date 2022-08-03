from FlightRadar24.api import FlightRadar24API, Flight
import numpy as np
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError
import asyncio
from aiohttp import ClientSession
from flightradar_client.fr24feed_flights import FlightradarFlightsFeed
import requests

fr_api = FlightRadar24API()






def get_airports():
    airports = fr_api.get_airports()

def get_flights():
    flights = fr_api.get_flights()
    for flight in flights:
        print(flight)

def get_flight_info(flight_code):
    data=np.random.rand(20,1)
    flight=Flight("123",data)
    details = fr_api.get_flight_details(flight_code)
    flight.set_flight_details(details)
    return f"FROM: {flight.origin_airport_name} TO: {flight.destination_airport_name} alt: {flight.altitude}"

def get_data(flight_code):
    url=f"https://www.flightradar24.com/v1/search/web/find?query={flight_code}&limit=1"
    x = requests.get(url)
    return x.json()['results'][0]


async def main() -> None:
    async with ClientSession() as websession:
        # Home Coordinates: Latitude: -33.5, Longitude: 151.5
        feed = FlightradarFlightsFeed((39.4831, -0.3758), websession,hostname="192.168.1.37")
        status, entries = await feed.update()
        if status=="OK":
            for entry in entries:
                if len(entries[entry]._data["callsign"])>0:
                    data=get_data(entries[entry]._data["callsign"])
                    if len(data["id"])==8:
                        print(get_flight_info(data["id"]))
                    

        #get_flights()
        
asyncio.get_event_loop().run_until_complete(main())

