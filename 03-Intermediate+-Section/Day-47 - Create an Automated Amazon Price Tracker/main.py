import os
import requests
import smtplib
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

practice_url = "https://appbrewery.github.io/instant_pot/"
live_url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"


# ====================== Add Headers to the Request ===========================

# Full headers would look something like this
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

# A minimal header would look like this:
# header = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9"
# }

# Adding headers to the request
response = requests.get(live_url, headers=header)

soup = BeautifulSoup(response.content, "html.parser")
# Check you are getting the actual Amazon page back and not something else
# print(soup.prettify())

# Find the HTML element that contains the price
price = soup.find(class_="a-offscreen").get_text()

# Remove the dollar sign using split
price_without_currency = price.split("$")[1]

# Convert to floating point number
price_as_float = float(price_without_currency)
# print(price_as_float)


# ====================== Send an Email ===========================

# Get the product title
title = soup.find(id="productTitle").get_text().strip()
# print(title)

# Set the price below which you would like to get a notification
BUY_PRICE = 100

if price_as_float < BUY_PRICE:
    message = f"{title} is on sale for {price}!"

    with smtplib.SMTP(os.environ["SMTP_ADDRESS"], port=587) as connection:
        connection.starttls()
        connection.login(os.environ["SENDER_EMAIL"], os.environ["SENDER_PASSWORD"])
        connection.sendmail(
            from_addr=os.environ["SENDER_EMAIL"],
            to_addrs=os.environ["RECEIVER_EMAIL"],
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{live_url}".encode("utf-8")
        )
