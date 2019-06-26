FROM python:3.7.3-slim-stretch

RUN apt-get update && apt-get install -y libgeos-dev
ADD . /app/
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pybabel compile -d ./locale -l fa -D fa_IR
CMD FLASK_APP=main.py flask run --host 0.0.0.0
