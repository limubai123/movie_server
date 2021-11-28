FROM python:3.8-slim

#for non interactive apt-get
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    git \
    gcc \
    vim \
    python \
    python-dev \
    python-setuptools \
    libmaxminddb0 \
    libmaxminddb-dev \
    mmdb-bin \
    supervisor \
    sqlite3 \
    binutils \
    libproj-dev \
    libpq-dev \
    python3-dev \
    curl \
    libxslt-dev \
    build-essential \
    cron \
    libpcre3-dev \
    libssl-dev \
    zlib1g-dev \
    procps\
    && rm -rf /var/lib/apt/lists/*



RUN apt-get update && apt-get install -y redis-server gunicorn


COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install redis-server
RUN pip install -r requirements.txt

RUN mkdir -p /usr/src/logs

COPY supervisord.conf /etc/supervisor/conf.d/
COPY . /usr/src/app/.
RUN cd /usr/src/app/ && python manage.py makemigrations
RUN cd /usr/src/app/ && python manage.py migrate
RUN cd /usr/src/app/ && python manage.py collectstatic
RUN cd /usr/src/app/ && python manage.py seeds
RUN cd /usr/src/app/ && python manage.py test
RUN echo user=root >>  /etc/supervisor/supervisord.conf
CMD ["/usr/bin/supervisord","-n"]