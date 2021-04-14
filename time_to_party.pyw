import requests
import pandas as pd
import numpy as np
import datetime
import isoweek
import csv
import json
import io
from bs4 import BeautifulSoup

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

def save_data(data: dict):
    """Save data to json file"""
    with open('frontend/src/assets/data.json', 'w') as f:
        json.dump(data, f, indent=4)

def sort_fn(tpl: tuple):
    """sort fn for week-strings"""
    week, year = tpl[0].split("-")
    val = int(week) + int(year) ** 2
    return val

def main():
    """write vaccination data to json file"""
    data = load_data()
    # convert date column to datetime objects
    data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d")

    # group by weekday
    data["weekday"] = data["date"].dt.weekday
    nach_wochentag = data.groupby("weekday")["dosen_differenz_zum_vortag"].sum().astype(int)

    # get unique id for week and year
    data["unique_week_nr"] = data["date"].dt.strftime('%U-%Y')

    # get vaccinations per week
    nach_woche = dict(data.groupby("unique_week_nr")["dosen_kumulativ"].max())
    nach_woche = sorted(nach_woche.items(), key=sort_fn)
    # format list dtype
    for i in range(len(nach_woche)):
        nach_woche[i] = list(nach_woche[i])
        nach_woche[i][1] = int(nach_woche[i][1])
    # drop last week if its not complete yet
    this_week = data[data["unique_week_nr"] == nach_woche[-1][0]]
    if len(this_week) < 7:
        del nach_woche[-1]
    # unpack tuple of shape [*, 2] to two 1d arrays
    wochen, nach_woche = zip(*nach_woche)
    # get vaccinations of last 7 days
    last_seven_days = data.iloc[-7:]
    last_seven_days_total = last_seven_days["dosen_differenz_zum_vortag"].sum()
    last_seven_days_avg = last_seven_days_total // 7

    # misc stats
    einw = scrape_inhabitants()
    impfrate_herdenimmunität = 0.75
    herdenimmunität_anz = einw * impfrate_herdenimmunität
    impfdosen_insgm = herdenimmunität_anz * 2
    verabreicht = data["dosen_kumulativ"].max()
    impfdosen_übrig = impfdosen_insgm - verabreicht

    # find best fit line to estimate vaccination progression
    coeffs = np.polyfit(range(len(nach_woche)), nach_woche, deg=2)
    polyn = np.poly1d(coeffs)
    # forecast with best fit line
    best_fit_func = []
    best_fit_func_weeks = []
    week = int(wochen[0].split("-")[0])
    year = int(wochen[0].split("-")[1])
    week_cnt = isoweek.Week.last_week_of_year(year).week
    # predict months until herd immunity count is met
    for i in range(100):
        line_val = int(polyn(i))
        best_fit_func.append(line_val)
        best_fit_func_weeks.append((str(week) + "-" + str(year)))
        week += 1
        if week > week_cnt:
            year += 1
            week = 0
            week_cnt = isoweek.Week.last_week_of_year(year).week
        if line_val > impfdosen_insgm:
            break
    # make prediction on when herd immunity is reached (2 weeks for effect to kick in)
    alle_geimpft = (datetime.datetime.strptime(best_fit_func_weeks[-1] + "-1", "%U-%Y-%w") + datetime.timedelta(days=14)).strftime("%Y-%m-%d")

    # save data to json
    data_dict = {
        "last_seven_days_total" : int(last_seven_days_total),
        "last_seven_days_avg" : int(last_seven_days_avg),
        "einwohner_deutschland": int(einw),
        "impfrate_herdenimmunitaet": impfrate_herdenimmunität,
        "menschen_fuer_herdenimmunitaet": int(herdenimmunität_anz),
        "dosen_fuer_herdenimmunitaet": int(impfdosen_insgm),
        "impfdosen_bisher": int(verabreicht),
        "impfdosen_uebrig": int(impfdosen_übrig),
        "wann_genug_leute_geimpft": alle_geimpft,
        "impfungen_nach_wochentag": list(nach_wochentag),
        "impfungen_nach_woche": nach_woche,
        "impfungen_nach_woche_kalenderwochen": best_fit_func_weeks[:len(nach_woche)],
        "impf_forecast": best_fit_func,
        "impf_forecast_kalenderwochen": best_fit_func_weeks,
        "stand": datetime.date.today().strftime("%Y-%m-%d"),
        "last_data_update": scrape_status_date(),
        "impf_fortschritt_prozent": int((verabreicht / impfdosen_insgm) * 100)
    }
    save_data(data_dict)


if __name__ == "__main__":
    main()