import csv
import requests
import pandas as pd
import io
import datetime
import json

CSV_URL = 'https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv'


with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    data = pd.read_csv(io.StringIO(decoded_content), delimiter="\t")

last_seven_days = data.iloc[-7:]
dosen_insgesamt = data.iloc[-1]["dosen_kumulativ"]
last_seven_days_total = last_seven_days["dosen_differenz_zum_vortag"].sum()
last_seven_days_avg = last_seven_days_total // 7

einw = 83_000_000
impfrate_herdenimmunität = 0.75
herdenimmunität_anz = einw * impfrate_herdenimmunität
impfdosen_insgm = herdenimmunität_anz * 2
verabreicht = 11_500_000 + 4_700_000
impfdosen_übrig = impfdosen_insgm - verabreicht

td = datetime.timedelta(days=impfdosen_übrig // int(last_seven_days_avg))
today = datetime.date.today()
alle_geimpft = (today + td).strftime("%Y-%m-%d")

data_dict = {
    "last_seven_days_total" : int(last_seven_days_total),
    "last_seven_days_avg" : int(last_seven_days_avg),
    "einwohner_deutschland": int(einw),
    "impfrate_herdenimmunitaet": impfrate_herdenimmunität,
    "menschen_fuer_herdenimmunitaet": int(herdenimmunität_anz),
    "dosen_fuer_herdenimmunitaet": int(impfdosen_insgm),
    "impfdosen_bisher": int(dosen_insgesamt),
    "impfdosen_uebrig": int(impfdosen_übrig),
    "genug_leute_geimpft": alle_geimpft
}

with open('frontend/src/assets/data.json', 'w') as f:
    json.dump(data_dict, f)

