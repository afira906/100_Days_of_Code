from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome browser open after the program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.python.org")

# -------------This code will not work if you want to use Amazon
# -------------because Amazon doesn't allow bots to use their website-------------------
# --------------------Getting hold of different elements-------------------

# By .CLASS_NAME
# price_dollar = driver.find_element(By.CLASS_NAME, value="a-price-whole")
# price_cents = driver.find_element(By.CLASS_NAME, "a-price-fraction")
# print(f"The price is {price_dollar.text}.{price_cents.text}")

# By .NAME
# search_bar = driver.find_element(By.NAME, value="q")
# print(search_bar.tag_name)
# print(search_bar.get_attribute("placeholder"))

# By .ID
# button = driver.find_element(By.ID, value="submit")
# print(button.size)

# By .CSS_SELECTOR
# documentation_link = driver.find_element(By.CSS_SELECTOR, value=".documentation-widget a")
# print(documentation_link.text)

# By .XPATH
# bug_link = driver.find_element(By.XPATH, value='//*[@id="site-map"]/div[2]/div/ul/li[3]/a')
# print(bug_link.text)

# Gives you all the data
# driver.find_elements(By.CSS_SELECTOR)

# Challenge: Print the event dates from python.org
event_times = driver.find_elements(By.CSS_SELECTOR, value=".event-widget time")
event_names = driver.find_elements(By.CSS_SELECTOR, value=".event-widget li a")
events = {}

for n in range(len(event_times)):
    events[n] = {
        "time": event_times[n].text,
        "name": event_names[n].text,
    }
# print(events)
pprint(events)

# driver.close()
driver.quit()
