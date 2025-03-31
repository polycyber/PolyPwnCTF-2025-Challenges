FROM python:3.10-slim-bullseye

WORKDIR /app

RUN apt-get update && \
    apt-get install -y socat && \
    apt-get clean && \
    pip install inputimeout && \
    rm -rf /var/lib/apt/lists/*

COPY resources/menu.txt .
COPY resources/plats_flag.txt .
COPY src/app.py .
COPY src/run.sh .

RUN chmod +x run.sh

EXPOSE 1437

ENTRYPOINT ["sh","/app/run.sh"]