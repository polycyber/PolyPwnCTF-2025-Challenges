
FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# CMD ["fastapi", "run", "app/main.py", "--port", "5000"]
EXPOSE 5000
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]
# fastapi run server/app/main.py --port 8080
