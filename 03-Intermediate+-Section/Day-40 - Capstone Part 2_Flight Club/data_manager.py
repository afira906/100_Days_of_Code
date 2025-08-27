import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/02ff33c093786110d13fb8e164230c81/flightDeals/prices"
SHEETY_USERS_ENDPOINT="https://api.sheety.co/02ff33c093786110d13fb8e164230c81/flightDeals/users"


class DataManager:

    def __init__(self):
        self.sheety_api_key = os.getenv("SHEETY_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.sheety_api_key}"
        }
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=self.headers)
        data = response.json()
        # print(data)
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            try:
                response = requests.put(
                    url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                    json=new_data,
                    headers=self.headers
                )
                response.raise_for_status()
            except Exception as e:
                print(f"Failed to update {city['city']}: {e}")

    def get_customer_emails(self):
        response = requests.get(url=SHEETY_USERS_ENDPOINT, headers=self.headers)
        data = response.json()
        # print(data)
        self.customer_data = data["users"]
        return self.customer_data
