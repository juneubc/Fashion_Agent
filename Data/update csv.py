import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Load your CSV
df = pd.read_csv('Data/store_zara_updated.csv')

# Set up Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Go to Zara women's section
category_url = "https://www.zara.com/ca/en/woman-new-in-l1180.html"
driver.get(category_url)
time.sleep(5)

# Scroll to load all products
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Find all product links
product_links = driver.find_elements(By.CSS_SELECTOR, 'a._item')
product_data = []
for link in product_links:
    url = link.get_attribute('href')
    name = link.text.strip()
    if url and name:
        product_data.append({'name': name.lower(), 'url': url})

driver.quit()

# Create a mapping from product name to URL
url_map = {item['name']: item['url'] for item in product_data}

# Update the CSV with valid URLs
def find_url(row):
    name = str(row['name']).lower()
    return url_map.get(name, row['url'])

df['url'] = df.apply(find_url, axis=1)

# Save the updated CSV
df.to_csv('Data/store_zara_updated_with_valid_urls.csv', index=False)
print("Updated CSV with valid URLs saved as Data/store_zara_updated_with_valid_urls.csv")