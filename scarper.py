from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def scrape(url, max_page):
    # Set up the web driver
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Open the URL
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    all_products = []

    for i in range(1, max_page+1):
        print(f"Scraping page {i}...")

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find generic class for all products
        products = soup.find_all('div', class_='tUxRFH')

        for product in products:
            title = product.find('div', class_='KzDlHZ')
            price = product.find('div', class_='Nx9bqj _4b5DiR')

            title_text = title.text.strip() if title else "No title"
            price_text = price.text.strip() if price else "No price"

            all_products.append({"title": title_text, "price": price_text})
            print(f"Product: {title_text}, Price: {price_text}")

        # Try clicking the "Next" button
        try:
            next_button = driver.find_element(By.XPATH, "//a[@class='_9QVEpD' and span[text()='Next']]")
            if next_button:
                next_button.click()
                time.sleep(3)
                continue
            else:
                break  # No more pages
        except NoSuchElementException:
                print("No more pages")
                break  # No "Next" button found
    driver.quit()
    return all_products

# Run the scraper
base_url = "https://www.flipkart.com/search?q=iphone"
max_page = 3

products = scrape(base_url, max_page)
# print(products)
