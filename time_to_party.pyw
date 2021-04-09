import csv
import requests
import pandas as pd
import numpy as np
import io
import datetime
import json
from calendar import monthrange
import isoweek

URL = 'https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv'

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

def get_month_list(reverse=False):
    all_months = [
    (1, 'Januar'),
    (2, 'Februar'),
    (3, 'März'),
    (4, 'April'),
    (5, 'Mai'),
    (6, 'Juni'),
    (7, 'Juli'),
    (8, 'August'),
    (9, 'September'),
    (10, 'Oktober'),
    (11, 'November'),
    (12, 'Dezember'),
    ]
    if not reverse:
        month = {str(month_num): month_name for month_num, month_name in all_months}
    else:
        month = {month_name: str(month_num) for month_num, month_name in all_months}
    return month

def format_month_strings(month_strings: list, all_months: list):
    """Formats month numbers to corresponding month names"""
    monate_data_format = []
    for m in monate_data:
        m_str = ""
        month_num = m.split("-")[0]
        m_str += all_months[month_num]
        m_str +=  " " + m.split("-")[1]
        monate_data_format.append(m_str)
    return monate_data_format

def sort_months_fn(tpl: tuple):
    """sort fn for months"""
    month, year = tpl[0].split("-")
    val = int(month) + int(year) ** 2
    return val

data = load_data(URL)
# group by weekday
data["weekday"] = pd.to_datetime(data["date"]).dt.weekday
nach_wochentag = data.groupby("weekday")["dosen_differenz_zum_vortag"].sum().astype(int)

# get unique id for week and year
data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d")
data["week_nr"] = data["date"].dt.isocalendar().week.astype(str)
data["year"] = data["date"].dt.year.astype(str)
data["unique_week_nr"] = data["date"].dt.strftime('%U-%Y')

# get vaccinations per week
nach_woche = dict(data.groupby("unique_week_nr")["dosen_kumulativ"].max())
nach_woche = sorted(nach_woche.items(), key=sort_months_fn)
# format list dtype
for i in range(len(nach_woche)):
    nach_woche[i] = list(nach_woche[i])
    nach_woche[i][1] = int(nach_woche[i][1])
wochen, nach_woche = zip(*nach_woche)

# get vaccinations of last 7 days
last_seven_days = data.iloc[-7:]
dosen_insgesamt = data.iloc[-1]["dosen_kumulativ"]
last_seven_days_total = last_seven_days["dosen_differenz_zum_vortag"].sum()
last_seven_days_avg = last_seven_days_total // 7

# misc stats
einw = 83000000
impfrate_herdenimmunität = 0.75
herdenimmunität_anz = einw * impfrate_herdenimmunität
impfdosen_insgm = herdenimmunität_anz * 2
verabreicht = data["dosen_kumulativ"].max()
impfdosen_übrig = impfdosen_insgm - verabreicht

# find best fit line to estimate vaccination progression
coeffs = np.polyfit(range(len(nach_woche)), nach_woche, deg=2)
polyn = np.poly1d(coeffs)
# forecast with best fit line (this is very speculative dont take it too seriously)
geimpft = 0
best_fit_func = []
best_fit_func_weeks = []
week, year = wochen[0].split("-")
week = int(week)
year = int(year)
week_cnt = isoweek.Week.last_week_of_year(year).week
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
# make prediction
alle_geimpft = datetime.datetime.strptime(best_fit_func_weeks[-1] + "-1", "%U-%Y-%w").strftime("%Y-%m-%d")
best_fit_func[0] = 0

# save data to json
data_dict = {
    "last_seven_days_total" : int(last_seven_days_total),
    "last_seven_days_avg" : int(last_seven_days_avg),
    "einwohner_deutschland": int(einw),
    "impfrate_herdenimmunitaet": impfrate_herdenimmunität,
    "menschen_fuer_herdenimmunitaet": int(herdenimmunität_anz),
    "dosen_fuer_herdenimmunitaet": int(impfdosen_insgm),
    "impfdosen_bisher": int(dosen_insgesamt),
    "impfdosen_uebrig": int(impfdosen_übrig),
    "wann_genug_leute_geimpft": alle_geimpft,
    "impfungen_nach_wochentag": list(nach_wochentag),
    "impfungen_nach_woche": nach_woche,
    "impf_forecast": best_fit_func,
    "impf_forecast_wochen": best_fit_func_weeks,
    "stand": datetime.datetime.today().strftime("%Y-%m-%d")
}

save_data(data_dict)

