FROM nginx:latest

RUN apt update && apt install -y python3 python3-pip python3-venv && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt

RUN python3 -m venv /app/venv && /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

RUN /app/venv/bin/playwright install --with-deps firefox

COPY nginx.conf /etc/nginx/nginx.conf

COPY app /app

EXPOSE 80

CMD /app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 & nginx -g "daemon off;"