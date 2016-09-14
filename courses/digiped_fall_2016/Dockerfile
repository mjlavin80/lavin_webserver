FROM tiangolo/uwsgi-nginx-flask:flask

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get -y install \
    libpq-dev \
    libmysqlclient-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 8080

COPY ./app /app
COPY ./app2 /app2

RUN pip install -r /app/requirements.txt
