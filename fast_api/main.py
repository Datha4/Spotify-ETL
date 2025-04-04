from fastapi import FastAPI, HTTPException, Form, Header
from fastapi.responses import StreamingResponse
import psycopg2
import utils.queries as queries
from io import BytesIO
import os

api = FastAPI(
    title="API Queries Music collect",
    description="This API is designed to collect data, made and coded by David Thak",
    version="1.0.0",
    openapi_tags=[
        {"name": "main", "description": "This API is designed to collect data"},
        {"name": "secondary", "description": "functions in dev"},
    ],
)

conn_params = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "spotify_database"),
}

repo_path = "/tmp/db_data/"


@api.post("/query", name="Form to query on the music_database", tags=["main"])
def get_index(select_query: str):
    """Insert your SQL query here, for example 'SELECT * FROM all_toptracks_data;'"""
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        data = queries.queries(cursor=cursor, select_query=select_query)
        csv_bytes = data.to_csv(index=False).encode("utf-8")

        # Créer une réponse de streaming pour renvoyer le fichier CSV
        response = StreamingResponse(BytesIO(csv_bytes), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=result.csv"

        cursor.close()
        conn.close()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api.get("/get_table", name="get the list of all the table in the db", tags=["main"])
def get_other():
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        )
        table_list = [table[0] for table in cursor.fetchall()]
        cursor.close()
        conn.close()
        return {
            "alltable": table_list,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(api, host="localhost", port=8000)
