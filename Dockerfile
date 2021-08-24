FROM python:3.8
ENV PYTHONUNBUFFERED=1
RUN apt-get -y update && apt-get -y install build-essential redis-server net-tools telnet
WORKDIR /web_django
COPY requirements.txt /web_django
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /web_django
EXPOSE 8000
ENTRYPOINT ["/bin/sh","/web_django/dockerfile-entrypoint.sh"]