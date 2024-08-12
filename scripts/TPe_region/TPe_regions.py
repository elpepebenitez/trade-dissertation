import pandas as pd
import os

# Define file paths
ptas_dir = './data/processed_data/ptas'
aggregated_file = './data/processed_data/intermediate/aggregated_TPe_V202401.csv'
country_key_file = './data/raw_data/cepii/TradeProd_Gravity_country_key.csv'
output_dir = './data/processed_data/TPe'

# Load the country key mapping
country_key = pd.read_csv(country_key_file)

# Create a mapping from numeric to 3-letter ISO codes
iso3num_to_iso3 = country_key.set_index('iso3num')['iso3_tp'].to_dict()
iso3_to_iso3num = country_key.set_index('iso3_tp')['iso3num'].to_dict()

# Load the aggregated TPe data
aggregated_tpe = pd.read_csv(aggregated_file)

# Create output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# List all region files in the ptas directory
region_files = [f for f in os.listdir(ptas_dir) if f.endswith('.csv')]

# Process each region file
for region_file in region_files:
    region_path = os.path.join(ptas_dir, region_file)
    
    # Load the region data
    region_data = pd.read_csv(region_path)
    
    # Convert numeric ISO codes to 3-letter ISO codes
    region_data['iso1_3letter'] = region_data['iso1'].map(iso3num_to_iso3)
    region_data['iso2_3letter'] = region_data['iso2'].map(iso3num_to_iso3)
    
    # Keep all rows from aggregated_tpe where iso3_tp_o matches either iso1 or iso2
    filtered_tpe = aggregated_tpe[(aggregated_tpe['iso3_tp_o'].isin(region_data['iso1_3letter'])) |
                                  (aggregated_tpe['iso3_tp_o'].isin(region_data['iso2_3letter']))]
    
    # Save the filtered data to the output directory
    output_path = os.path.join(output_dir, region_file)
    filtered_tpe.to_csv(output_path, index=False)
    
    print(f"Filtered data for region '{region_file}' has been saved to {output_path}")
