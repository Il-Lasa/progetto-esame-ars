import sqlite3
import pandas as pd

def get_dataframe(table_name):
    conn = sqlite3.connect('arpa.db')
    query = f'SELECT * FROM {table_name}'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

stations_df = get_dataframe('stations')
pollutants_df = get_dataframe('pollutants')
measurements_df = get_dataframe('measurements')

print("----------------- INFO STATIONS -----------------")
print(f'Numero di colonne: {len(stations_df.columns)}')
print(f'Numero di righe (stazioni): {len(stations_df)}')
print("---------------- INFO POLLUTANTS ----------------")
print(f'Numero di colonne: {len(pollutants_df.columns)}')
print(f'Numero di righe (pollutants): {len(pollutants_df)}')
print("--------------- INFO MEASUREMENTS ---------------")
print(f'Numero di colonne: {len(measurements_df.columns)}')
print(f'Numero di righe (misurazioni): {len(measurements_df)}')
data = measurements_df['data_rilevazione'].unique()
print(f'Date di misurazione: {data}')
print("-------------------------------------------------")