# Sending Email with Python
import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("MY_PASSWORD")

with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs=my_email,
        msg="Subject:Hello\n\nThis is the body of my email."
    )


# Working with date and time in Python
import datetime as dt

now = dt.datetime.now()
year = now.year
month = now.month
day_of_week = now.weekday()
print(day_of_week)

date_of_birth = dt.datetime(year=1995, month=12, day=15, hour=4)
print(date_of_birth)
