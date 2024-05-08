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

# Initialize columns for each year
for year in range(2019, 2024):
    final_df[f'Revenue - {year}'] = 0
    final_df[f'Quantity - {year}'] = 0

# Process orders and update final_df
for index, row in orders_df.iterrows():
    #products_names = row["Products"].split(', ')
    products_id = map(int, row["productsIDs"].split(', '))
    quantities = map(int, row["Quantities"].split(', '))
    prices = map(float, row["ProductPricesInCP"].split(', '))

    order_date = pd.to_datetime(row["OrderDate"]).year

    for product_ids, quantity, price in zip(products_id, quantities, prices):
        # Find the index of the row in final_df where 'Product Name' matches product_name
        #index = final_df.index[final_df['Product Name'] == product_name].tolist()[0]
        # Find the index of the row in final_df where product_code matches product_ids
        index = final_df.index[final_df['product_code'] == product_ids].tolist()[0]
        # Update the quantity for the corresponding product ID by adding the new quantity
        final_df.at[index, f'Quantity - {order_date}'] += quantity
        # Update the price for the corresponding product ID by adding the new price
        final_df.at[index, f'Revenue - {order_date}'] = final_df.at[index, f'Revenue - {order_date}'] + price

# Create final_v2_df
final_v2_df = final_df.groupby('Product Name').agg({
    'Type': 'first',  # Keep the original Product Type value
    'Quantity - 2019': 'sum', 
    'Quantity - 2020': 'sum', 
    'Quantity - 2021': 'sum', 
    'Quantity - 2022': 'sum', 
    'Quantity - 2023': 'sum', 
    'Revenue - 2019': 'sum', 
    'Revenue - 2020': 'sum', 
    'Revenue - 2021': 'sum', 
    'Revenue - 2022': 'sum', 
    'Revenue - 2023': 'sum'
}).reset_index()

# Save final_df and final_v2_df to CSV files
final_df.to_csv('final_df.csv', index=False)
final_v2_df.to_csv('final_v2_df.csv', index=False)