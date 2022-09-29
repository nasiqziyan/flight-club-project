import requests

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/<YOUR 32-CHARACTER ACCOUNT CODE>/flightDeals/prices"
SHEETY_USERS_ENDPOINT = "https://api.sheety.co/<YOUR 32-CHARACTER ACCOUNT CODE>/flightDeals/users"


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        self.destination_data = response.json()['prices']
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            # To update a row in our sheety file that contains a sheet called 'prices', we first create a dictionary
            # called new_data. Then, this API is such that if the sheet is called 'prices', then we point to the sheet
            # via its singular, i.e. 'price' and not 'prices' - even though we first accessed the
            # data using: response.json()['prices'].

            new_data = {

                # For each 'city', we update the column titled 'iataCode' by the typing the key 'iataCode:', and
                # following this by what we want to change it to, i.e. city['iataCode'].
                'price': {
                    'iataCode': city['iataCode']
                }
            }
            # Finally, we make the actual update to the sheet using the kwarg called 'json' and passing the data in.
            response = requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}", json=new_data)

    def get_customer_data(self):
        response = requests.get(url=SHEETY_USERS_ENDPOINT)
        self.customer_data = response.json()["users"]
        return self.customer_data
