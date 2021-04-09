import csv
import requests
import pandas as pd
import json
import io
from bs4 import BeautifulSoup

def load_data(url: str):
    """Loads data from url"""
    with requests.Session() as s:
        download = s.get(url)
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

def save_data(data: dict):
    """Save data to json file"""
    with open('frontend/src/assets/data.json', 'w') as f:
        json.dump(data, f)

def sort_fn(tpl: tuple):
    """sort fn for week-strings"""
    week, year = tpl[0].split("-")
    val = int(week) + int(year) ** 2
    return val