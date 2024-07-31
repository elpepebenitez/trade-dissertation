import pandas as pd
import numpy as np

# Define file paths
input_file_path = './data/processed_data/merged_trade_gravity_NS_SS.csv'
output_file_path = './data/processed_data/sample_merged_trade_gravity_NS_SS.csv'

# Define filter criteria
sample_years = [1995, 2000, 2005, 2010, 2015]
sample_countries = ['PAN', 'CRI', 'COL']

# Read the data
data = pd.read_csv(input_file_path, low_memory=False)

# Filter the data
filtered_data = data[(data['year'].isin(sample_years)) & 
                     ((data['iso3_o'].isin(sample_countries)))]

# Ensure we have enough data to sample from
if len(filtered_data) < 2000:
    print("Not enough data to sample 2000 rows. Consider relaxing filter criteria.")
else:
    # Sample 2000 rows
    sample_data = filtered_data.sample(n=2000, random_state=1)
    
    # Save the sample data to a new CSV file
    sample_data.to_csv(output_file_path, index=False)
    print(f"Sample data saved to {output_file_path}")


# # Load the gravity data CSV file
# gravity_file_path = './data/raw_data/cepii/Gravity_csv_V202211/Gravity_V202211.csv'
# gravity_df = pd.read_csv(gravity_file_path, low_memory=False)
# # Load the trade data CSV file
# trade_file_path = "./data/raw_data/cepii/TPe_V202401.csv"
# trade_df = pd.read_csv(trade_file_path, low_memory=False)
# # Load the country key data CSV file
# country_key_file_path = "./data/raw_data/cepii/TradeProd_Gravity_country_key.csv"
# country_key_df = pd.read_csv(country_key_file_path, low_memory=False)

# print(gravity_df.columns)
# print(trade_df.columns)
# print(country_key_df.columns)

# print(gravity_df.dtypes)
# print(trade_df.dtypes)
# print(country_key_df.dtypes)

# # Define the time period and countries you are interested in
# start_year = 2000
# end_year = 2010
# countries = ['USA', 'CAN', 'MEX']  # Example countries

# # Filter the gravity data for the specified time period and countries
# filtered_gravity_df = gravity_df[
#     (gravity_df['year'] >= start_year) & 
#     (gravity_df['year'] <= end_year) & 
#     (gravity_df['iso3_o'].isin(countries))
# ]

# # Take a random sample of 5000 rows from the filtered data
# sampled_gravity_df = filtered_gravity_df.sample(n=2000, random_state=42)

# # Save the sample to a new CSV file
# gravity_output_file_path = './data/processed_data/Gravity_V202211_sample.csv'
# sampled_gravity_df.to_csv(gravity_output_file_path, index=False)

# print(f'Gravity sample saved to {gravity_output_file_path}')

# # Filter the trade data for the specified time period and countries
# filtered_trade_df = trade_df[
#     (trade_df['year'] >= start_year) & 
#     (trade_df['year'] <= end_year) & 
#     (trade_df['iso3_tp_o'].isin(countries))
# ]

# # Take a random sample of 5000 rows from the filtered data
# sampled_trade_df = filtered_trade_df.sample(n=2000, random_state=42)

# # Save the sample to a new CSV file
# trade_output_file_path = './data/processed_data/TPe_V202401_sample.csv'
# sampled_trade_df.to_csv(trade_output_file_path, index=False)

# print(f'Trade sample saved to {trade_output_file_path}')


