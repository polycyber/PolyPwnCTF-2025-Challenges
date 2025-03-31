FROM python:3-alpine

RUN apk add --no-cache py3-pip

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

RUN mkdir /app

WORKDIR /app

COPY static ./static
COPY templates ./templates
COPY app.py .
COPY conf.py .
COPY schema.sql .
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 80

CMD [ "gunicorn", "-w", "4", "-c", "conf.py", "-b", "0.0.0.0:80", "app:app" ]