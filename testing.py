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
from selenium.webdriver import ActionChains


options = Options()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
capabilities = driver.capabilities


driver.get(
    "https://bid.auctionhouseofbroadway.com/ui/auctions/106702")
driver.maximize_window()

time.sleep(5)

# scroll_ele = driver.find_element(
#     By.XPATH, '//*[@id="Root"]/div/div[1]').send_keys(Keys.PAGE_DOWN)

#  driver.execute_script(
#     "window.scrollTo(0,document.documentElement.scrollHeight)")

print(driver.title)
print(driver.current_url)

scrollable_div = driver.find_element(By.CSS_SELECTOR,
                                     '[data-testid="auction-list-scroll"]')  # Replace with the actual ID or locator
height = driver.execute_script("return document.body.scrollHeight")
print(height)

scroll_distance = 5000  # Adjust this value as needed
driver.execute_script(
    f"arguments[0].scrollBy(0, {scroll_distance});", scrollable_div)

# Check if the div is scrollable
is_scrollable = driver.execute_script(
    "return arguments[0].scrollHeight > arguments[0].clientHeight;", scrollable_div)

if is_scrollable:
    print("The div is scrollable.")
else:
    print("The div is not scrollable.")

time.sleep(10)
driver.quit()
