import pandas as pd
import os


def queries(cursor, select_query, repo_path="/tmp/db_data/"):
    cursor.execute(select_query)

    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    top_tracks_concat = pd.DataFrame(data, columns=column_names)
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
    else:
        pass

    top_tracks_concat.to_csv("/tmp/db_data/output.csv", index=False)

    return top_tracks_concat
