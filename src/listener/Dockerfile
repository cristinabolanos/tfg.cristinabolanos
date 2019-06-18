FROM python:3.7.3-stretch
LABEL location="local"
LABEL version="0.0.0"

COPY listener.py /var/listener/run.py
RUN pip3 install peewee pymysql pycrypto

CMD [ "python3", "/var/listener/run.py"]
