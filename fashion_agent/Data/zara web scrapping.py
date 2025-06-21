import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Example Zara Canada category URL (change as needed)
category_url = "https://www.zara.com/ca/en/woman-new-in-l1180.html"

driver.get(category_url)
time.sleep(5)  # Wait for JS to load

products = driver.find_elements(By.CSS_SELECTOR, 'a.product-link._item')

data = []
for product in products:
    try:
        url = product.get_attribute('href')
        name = product.find_element(By.CSS_SELECTOR, 'span.product-name').text
        # Go to product page for more details
        driver.execute_script("window.open(arguments[0]);", url)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)
        # Extract details
        try:
            description = driver.find_element(By.CSS_SELECTOR, 'p.product-description').text
        except:
            description = ""
        try:
            price = driver.find_element(By.CSS_SELECTOR, 'span.price-current__amount').text
        except:
            price = ""
        try:
            sku = driver.find_element(By.CSS_SELECTOR, 'span.reference-information__reference').text
        except:
            sku = ""
        try:
            images = [img.get_attribute('src') for img in driver.find_elements(By.CSS_SELECTOR, 'img.media-image__image')]
        except:
            images = []
        # You can add more fields as needed
        data.append({
            "brand": "Zara",
            "url": url,
            "sku": sku,
            "name": name,
            "description": description,
            "price": price,
            "currency": "CAD",
            "images": images,
            "scraped_at": datetime.now().isoformat(),
            "terms": "",  # You can extract category/terms if available
            "section": "woman-new-in"
        })
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except Exception as e:
        print(f"Error: {e}")
        continue

driver.quit()

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("zara_ca_catalog.csv", index=False)
print("Scraping complete. Data saved to zara_ca_catalog.csv")