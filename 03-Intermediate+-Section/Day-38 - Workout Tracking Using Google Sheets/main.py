import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

GENDER = "female"
WEIGHT_KG = "52"
HEIGHT_CM = "171"
AGE = "19"

# Your personal data. Used by Nutritionix to calculate calories.
APP_ID = os.environ["ENV_NIX_APP_ID"]
API_KEY = os.environ["ENV_NIX_API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["ENV_SHEETY_ENDPOINT"]
TOKEN = os.environ["ENV_SHEETY_TOKEN"]

exercise_text = input("Tell me which exercises you did: ")

# Nutritionix API Call
headers = {
    "x-app-key": API_KEY,
    "x-app-id": APP_ID,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(f"Nutritionix API call: \n {result} \n")

# Adding date and time
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Sheety API Call & Authentication
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=headers)
    print(sheet_response)
