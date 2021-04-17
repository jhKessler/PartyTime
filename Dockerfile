FROM nikolaik/python-nodejs:latest
WORKDIR /app


#install frontend
COPY frontend/package.json /app
RUN npm install
COPY ./frontend /app
RUN npm run build --prod
RUN npm i serve -g

#copy python script
COPY time_to_party.pyw /app
COPY utils.py /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

#install crontab
RUN apt-get update
RUN apt-get install cron -y
COPY crontab /etc/cron.d/update-data
RUN service cron start


ENTRYPOINT serve dist/frontend -p 5555
