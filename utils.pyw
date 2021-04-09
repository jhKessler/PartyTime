import csv
import requests
import pandas as pd
import json
import io

def load_data(url: str):
    """Loads data from url"""
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        data = pd.read_csv(io.StringIO(decoded_content), delimiter="\t")
    return data

def save_data(data: dict):
    """Save data to json file"""
    with open('frontend/src/assets/data.json', 'w') as f:
        json.dump(data, f)

def sort_fn(tpl: tuple):
    """sort fn for week-strings"""
    week, year = tpl[0].split("-")
    val = int(week) + int(year) ** 2
    return val