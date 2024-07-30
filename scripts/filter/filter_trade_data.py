import pandas as pd

# List of ISO3 codes for exporters to exclude
exclude_exporters = [
    'AUS', 'AUT', 'BEL', 'CAN', 'DNK', 'FIN', 'FRA', 'DEU', 'GRC', 'ISL', 'ISR', 'ITA', 'JPN',
    'LUX', 'NLD', 'NZL', 'NOR', 'PRT', 'ESP', 'SWE', 'CHE', 'GBR', 'USA'
]

# Function to filter trade data
def filter_trade_data(trade_data_path, filtered_trade_path):
    # Read trade data
    trade_data = pd.read_csv(trade_data_path, low_memory=False)

    # Filter years
    trade_data_filtered = trade_data[(trade_data['year'] >= 1995) & (trade_data['year'] <= 2015)]

    # Remove rows where the exporter is in the exclude list
    trade_data_filtered = trade_data_filtered[~trade_data_filtered['iso3_tp_o'].isin(exclude_exporters)]

    # Save filtered data
    trade_data_filtered.to_csv(filtered_trade_path, index=False)

    print(f"Filtered trade data saved to: {filtered_trade_path}")

# File paths
trade_data_file_path = "./data/raw_data/cepii/TPe_V202401.csv"
filtered_trade_file_path = "./data/processed_data/filtered_TPe_V202401.csv"

# Filter trade data
filter_trade_data(trade_data_file_path, filtered_trade_file_path)
