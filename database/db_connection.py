import os
import psycopg2
from psycopg2 import sql
import pandas as pd
import csv
from dotenv import load_dotenv

load_dotenv()
conn_params = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()
output_folder = "/tmp/output"

csv_files = [file for file in os.listdir(output_folder) if file.endswith(".csv")]

for csv_file in csv_files:
    table_name = os.path.splitext(csv_file)[0].replace("-", "_")
    csv_file_path = os.path.join(output_folder, csv_file)

    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)

        drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
        cursor.execute(drop_table_query)
        conn.commit()

        create_table_query = f"""
            CREATE TABLE {table_name} (
                {", ".join(f"{header} VARCHAR" for header in headers)}
            )
        """

        cursor.execute(create_table_query)
        conn.commit()

        for row in csv_reader:
            insert_query = f"""
                INSERT INTO {table_name} ({", ".join(headers)})
                VALUES ({", ".join("%s" for _ in headers)})
            """
            cursor.execute(insert_query, row)
        conn.commit()

cursor.close()
conn.close()
print("Table generated !")
