import pandas as pd
import requests
from io import StringIO

# URLs of the files on GitHub
orders_url = 'https://raw.githubusercontent.com/JannesPeeters/DEAD/main/data/orders.csv'
products_url = 'https://raw.githubusercontent.com/JannesPeeters/DEAD/main/data/products.csv'

# Download orders.csv
orders_response = requests.get(orders_url)
orders_csv = orders_response.text
orders_df = pd.read_csv(StringIO(orders_csv))

# Download products.csv
products_response = requests.get(products_url)
products_csv = products_response.text
products_df = pd.read_csv(StringIO(products_csv))

# Create a new DataFrame for final output
final_df = products_df[['Product Name', 'product_code', 'Type']].copy()

# Rename columns
final_df.rename(columns={'Product Name': 'product_name', 'Type': 'type'}, inplace=True)

# Initialize columns for each year
for year in range(2019, 2024):
    final_df[f'revenue_{year}'] = 0
    final_df[f'quantity_{year}'] = 0

# Process orders and update final_df
for index, row in orders_df.iterrows():
    products_id = map(int, row["productsIDs"].split(', '))
    quantities = map(int, row["Quantities"].split(', '))
    prices = map(float, row["ProductPricesInCP"].split(', '))

    order_date = pd.to_datetime(row["OrderDate"]).year

    for product_ids, quantity, price in zip(products_id, quantities, prices):
        index = final_df.index[final_df['product_code'] == product_ids].tolist()[0]
        final_df.at[index, f'quantity_{order_date}'] += quantity
        final_df.at[index, f'revenue_{order_date}'] += price

# Create final_v2_df
final_v2_df = final_df.groupby('product_name').agg({
    'type': 'first',  # Keep the original Product Type value
    'quantity_2019': 'sum', 
    'quantity_2020': 'sum', 
    'quantity_2021': 'sum', 
    'quantity_2022': 'sum', 
    'quantity_2023': 'sum', 
    'revenue_2019': 'sum', 
    'revenue_2020': 'sum', 
    'revenue_2021': 'sum', 
    'revenue_2022': 'sum', 
    'revenue_2023': 'sum'
}).reset_index()

# Save final_v2_df to CSV file
final_v2_df.to_csv('final_v2_df.csv', index=False)

# Save final_v2_df to JSON file
final_v2_df.to_json('final_v2_df.json', orient='records')