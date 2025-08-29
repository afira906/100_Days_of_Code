# "Note: Automated following is intentionally omitted to comply with Instagram's
# Terms of Service and prevent account restrictions."

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SIMILAR_ACCOUNT = os.getenv("SIMILAR_ACCOUNT")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


class InstaFollower:

    def __init__(self):
        # Optional - Keep browser open (helps diagnose issues during a crash)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        url = "https://www.instagram.com/accounts/login/"
        self.driver.get(url)

        time.sleep(10)
        username = self.driver.find_element(by=By.NAME, value="username")
        username.send_keys(USERNAME)

        time.sleep(10)
        password = self.driver.find_element(by=By.NAME, value="password")
        password.send_keys(PASSWORD)
        password.send_keys(Keys.ENTER)

        time.sleep(10)
        save_login_prompt = self.driver.find_element(By.XPATH, "//div[@role='button' and contains(., 'Not now')]")
        if save_login_prompt:
            save_login_prompt.click()

    def find_followers(self):
        time.sleep(5)
        # Show followers of the selected account.
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}")

        time.sleep(10)
        followers_link = self.driver.find_element(By.XPATH, '//a[contains(@href, "/followers")]/span[contains(., "followers")]')
        followers_link.click()

        time.sleep(10)
        modal_xpath = "/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"
        modal = self.driver.find_element(By.XPATH, value=modal_xpath)
        for i in range(10):
            # In this case we're executing some Javascript, that's what the execute_script() method does.
            # The method can accept the script as well as an HTML element.
            # The modal in this case, becomes the arguments[0] in the script.
            # Then we're using Javascript to say: "scroll the top of the modal (popup) element by the height of the modal (popup)"
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)

    def follow(self):
        all_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button._acan._acap._acas')

        for button in all_buttons:
            try:
                button.click()
                time.sleep(1.5)  # Add delay between clicks
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Cancel')]")
                cancel_button.click()


bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()
