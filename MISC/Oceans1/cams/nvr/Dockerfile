FROM python:3-alpine

RUN apk add --no-cache py3-pip

RUN mkdir /app

WORKDIR /app

COPY static .
COPY templates .
COPY app.py .
COPY schema.sql .
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 80

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app" ]