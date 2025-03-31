import os
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

index = list(range(2377, 2381))  # Example range of event IDs
base_url = "https://www.vlr.gg/stats/?event_group_id=all&event_id=1&series_id=all&region=all&min_rounds=25&min_rating=1550&agent=all&map_id=all&timespan=all"


"""GET PLAYER STATS"""
service = Service(executable_path="D:/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(base_url)

os.makedirs("player", exist_ok=True)

wait = WebDriverWait(driver, 10)
dropdown_element = wait.until(EC.visibility_of_element_located((By.NAME, 'event_id')))

options = dropdown_element.find_elements(By.TAG_NAME, 'option')

filtered_options = [(option.text, option.get_attribute('value')) for option in options 
                     if 'Champions Tour' in option.text or 'Challengers League' or 'Valorant Champions' in option.text]
print("Filtered Options:", filtered_options)

driver.quit()
