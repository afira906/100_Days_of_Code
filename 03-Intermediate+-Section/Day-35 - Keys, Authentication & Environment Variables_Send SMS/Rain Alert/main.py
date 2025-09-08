import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# Load environment variables from .env file
load_dotenv()

OWM_endpoint = os.getenv("OWM_ENDPOINT")
api_key = os.getenv("OWM_API_KEY")
Account_SID = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

weather_params = {
    "lat": 30.8782,
    "lon":  73.5954,
    "appid": api_key,
    "cnt": 4
}

response = requests.get(OWM_endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

# print(weather_data["list"][0]["weather"][0]["id"])

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    proxy_client = TwilioHttpClient()
    https_proxy = os.environ.get('https_proxy')

    try:
        client = Client(Account_SID, auth_token)
        message = client.messages.create(
            body="It's going to rain today. Remember to bring an ☂️.",
            from_="",
            to=""
        )
        print(f"Message status: {message.status}")
    except Exception as e:
        print(f"Error sending message: {e}")
