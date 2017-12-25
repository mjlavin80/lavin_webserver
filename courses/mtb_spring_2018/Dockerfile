FROM lavinflaskbase
RUN apt-get -y install \
    libxml2-dev libxslt-dev
COPY ./app /app
RUN pip install -r /app/requirements.txt
