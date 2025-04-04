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

base_url = "https://www.vlr.gg/stats/?event_group_id=all&event_id=1&series_id=all&region=all&min_rounds=25&min_rating=1550&agent=all&map_id=all&timespan=all"
matches_url = "https://www.vlr.gg/event/matches/{}"
players_stats_url = "https://www.vlr.gg/event/stats/{}"


"""
Find the event ID for the target events.
"""
service = Service(executable_path="D:/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(base_url)

os.makedirs("player", exist_ok=True)

wait = WebDriverWait(driver, 10)
dropdown_element = wait.until(EC.visibility_of_element_located((By.NAME, 'event_id')))

options = dropdown_element.find_elements(By.TAG_NAME, 'option')

filtered_options = {option.get_attribute('value'): option.text for option in options 
                    if 'Champions Tour' in option.text or 'Challengers League' in option.text or 'Valorant Champions' in option.text}

driver.quit()

# """
# Get the player stats for each event ID.
# """
# driver = webdriver.Chrome(service=service)
# for event in filtered_options.keys():   
#     url_match = matches_url.format(event)
#     url_stats = players_stats_url.format(event)

#     driver.get(url_match)
#     driver.execute_script("window.scrollTo(1, 10000)")
#     time.sleep(1)

#     html = driver.page_source

#     with open("team/{}.html".format(event), "w+", encoding="utf-8") as f:
#         f.write(html)

#     driver.get(url_stats)
#     driver.execute_script("window.scrollTo(1, 10000)")
#     time.sleep(1)

#     html = driver.page_source

#     with open("player/{}.html".format(event), "w+", encoding="utf-8") as f:
#         f.write(html)

"""
Parse player stats
"""
dfs = []
for event in filtered_options.keys():
    with open("player/{}.html".format(event), encoding="utf-8") as f:
        page = f.read()

    soup = bs(page, "html.parser")

    thead = soup.find('tr')
    if thead:
        thead.decompose()

    player_table = soup.find("table")
    player = pd.read_html(StringIO(str(player_table)))[0]
    player["Event"] = filtered_options[event]
    player["Event ID"] = event
    dfs.append(player)

players = pd.concat(dfs)
players.to_csv("players.csv")


