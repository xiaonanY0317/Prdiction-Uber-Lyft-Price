import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def scatter_plot(table):
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=table, x='short_summary', y='unit_price', hue='cab_type')
    plt.title('Price/mile and tempreature by Cab Type')
    plt.xlabel('tempreature')
    plt.ylabel('Price ($)')
    plt.legend(title='Cab Type')  
    plt.show()

def weather_bar_plot(table):
    average_prices = table.groupby('short_summary')['unit_price'].mean()
    plt.figure(figsize=(12, 6))
    plt.bar(average_prices.index, average_prices, color="lightblue")
    plt.title("Average Price/Mile in Different Weather")
    plt.xlabel("Short_Summary")
    plt.ylabel("Average Price/Mile")
    plt.xticks(rotation=90)
    plt.show()

def hour_bar_plot(table):
    average_prices = table.groupby('hour')['unit_price'].mean()
    plt.figure(figsize=(12, 6))
    plt.bar(average_prices.index, average_prices, color="lightblue")
    plt.title("Uber: Average Price/Mile in Different Weather")
    plt.xlabel("Short_Summary")
    plt.ylabel("Average Price/Mile")
    plt.xticks(rotation=90)
    plt.show()

def weather_compare(table_1,table_2):
    weather = table_1['short_summary'].value_counts().keys()
    table_1_price=table_1.groupby('short_summary')['unit_price'].mean()
    table_2_price=table_2.groupby('short_summary')['unit_price'].mean()
    X_axis = np.arange(len(weather))
    plt.bar(X_axis - 0.2, table_1_price, 0.4, label = 'Uber',color="pink")
    plt.bar(X_axis + 0.2, table_2_price, 0.4, label = 'Lyft',color="lightblue")
  
    plt.xticks(X_axis,weather,rotation=90)
    plt.xlabel("Short_Summary")
    plt.ylabel("Mean Price")
    plt.title("Uber VS Lyft: Unit Price in Different Weather")
    plt.legend()
    plt.show()
    
def hour_compare(table_1,table_2):
    weather = table_1['hour'].value_counts().keys()
    table_1_price=table_1.groupby('hour')['unit_price'].mean()
    table_2_price=table_2.groupby('hour')['unit_price'].mean()
    X_axis = np.arange(len(weather))
    plt.bar(X_axis - 0.2, table_1_price, 0.4, label = 'Uber',color="pink")
    plt.bar(X_axis + 0.2, table_2_price, 0.4, label = 'Lyft',color="lightblue")
  
    plt.xticks(X_axis,weather,rotation=90)
    plt.xlabel("hour")
    plt.ylabel("Mean Price")
    plt.title("Uber VS Lyft: Unit Price in Different hour time")
    plt.legend()
    plt.show()
    


