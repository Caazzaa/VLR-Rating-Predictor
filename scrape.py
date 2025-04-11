import os
import requests
import regex as re
from datetime import datetime
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

"""
Get the player stats for each event ID.
"""
driver = webdriver.Chrome(service=service)
for event in filtered_options.keys():   
    url_match = matches_url.format(event)
    url_stats = players_stats_url.format(event)

    driver.get(url_match)
    driver.execute_script("window.scrollTo(1, 10000)")
    time.sleep(1)

    html = driver.page_source

    with open("team/{}.html".format(event), "w+", encoding="utf-8") as f:
        f.write(html)

    driver.get(url_stats)
    driver.execute_script("window.scrollTo(1, 10000)")
    time.sleep(1)

    html = driver.page_source

    with open("player/{}.html".format(event), "w+", encoding="utf-8") as f:
        f.write(html)

"""
Parse player stats
"""
dfs = []
for event in filtered_options.keys():
    if not os.path.exists("player/{}.html".format(event)):
        continue
    with open("player/{}.html".format(event), encoding="utf-8") as f:
        page = f.read()

    soup = bs(page, "html.parser")

    thead = soup.find('tr')
    if thead:
        thead.decompose()

    player_table = soup.find("table")
    player = pd.read_html(StringIO(str(player_table)))[0]
    
    date = soup.find("div", class_="event-desc-item-value")
    date = date.get_text(strip=True).split("–")[0].strip().split("-")[0].strip()
    date = date.replace(",", "")
    print(date)
    if len(date.split()) == 2:  # If year is missing, append the last year from the previous iteration
        if re.match(r'.*([1-3][0-9]{3})', filtered_options[event]):
            last_year = re.search(r'([1-3][0-9]{3})', filtered_options[event]).group(1)  # Extract the year from the date string
        elif dfs:  # Check if there is a previous iteration
            last_year = dfs[-1]["Date"].dt.year.max()  # Get the latest year from the previous DataFrame
        else:
            last_year = datetime.now().year
        date = f"{date} {last_year}"
    try:
        date = datetime.strptime(date, "%b %d %Y")
    except ValueError:
        raise ValueError(f"Date format is invalid or unrecognized: {date}")
    print(date)

    player["Date"] = date
    player["Event"] = filtered_options[event]
    player["Event ID"] = event
    dfs.append(player)

players = pd.concat(dfs)
players.columns = ['Player/Team', 'Agents', 'Rounds Played', 'Rating', 'ACS', 'KD', 'KAST', 'ADR', 'KPR', 'APR', 'FKPR', 'FDPR', 'HS%', 'Clutch%', 'Clutches (won/played)', 'Max Kills', 'Kills', 'Deaths', 'Assists', 'First Kills', 'First Deaths', 'Date', 'Event', 'Event ID']
players.to_csv("player_stats.csv", index=False)


