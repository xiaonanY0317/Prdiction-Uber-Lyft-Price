import duckdb
import pandas as pd
import numpy as np
import subprocess

def get_data_from_duckdb(sheet_name) -> pd.DataFrame:
    conn = duckdb.connect(database="dev.duckdb")
    query_1 = f"DELETE FROM rideshare WHERE COALESCE(id,cab_type,temperature,short_summary,distance,windSpeed,visibility,humidity,price,) IS NULL"
    query_2 = f"SELECT * FROM {sheet_name}"
    result = conn.execute(query_1)
    result = conn.execute(query_2).fetchdf()
    return result

def run_dbt():
    dbt_command = "dbt run"
    subprocess.run(dbt_command, shell=True)

def data_cleaning_weather(table):
    table = table.dropna()
    table['price'] = table['price'].replace('NA', np.nan)
    table['price'] = table['price'].fillna(0)
    table['distance'] = pd.to_numeric(table['distance'], errors='coerce')
    table['distance'] = table['distance'].fillna(0)
    mask = table['distance'] != 0
    table.loc[mask, 'unit_price'] = table.loc[mask, 'price'].astype(float) / table.loc[mask, 'distance']
    table['unit_price'] = pd.to_numeric(table['unit_price'], errors='coerce')
    table=pd.DataFrame(table)
    return table

def data_cleaning_hour(table):
    table = table.dropna()
    table['price'] = table['price'].replace('NA', np.nan)
    table['price'] = table['price'].fillna(0)
    table['distance'] = pd.to_numeric(table['distance'], errors='coerce')
    table['distance'] = table['distance'].fillna(0)
    mask = table['distance'] != 0
    table.loc[mask, 'unit_price'] = table.loc[mask, 'price'].astype(float) / table.loc[mask, 'distance']
    table['unit_price'] = pd.to_numeric(table['unit_price'], errors='coerce')
    table['datetime'] = pd.to_datetime(table['datetime'])
    table['hour'] = table['datetime'].dt.hour
    table['minute'] = table['datetime'].dt.minute
    table=pd.DataFrame(table)
    return table

def preprocess_data(file_path,weather_condition):
    data= pd.read_csv(file_path)
    data = data.dropna()
    data['datetime'] = pd.to_datetime(data['datetime'])
    data['hour'] = data['datetime'].dt.hour
    data['minute'] = data['datetime'].dt.minute
    data = data[data['short_summary'] == weather_condition] 
    return data
