import pandas as pd

# List of ISO3 codes for exporters to exclude
exclude_exporters = [
    'AUS', 'AUT', 'BEL', 'CAN', 'DNK', 'FIN', 'FRA', 'DEU', 'GRC', 'ISL', 'ISR', 'ITA', 'JPN',
    'LUX', 'NLD', 'NZL', 'NOR', 'PRT', 'ESP', 'SWE', 'CHE', 'GBR', 'USA'
]

# Function to filter gravity data
def filter_gravity_data(gravity_data_path, filtered_gravity_path):
    # Read gravity data
    gravity_data = pd.read_csv(gravity_data_path, low_memory=False)

    # Filter years
    gravity_data_filtered = gravity_data[(gravity_data['year'] >= 1995) & (gravity_data['year'] <= 2015)]

    # Remove rows where the exporter is in the exclude list
    gravity_data_filtered = gravity_data_filtered[~gravity_data_filtered['iso3_o'].isin(exclude_exporters)]

    # Save filtered data
    gravity_data_filtered.to_csv(filtered_gravity_path, index=False)

    print(f"Filtered gravity data saved to: {filtered_gravity_path}")

# File paths
gravity_data_file_path = "./data/raw_data/cepii/Gravity_csv_V202211/Gravity_V202211.csv"
filtered_gravity_file_path = "./data/processed_data/filtered_Gravity_V202211.csv"

# Filter gravity data
filter_gravity_data(gravity_data_file_path, filtered_gravity_file_path)
