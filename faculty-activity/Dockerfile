FROM tiangolo/uwsgi-nginx-flask:flask

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get -y install \
    libpq-dev \
    libmysqlclient-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./app /app

RUN pip install -r /app/requirements.txt

COPY ./app /app
