FROM python

RUN mkdir /app
WORKDIR /app

RUN pip install "fastapi[standard]"
COPY . /app/

EXPOSE 8000

CMD ["fastapi", "run", "main.py"]