import time
import requests
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv


load_dotenv()
MY_LAT = 30.375320
MY_LONG = 69.345116


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(os.getenv("MY_EMAIL"), os.getenv("MY_PASSWORD"))
        ## This code dosn't work because it has a emoji
        # connection.sendmail(
        #     from_addr=MY_EMAIL,
        #     to_addrs=MY_EMAIL,
        #     msg="Subject:Look up️☝️\n\nThe iss is above you in the sky."
        # )
        msg = EmailMessage()
        msg.set_content("The ISS is above you in the sky.")
        msg['Subject'] = "Look up ☝️"
        msg['From'] = os.getenv("MY_EMAIL")
        msg['To'] = os.getenv("MY_EMAIL")

        connection.send_message(msg)
