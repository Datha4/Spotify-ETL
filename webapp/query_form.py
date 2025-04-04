import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import date


def fetch_data(query):
    api_url = "http://172.23.142.117:30080/query"
    params = {"select_query": query}
    headers = {"accept": "application/json"}

    response = requests.post(api_url, params=params, headers=headers)

    if response.status_code == 200:
        output_dir = "output_csv"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        csv_path = os.path.join(output_dir, "result.csv")
        with open(csv_path, "wb") as f:
            f.write(response.content)
        st.success("CSV file saved !")
        return pd.read_csv(csv_path)
    else:
        st.error(f"Call Api Error : {response.status_code}, {response.text}")
        return None


def fetch_tables():
    api_url = "http://172.23.142.117:30080/get_table"
    headers = {"accept": "application/json"}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(
            f"Erreur lors de l'appel de l'API : {response.status_code}, {response.text}"
        )
        return None


def main():
    st.title("App to query on the SQL database")
    if st.button("Get all tables available"):
        tables = fetch_tables()
        if tables:
            st.success("Available tables : ")
            st.write(tables)

    query = st.text_area("Write your SQL query here :")

    if st.button("Execute the query"):
        if query:
            df = fetch_data(query)
            if df is not None:
                st.dataframe(df)


if __name__ == "__main__":
    main()
