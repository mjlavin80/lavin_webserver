FROM tiangolo/uwsgi-nginx-flask:python3.11

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get -y install \
    libpq-dev \
    default-libmysqlclient-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./app /app

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
