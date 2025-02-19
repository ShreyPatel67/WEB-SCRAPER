from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

# Set up the Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.flipkart.com/search?q=Iphone14")
time.sleep(5)  # Allow time for JavaScript to load

soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find product details
products = soup.find_all('div', class_='_75nlfW')

for product in products:
    product_name = product.find('div', class_='KzDlHZ').text
    product_price = product.find('div', class_='Nx9bqj _4b5DiR').text
    print(f"Product: {product_name} - Price: {product_price}")

driver.quit()