import pandas as pd
from bs4 import BeautifulSoup
import requests
from pony import orm
import json
import io
from database import save_history

def load_data():
    """Loads data from url"""
    URL = 'https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv'
    with requests.Session() as s:
        download = s.get(URL)
        decoded_content = download.content.decode('utf-8')
        data = pd.read_csv(io.StringIO(decoded_content), delimiter="\t")
    return data

def scrape_inhabitants():
    """scrapes inhabitants of germany"""
    wikipedia_page = "https://de.wikipedia.org/wiki/Deutschland"
    r = requests.get(wikipedia_page).text
    soup = BeautifulSoup(r, features="lxml")
    side_table = soup.find(class_="infoboxstaat")
    tr_tags = side_table.find_all("tr")[11]
    td_tags = tr_tags.find_all("td")[1]
    einw_zahl = int(str(td_tags.prettify()).splitlines()[1].replace(".", ""))
    return einw_zahl

def scrape_status_date():
    """Scrapes date the data was last updated"""
    URL = "https://impfdashboard.de/daten"
    r = requests.get(URL).text
    soup = BeautifulSoup(r, features="lxml")
    sveltes = soup.find(class_="date").text
    stand = sveltes.split("Stand: ")[1]
    return stand

def save_data(new_data: dict):
    """Save data to json file"""
    with open('frontend/src/assets/data.json', 'r+') as f:
        save_history(new_data["last_data_update"], new_data["impf_forecast_kalenderwochen"], new_data["impf_forecast"])
        json.dump(new_data, f, indent=4)

def sort_fn(tpl: tuple):
    """sort fn for week-strings"""
    week, year = tpl[0].split("-")
    val = int(week) + int(year) ** 2
    return val