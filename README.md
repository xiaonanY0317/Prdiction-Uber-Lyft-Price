# Price prediction of Uber and Lyft

Our project is a data-driven initiative aimed at forecasting ride-sharing prices for Uber and Lyft services. As urban mobility continues to evolve, predicting ride prices becomes essential for both service providers and consumers. This project leverages machine learning algorithms to analyze historical ride data, weather conditions, time of day, and other relevant factors to generate accurate and insightful predictions.

## Table of Contents
### Data Source
Kaggle dataset: https://www.kaggle.com/datasets/brllrb/uber-and-lyft-dataset-boston-ma  
Dataset info:  
- Uber&Lyft order information.(Price, Time, Distance...)
- Weather condition.(Tempreature, Humidity, Visibility...)

### Project Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/wustl-data/Uber-Lyft.git
2. **Add package:**
   ```bash
   poetry install

### Usage
1. **Dataset Extract and Load:**
- **Extract data from kaggle**  
Extract data using kaggle API.
Need to apply kaggle API token.
   ```
   def extract_data(user_name,user_key,dataset_owner,dataset_name, target_path):
    os.environ['KAGGLE_USERNAME'] = user_name
    os.environ['KAGGLE_KEY'] = user_key
    dataset = f"{dataset_owner}/{dataset_name}"
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path=target_path,unzip=True)
   ```
- **Load data into duckdb**  
After extract, we get a CSV file. We need to load data into duckdb for futher using.
   ```
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
      dbt_command = "dbt run"
      subprocess.run(dbt_command, shell=True)
   ```

2. **Config dbt:**
- **download dbt pacakages**
- **Create and config profiles.yml file**
- **Create and config dbt_project.yml file**
- **Build sql model based on BDD feature stories.**
BDD Stories:
**feature 1**
Features: Finding influence factors of price change of ride apps  
- Scenario 1-1: How would the time period affect Lyft's price
   - Given: Rush time
   - When: daytime between hours between 7 am-8 am and daytime between hours between 4 pm-5 pm  
   - Then: the price will increase
- Scenario 1-2: How would the time period affect Uber's price
   - Given: Rush time
   - When: daytime between hours between 7 am-8 am and daytime between hours between 4 pm-5 pm   
   - Then: the price will increase
**feature 2**
Feature: Finding Influence Factors of Price Change of Ride Apps 
- Scenario 2-1: How would weather affect Uber's price
   - Given: Bad weather
   - When: Humidity above 70% (Rainy)
   - Then: Price will increase
- Scenario 2-2: How would weather affect Lyft's price 
   - Given: Bad weather
   - When: Temperature lower than 30。F
   - Then: Price will increase

- **Write sql script to get the columns we need for futher analysis**
All in models:
- weather_price_lyft
- weather_price_uber
- hour_price_lyft
- hour_price_uber

3. **Data Cleaning**
- Transform price from str to fload
- Split Datetime into hour, minute
- create unit_price for our futher use.

4. **Data visualization**
we create plot to check the relationship between price and hour and weather. And also compare the price between Uber and Lyft.
![Alt text](image/image-1.png)
![Alt text](image/image.png)
From the plot, we could know that acutually, there no big price difference between different weather and hour of Uber and Lyft. But most of the time, Uber is cheaper than Lyft.Thus in our model part, we would focus on predict price of uber and lyft.

5. **Modeling**
For model, we use linear regression to predict then price of Uber and Lyft in a certain weather and hour.
   ```
   def linear_regression(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    coefficients = model.coef_
    intercept = model.intercept_
    return mse, r2, coefficients, intercept
   ```
**Uber**
- Mean Squared Error: 72.91229425574122  
- R-squared: -3.869406136258746e-05
- coefficients: [0.00015431]
- intercept: 15.806537397305782
------------------------------
**Lyft**
- Mean Squared Error: 96.66602619494812
- R-squared: -7.567956791643127e-05
- coefficients: [0.00113354]
- intercept: 17.323630209825254

We found the R-squared is lower than 0 which indicate that Linear regression is not fit for our data. Thus we use pycaret in notebook to do the model selection. Then we use KNN and Random Forest model to fit our data. But we found that the R-squareds are all not so satisfy our expectation. We think it's beacuse the feature we choose is not enough or there might be a lot of outliers exist. We need to explore more.

6. **run main.py**
   change the variable based on your need
   make sure the enbironment have dbt.

7. **example notebook**
   check playground.ipynb
