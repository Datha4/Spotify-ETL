FROM python:3.10-slim

WORKDIR /tmp

COPY db_connection.py . 

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 pandas==2.0.0

EXPOSE 5432

CMD ["python3", "db_connection.py"]
