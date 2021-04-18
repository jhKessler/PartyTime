FROM nikolaik/python-nodejs:latest
WORKDIR /app


#install frontend
COPY frontend/package.json /app
RUN npm install
COPY ./frontend /app
RUN npm run build --prod

#copy python script
COPY ./backend /app
RUN pip install -r requirements.txt

#install crontab
RUN apt-get update
RUN apt-get install cron rsyslog -y
RUN service rsyslog start
#* * * * * cd /app && python3 time_to_party.pyw
#0 13 * * * cd /app && python3 time_to_party.pyw
RUN echo "* * * * * root (cd /app && /usr/local/bin/python3 time_to_party.pyw) >> /var/log/cron.log" >> /etc/cron.d/update-data
RUN chmod 0644 /etc/cron.d/update-data
RUN crontab /etc/cron.d/update-data
RUN touch /var/log/cron.log
RUN service cron start

ENV database_host=partytime_postgres

ENTRYPOINT node server.ts
#ENTRYPOINT ["/bin/bash"]
