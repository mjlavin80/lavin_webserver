FROM lavinflaskbase_2019

RUN apt-get -y install \
    libxml2-dev libxslt-dev

COPY ./app /app

RUN pip install -r requirements.txt
