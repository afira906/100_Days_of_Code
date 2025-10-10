from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env

ACCOUNT_EMAIL = os.getenv("ACCOUNT_EMAIL")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")
PHONE = os.getenv("PHONE")



# def abort_application():
#     # Click Close Button
#     close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
#     close_button.click()
#
#     time.sleep(2)
#     # Click Discard Button
#     discard_button = driver.find_elements(by=By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")[1]
#     discard_button.click()

# Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get(url="https://www.linkedin.com/jobs/search/?currentJobId=4222233205&distance=25&f_AL=true&geoId=102306254&keywords=python%20developer&origin=JOBS_HOME_KEYWORD_HISTORY&refresh=true")

## Click Reject Cookies Button
# time.sleep(2)
# reject_button = driver.find_element(By.CSS_SELECTOR, value='button[action-type="DENY"]')
# reject_button.click()

# Click the sign-in button
time.sleep(2)
sign_in_button = driver.find_element(by=By.XPATH, value='//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[2]/button')
sign_in_button.click()

# Sign in
time.sleep(5)
email_field = driver.find_element(By.XPATH, value='//*[@id="base-sign-in-modal_session_key"]')
email_field.send_keys(ACCOUNT_EMAIL)
password_field = driver.find_element(By.XPATH, value='//*[@id="base-sign-in-modal_session_password"]')
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)

# Save the job
# time.sleep(5)
# save_button = driver.find_element(By.CLASS_NAME, value="jobs-save-button__text")
# save_button.click()

# # Get Listings
# time.sleep(5)
# all_listings = driver.find_elements(by=By.CSS_SELECTOR, value=".job-card-container--clickable")
#
# # Apply for Jobs
# for listing in all_listings:
#     print("Opening Listing")
#     listing.click()
#     time.sleep(2)
#     try:
#         # Click Apply Button
#         apply_button = driver.find_element(by=By.CSS_SELECTOR, value=".jobs-s-apply button")
#         apply_button.click()
#
#         # Insert Phone Number
#         # Find an <input> element where the id contains phoneNumber
#         time.sleep(5)
#         phone = driver.find_element(by=By.CSS_SELECTOR, value="input[id*=phoneNumber]")
#         if phone.text == "":
#             phone.send_keys(PHONE)
#
#         # Check the Submit Button
#         submit_button = driver.find_element(by=By.CSS_SELECTOR, value="footer button")
#         if submit_button.get_attribute("data-control-name") == "continue_unify":
#             abort_application()
#             print("Complex application, skipped.")
#             continue
#         else:
#             # Click Submit Button
#             print("Submitting job application")
#             submit_button.click()
#
#         time.sleep(2)
#         # Click Close Button
#         close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
#         close_button.click()
#
#     except NoSuchElementException:
#         abort_application()
#         print("No application button, skipped.")
#         continue
#
# time.sleep(5)
# driver.quit()
