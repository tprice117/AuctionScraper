import time
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import pandas as pd
import csv
from selenium.webdriver.common.keys import Keys


options = Options()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
capabilities = driver.capabilities


print("Enter the url for the bid.auctionhouseofbroadway.com url: ")
userIn = input()


driver.get(userIn)
# driver.get("https://bid.auctionhouseofbroadway.com/ui/auctions/106702")
driver.maximize_window()
driver.set_window_size(1024, 768)

time.sleep(1)

print(driver.title)
csv_file_name = driver.title + ".csv"
print(driver.current_url)


iList = []
jList = []
nList = []


scrollable_div = driver.find_element(By.CSS_SELECTOR,
                                     '[data-testid="auction-list-scroll"]')  # Replace with the actual ID or locator
totalItems = driver.find_element(By.CLASS_NAME,
                                 'MuiSlider-valueLabelLabel')
totalItemsStr = totalItems.text

splitResult = totalItemsStr.split("/")
if len(splitResult) > 1:
    result_String = splitResult[1]
    print(result_String)
itemRange = int(result_String)


def scroll_down(scroll_distance):
    driver.execute_script(
        f"arguments[0].scrollBy(0, {scroll_distance});", scrollable_div)


soldItems = 0
unsoldItems = 0
max_scrolls = 30
scroll_count = 0
scraped_data = []
try:
    seen_elements = set()
    while True:
        scroll_down(450)
        time.sleep(2)
        parent_divs = driver.find_elements(By.CSS_SELECTOR, 'div.body')

        if len(parent_divs) == len(seen_elements):
            break

        # element scraping
        for n in parent_divs:
            title = n.find_element(By.CSS_SELECTOR,  'h1.ellipsis').text
            desc = n.find_element(By.CSS_SELECTOR, 'div.jss73').text
            bids = n.find_element(By.CSS_SELECTOR, '.jss147 span').text
            urls = n.find_element(By.CSS_SELECTOR, 'a.titleLink')
            if title not in seen_elements:
                # url scrape
                url = urls.get_attribute('href')
                print(f"{title}, {desc}, {bids}, {url}")
                # dict creation
                data = {
                    "title": title,
                    "description": desc,
                    "bids": bids,
                    "urls": url
                }
                # sold/unsold increment
                if bids.startswith("High"):
                    soldItems += 1
                else:
                    unsoldItems += 1

                # append dict to list
                scraped_data.append(data)
                seen_elements.add(title)


except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    driver.quit()


print(scraped_data)


csv_file_name = csv_file_name.replace(" ", "_")


keys = scraped_data[0].keys()
with open(csv_file_name, 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, keys)
    writer.writeheader()
    writer.writerows(scraped_data)

print("Scrape Complete: ")
print("Output File: " + csv_file_name)
print(f"{soldItems} sold items found")
print(f"{unsoldItems} unsold items found")
print(f"{itemRange} total items found")

driver.quit()
