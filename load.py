import duckdb
import os
import subprocess

def file(target_path):
    for filename in os.listdir(target_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(target_path, filename)
    return file_path

def load_all_files_into_db(target_path, table_name):
    file_path = file(target_path)
    conn = duckdb.connect(database='/workspaces/xiaonanY317/dev.duckdb')
    table_exists_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    table_exists_result = conn.execute(table_exists_query)
    table_exists = len(table_exists_result.fetchall()) > 0
    if table_exists:
        # Drop the existing table
        conn.execute(f"DROP TABLE IF EXISTS {table_name};")
    create_table_query = f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{file_path}');"
    conn.execute(create_table_query)
    conn.commit()
    result = conn.execute(f"SELECT * FROM {table_name} LIMIT 1")
    data = result.fetchdf()
    print("First 1 rows of the table:")
    print(data)
    
    




    

    
    