import os
from kaggle.api.kaggle_api_extended import KaggleApi

def extract_data(user_name,user_key,dataset_owner,dataset_name, target_path):
    os.environ['KAGGLE_USERNAME'] = user_name
    os.environ['KAGGLE_KEY'] = user_key
    dataset = f"{dataset_owner}/{dataset_name}"
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path=target_path,unzip=True)
