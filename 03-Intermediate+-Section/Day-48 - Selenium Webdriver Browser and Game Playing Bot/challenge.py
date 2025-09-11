from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome browser open after the program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://secure-retreat-92358.herokuapp.com/")

fName = driver.find_element(By.NAME, value="fName")
fName.send_keys("Afira")

lName = driver.find_element(By.NAME, value="lName")
lName.send_keys("Arif")

email = driver.find_element(By.NAME, value="email")
email.send_keys("afira45@testinggmail.com")

sign_up = driver.find_element(By.CLASS_NAME, value="btn-primary")
sign_up.click()

# driver.close()
# driver.quit()
