FROM python

RUN mkdir /app
WORKDIR /app

RUN pip install "fastapi[standard]" python-jose
RUN pip uninstall -y httptools
COPY . /app/

EXPOSE 8000

CMD ["fastapi", "run", "main.py"]