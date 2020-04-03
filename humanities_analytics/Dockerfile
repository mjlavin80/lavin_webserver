FROM lavinflaskbase_2019

RUN apt-get -y install \
    libpq-dev \
    libxml2-dev \
    libxslt-dev \
    && apt-get clean 

COPY ./app /app

