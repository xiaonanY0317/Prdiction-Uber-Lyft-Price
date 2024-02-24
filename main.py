from extract import extract_data
from load import load_all_files_into_db
from load import file
from clean_data import preprocess_data
from clean_data import get_data_from_duckdb
from clean_data import data_cleaning_weather
from clean_data import run_dbt
from visualization import weather_compare
from visualization import hour_compare
from model import linear_regression

target_path = "/workspaces/xiaonanY317/data"
user_name = 'xiaonany'
user_key = "bd1bf3764b29ed52246c08294264bb13"
dataset_owner = "brllrb"
dataset_name = "uber-and-lyft-dataset-boston-ma"
target_path = "/workspaces/xiaonanY317/data"
table_name = "rideshare"
#load and extract data
def load_extract():
    extract_data(user_name,user_key,dataset_owner,dataset_name,target_path)
    load_all_files_into_db(target_path, table_name)

#dbt_run
def dbt_run():
    run_dbt()
    
#data visualization
def data_visualization():
    sheet_name_1 = 'weather_price_uber'
    sheet_name_2 = 'weather_price_lyft'
    sheet_name_3 = 'hour_price_uber'
    sheet_name_4 = 'hour_price_lyft'
    table_1 = get_data_from_duckdb(sheet_name_1)
    table_2 = get_data_from_duckdb(sheet_name_2)
    table_3 = get_data_from_duckdb(sheet_name_3)
    table_4 = get_data_from_duckdb(sheet_name_4)
    table_1=data_cleaning_weather(table_1)
    table_2=data_cleaning_weather(table_2)
    table_3=data_cleaning_weather(table_3)
    table_4=data_cleaning_weather(table_4)
    weather_compare(table_1,table_2)# price compare between uber and lyft
    hour_compare(table_3,table_4)    
    
#model
def build_model():
    file_path = file(target_path)
    data_preprocess = preprocess_data(file_path,' Overcast ')# take Overcast as an example
    features = 'hour'
    target = 'price'
    uber_data = data_preprocess[data_preprocess['cab_type'] == 'Uber']
    lyft_data = data_preprocess[data_preprocess['cab_type'] == 'Lyft']

# Prepare data for Uber
    X_uber = uber_data[features].values.reshape(-1,1)
    y_uber = uber_data[target]

# Prepare data for Lyft
    X_lyft = lyft_data[features].values.reshape(-1,1)
    y_lyft = lyft_data[target]

    mse_uber, r2_uber , coefficients_uber, intercept_uber= linear_regression(X_uber, y_uber)
    mse_lyft, r2_lyft , coefficients_lyft, intercept_lyft= linear_regression(X_lyft, y_lyft)

    print(f"Mean Squared Error: {mse_uber}")
    print(f"R-squared: {r2_uber}")
    print(f"coefficients: {coefficients_uber}")
    print(f"intercept: {intercept_uber}")
    print("------------------------------")
    print(f"Mean Squared Error: {mse_lyft}")
    print(f"R-squared: {r2_lyft}")
    print(f"coefficients: {coefficients_lyft}")
    print(f"intercept: {intercept_lyft}")
    
    
    

if __name__ == "__main__":
    load_extract()
    dbt_run()
    data_visualization()
    build_model()
