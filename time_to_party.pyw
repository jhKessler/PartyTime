import csv
import requests
import pandas as pd
import numpy as np
import io
import datetime
import json
from calendar import monthrange

CSV_URL = 'https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv'

# load data
with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    data = pd.read_csv(io.StringIO(decoded_content), delimiter="\t")

# group by weekday
data["weekday"] = pd.to_datetime(data["date"]).dt.weekday
nach_wochentag = data.groupby("weekday")["dosen_differenz_zum_vortag"].sum().astype(int)

# group by month
# get unique id for month
data["month_nr"] = pd.to_datetime(data["date"]).dt.month.astype(str)
data["year"] = data["date"].str.split("-").map(lambda x: x[0])
data["unique_month_nr"] = data[["month_nr", "year"]].agg("-".join, axis=1)

# get vaccinations per month
nach_monat = dict(data.groupby("unique_month_nr")["dosen_differenz_zum_vortag"].sum())
nach_monat = sorted(nach_monat.items(), key=lambda x: int(x[0].split("-")[0]) + int(x[0].split("-")[1]) ** 2)
for i in range(len(nach_monat)):
    nach_monat[i] = list(nach_monat[i])
    nach_monat[i][1] = int(nach_monat[i][1])

# last month may not be over yet, estimate month by simple rule of three
last_month, last_year = nach_monat[-1][0].split("-")
num_days = monthrange(int(last_year), int(last_month))[1]
num_days_in = len(data.loc[data["unique_month_nr"] == nach_monat[-1][0]])
month_estimation = int((nach_monat[-1][1] / num_days_in) * num_days)
nach_monat[-1][1] = month_estimation
monate_data, nach_monat = zip(*nach_monat)
# format month string
monate_data_format = []
all_months = reversed([
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
])
all_months = {str(month_num): month_name for month_num, month_name in all_months}
for m in monate_data:
    m_str = ""
    month_num = m.split("-")[0]
    m_str += all_months[month_num]
    m_str +=  " " + m.split("-")[1]
    monate_data_format.append(m_str)

# get vaccinations of last 7 days
last_seven_days = data.iloc[-7:]
dosen_insgesamt = data.iloc[-1]["dosen_kumulativ"]
last_seven_days_total = last_seven_days["dosen_differenz_zum_vortag"].sum()
last_seven_days_avg = last_seven_days_total // 7

# calculate how long it takes to vaccinate to herd immunity if vaccination rate stays like last 7 days
einw = 83_000_000
impfrate_herdenimmunität = 0.75
herdenimmunität_anz = einw * impfrate_herdenimmunität
impfdosen_insgm = herdenimmunität_anz * 2
verabreicht = 11_500_000 + 4_700_000
impfdosen_übrig = impfdosen_insgm - verabreicht
td = datetime.timedelta(days=impfdosen_übrig // int(last_seven_days_avg))
today = datetime.date.today()
alle_geimpft = (today + td).strftime("%Y-%m-%d")

# find best fit line to estimate vaccination progression
coeffs = np.polyfit(range(len(nach_monat)), nach_monat, deg=2)
polyn = np.poly1d(coeffs)
# forecast with best fit line (this is very speculative dont take it too seriously)
geimpft = 0
best_fit_func = []
for i in range(100):
    best_fit_func.append(np.round(polyn(i)))
    geimpft += polyn(i)
    if geimpft > impfdosen_insgm:
        break
best_fit_func[0] = 0

max_year = data["year"].astype(int).max()
monate_data_forecast = ["Dezember 2020"]
month_cnt = 0
year = 2021
for i in range(1, len(best_fit_func)):
    month_num = i % 12
    if i % 12 == 0:
        month_num = 12
        year += 1
    monate_data_forecast.append(all_months[str(month_num)] + " " + str(year))
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
    "impfungen_nach_monat": nach_monat,
    "impfungen_nach_monat_monate": monate_data_format,
    "impf_forecast": best_fit_func,
    "impf_forecast_monate": monate_data_forecast,
    "stand": today.strftime("%Y-%m-%d")
}
with open('frontend/src/assets/data.json', 'w') as f:
    json.dump(data_dict, f)

