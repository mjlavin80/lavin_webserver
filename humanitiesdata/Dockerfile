FROM lavinflaskbase_2019

RUN apt-get -y install \
    libpq-dev \
    libmysqlclient-dev \
    libxml2-dev \
    libxslt-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./app /app

RUN pip install -r /app/requirements.txt
