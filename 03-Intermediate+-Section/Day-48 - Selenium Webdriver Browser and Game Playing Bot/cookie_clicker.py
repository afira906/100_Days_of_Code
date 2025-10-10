from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Get cookie element
cookie = driver.find_element(By.ID, "cookie")


def get_affordable_upgrades():
    """Check store for affordable upgrades and return them sorted by price"""
    # Get all available store items
    items = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#store div[id^='buy']:not(.grayed)"))
    )

    # Get current cookie count
    cookie_count = int(driver.find_element(By.ID, "money").text.replace(",", ""))

    upgrades = []
    for item in items:
        try:
            # Extract price from the item's text
            price_text = item.find_element(By.TAG_NAME, "b").text
            price = int(price_text.split("-")[1].strip().replace(",", ""))

            if cookie_count >= price:
                upgrades.append({
                    'id': item.get_attribute("id"),
                    'price': price,
                    'name': item.get_attribute("id").replace("buy", "")
                })
        except Exception as e:
            continue

    return sorted(upgrades, key=lambda x: x['price'])


def purchase_best_upgrade():
    """Purchase the most expensive affordable upgrade"""
    affordable = get_affordable_upgrades()
    if affordable:
        best_upgrade = max(affordable, key=lambda x: x['price'])
        print(f"Purchasing {best_upgrade['name']} for {best_upgrade['price']}")
        driver.find_element(By.ID, best_upgrade['id']).click()
        return True
    return False


# Main loop
last_check = time.time()
check_interval = 5  # Check every 5 seconds
duration = 60 * 5  # 5 minutes
end_time = time.time() + duration

while time.time() < end_time:
    cookie.click()

    # Check for upgrades every 5 seconds
    if time.time() - last_check > check_interval:
        purchase_best_upgrade()
        last_check = time.time()

# Final results
cps = driver.find_element(By.ID, "cps").text
print(f"\nFinal Cookies Per Second: {cps}")
print("5-minute automation complete!")
