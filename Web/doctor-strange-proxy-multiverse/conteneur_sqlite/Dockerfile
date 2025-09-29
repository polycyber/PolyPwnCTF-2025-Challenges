FROM postgres:latest

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD stephen89701
ENV POSTGRES_DB strangedb

EXPOSE 5432

# Create an initialization script
COPY init.sql /docker-entrypoint-initdb.d/