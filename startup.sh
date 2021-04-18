#!/bin/bash
cd /app
export PYTHONPATH=/usr/local/bin/python3
export database_host=partytime_postgres
echo $(set) >/app/debug
echo $(/usr/local/bin/python3 time_to_party.py) >>/app/debug
