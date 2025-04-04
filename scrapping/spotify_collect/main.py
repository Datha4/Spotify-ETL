import requests
import pandas as pd
import module_collect.collect_utils as collect_utils
import os
import datetime
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    url = os.getenv("TOKEN_URL")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("APP_ID"),
        "client_secret": os.getenv("APP_SECRET"),
    }

    r = requests.post(url, headers=headers, data=data)
    r_json = r.json()
    token = r_json["access_token"]
    print(f"Token is correctly generated ! ")
    headers = {"Authorization": f"Bearer {token}"}

    artists_list = [
        "Pop Smoke",
        "Travis Scott",
        "Drake",
        "The Weeknd",
        "Gunna",
        "post malone",
        "kanye west",
        "Young thug",
        "Rae Sremmurd",
        "future",
        "doja cat",
        "Nicki Minaj",
        "Kendrick Lamar",
        "Shaboozey",
        "Lil Nas X",
    ]

    artist_stats_df, top_tracks_df = collect_utils.artist_stats(artists_list, headers)

    output_path = "/tmp/output"

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        print("Directory already created ! ")

    actual_date = datetime.datetime.now()
    date_format = actual_date.strftime("%d_%m_%Y_%H_%M")

    artist_stats_df["extraction_date"] = actual_date.strftime("%Y-%m-%d %H:%M:%S")
    top_tracks_df["extraction_date"] = actual_date.strftime("%Y-%m-%d %H:%M:%S")

    artist_stats_df.to_csv(
        f"{output_path}/artist_stats_df_{date_format}.csv", index=False
    )
    top_tracks_df.to_csv(f"{output_path}/top_tracks_df_{date_format}.csv", index=False)
