import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

USER_NAME = os.environ.get("USER_NAME")
TOKEN = os.environ.get("TOKEN")
GRAPH_ID = os.environ.get("GRAPH_ID")

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USER_NAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USER_NAME}/graphs"

graph_config = {
    "id": GRAPH_ID,
    "name": "Typing Graph",
    "unit": "WPM",
    "type": "int",
    "color": "ajisai"
}

headers = {
    "X-USER-TOKEN": TOKEN
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

pixel_creation_endpoint = f"{pixela_endpoint}/{USER_NAME}/graphs/{GRAPH_ID}"

today = datetime.now()

pixel_params = {
    "date": today.strftime("%Y%m%d"),
    "quantity": input("How many words did you type today?")
}

response = requests.post(url=pixel_creation_endpoint, json=pixel_params, headers=headers)
print(response.text)

# update_endpoint = f"{pixela_endpoint}/{USER_NAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"

# new_pixel_data = {
#     "quantity": "60"
# }

# response = requests.put(url=update_endpoint, json=new_pixel_data, headers=headers)
# print(response)

# response = requests.delete(url=update_endpoint, headers=headers)
# print(response)
