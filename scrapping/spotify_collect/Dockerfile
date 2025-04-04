
    FROM python:3.10-slim

    WORKDIR /tmp/spotify_scrapping

    COPY main.py .
    COPY requirements.txt .
    COPY module_collect ./module_collect


    VOLUME /tmp/output

    RUN pip install --no-cache-dir -r requirements.txt

    CMD ["python", "main.py"]    