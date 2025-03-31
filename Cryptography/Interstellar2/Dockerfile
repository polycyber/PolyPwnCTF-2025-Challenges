FROM python:3.10-slim-bullseye
WORKDIR /app

RUN apt-get update && \
    apt-get install -y socat net-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY src/run.sh run.sh
COPY src/app.py app.py
RUN pip install --no-cache-dir pycryptodome

EXPOSE 1337
RUN chmod +x run.sh
ENTRYPOINT ["sh","/app/run.sh"]
