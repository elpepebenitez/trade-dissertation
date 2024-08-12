import pandas as pd
import os

# Load the first dataset
file_path_treaties = './data/raw_data/pta/desta_list_of_treaties_02_02.csv'
data_treaties = pd.read_csv(file_path_treaties)

# Filter the first dataset
filtered_treaties = data_treaties[
    (data_treaties['year'] >= 2000) & (data_treaties['year'] <= 2010) &
    (data_treaties['entryforceyear'] >= 2000) & (data_treaties['entryforceyear'] <= 2010) &
    (data_treaties['wto_listed'] == 1)
]

# Extract unique base_treaty values
base_treaty_values = filtered_treaties['base_treaty'].unique()

# Load the second dataset
file_path_dyads = './data/raw_data/pta/desta_list_of_treaties_02_02_dyads.csv'
data_dyads = pd.read_csv(file_path_dyads)

# Filter the second dataset based on base_treaty values from the first dataset
filtered_dyads = data_dyads[data_dyads['base_treaty'].isin(base_treaty_values)]

# Create output directory if it does not exist
output_dir = './data/processed_data/ptas/'
os.makedirs(output_dir, exist_ok=True)

# Get unique regions from the filtered dataset
regions = filtered_dyads['regioncon'].unique()

# Save filtered data for each region
for region in regions:
    region_data = filtered_dyads[filtered_dyads['regioncon'] == region]
    output_path = os.path.join(output_dir, f'{region}_ptas.csv')
    region_data.to_csv(output_path, index=False)
    print(f"Filtered data for region '{region}' has been saved to {output_path}")

