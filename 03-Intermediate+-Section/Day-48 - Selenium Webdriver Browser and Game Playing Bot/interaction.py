from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Keep Chrome browser open after the program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://en.wikipedia.org/wiki/Main_Page")

# Find element by XPATH
# article_count = driver.find_element(By.XPATH, value='//*[@id="articlecount"]/ul/li[2]/a[1]')
# print(article_count.text)

# Hone in on anchor tag using CSS_SELECTOR
article_count = driver.find_element(By.CSS_SELECTOR, value="#articlecount a")
# article_count.click()

# Find element by LINK TEXT
all_portals = driver.find_element(By.LINK_TEXT, value="Content portals")
# all_portals.click()

# Find the <search>
search = driver.find_element(By.XPATH, value='//*[@id="p-search"]/a/span[1]')
search.click()

search = driver.find_element(By.NAME, value="search")
search.send_keys("Python", Keys.ENTER)

# driver.close()
# driver.quit()
