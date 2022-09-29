import requests
import os
from flight_data import FlightData

from dotenv import load_dotenv  # pip install python-dotenv
load_dotenv("<LOCATION OF YOUR ENVIRONMENT VARIABLES FILE CONTAINING API AUTH TOKENS>")

TEQUILA_KIWI_API = os.getenv('TEQUILA_KIWI_API')
TEQUILA_ENDPOINT = 'https://api.tequila.kiwi.com'

class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def get_destinatation_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {'apikey': TEQUILA_KIWI_API}
        query = {
            'term': city_name,
            'location_types': 'airport'
        }
        response = requests.get(url=location_endpoint, params=query, headers=headers)
        code = response.json()['locations'][0]['code']
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time) -> FlightData:
        """Returns object from FlightData class"""

        location_endpoint = f"{TEQUILA_ENDPOINT}"
        headers = {'apikey': TEQUILA_KIWI_API}
        query = {
            'fly_from': origin_city_code,
            'fly_to': destination_city_code,
            'date_from': from_time.strftime("%d/%m/%Y"),
            'date_to': to_time.strftime("%d/%m/%Y"),
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            'flight_type': 'round',
            'max_stopovers': 0,
            'one_for_city': 1,
            'curr': 'GBP'
        }

        response = requests.get(url=f"{location_endpoint}/v2/search", headers=headers, params=query)

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}")

            query["max_stopovers"] = 1
            response = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search",
                headers=headers,
                params=query,
            )
            data = response.json()["data"][0]

            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],

                # If there's a stopover, the "route" key value pair will contain a list with 4 items:
                # [origin -> stop_over, stop_over -> destination, destination -> stop_over, stop_over -> origin].
                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"],
                booking_link = data['deep_link']
            )
            return flight_data

        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
                booking_link=data['deep_link']
            )
            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data
