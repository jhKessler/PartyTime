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
RUN chmod a+x time_to_party.py


COPY startup.sh /app

#install crontab
RUN apt-get update
RUN apt-get install cron rsyslog -y

RUN echo "0 14 * * * root cd /app && bash startup.sh" >> /etc/cron.d/update-data
RUN chmod 0644 /etc/cron.d/update-data

ENV database_host=partytime_postgres

ENTRYPOINT service cron start && service rsyslog start && bash /app/startup.sh && node server.ts
