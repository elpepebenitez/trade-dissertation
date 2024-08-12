import pandas as pd
import os

# Define file paths
ptas_dir = './data/processed_data/ptas/'
tpe_dir = './data/processed_data/TPe/'
country_key_file = './data/raw_data/cepii/TradeProd_Gravity_country_key.csv'
output_dir = './data/processed_data/stata/'

# Load the country key mapping
country_key = pd.read_csv(country_key_file)

# Create a mapping from numeric to 3-letter ISO codes
iso3num_to_iso3 = country_key.set_index('iso3num')['iso3_tp'].to_dict()
iso3_to_iso3num = country_key.set_index('iso3_tp')['iso3num'].to_dict()

# Create output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# List all region files in the ptas directory
region_files = [f for f in os.listdir(ptas_dir) if f.endswith('.csv')]

# Process each region file
for region_file in region_files:
    region_name = region_file.split('_')[0]
    pta_path = os.path.join(ptas_dir, region_file)
    tpe_path = os.path.join(tpe_dir, f'{region_name}_ptas.csv')
    
    if not os.path.exists(tpe_path):
        print(f"TPe file for region '{region_name}' does not exist, skipping.")
        continue
    
    # Load the PTA and TPe data
    pta_data = pd.read_csv(pta_path)
    tpe_data = pd.read_csv(tpe_path)
    
    # Convert numeric ISO codes to 3-letter ISO codes in PTA data
    pta_data['iso1_3letter'] = pta_data['iso1'].map(iso3num_to_iso3)
    pta_data['iso2_3letter'] = pta_data['iso2'].map(iso3num_to_iso3)
    
    # Create a set of tuples for easy lookup of country pairs in PTA data
    pta_pairs = set(zip(pta_data['iso1_3letter'], pta_data['iso2_3letter']))
    
    # Initialize new columns in TPe data
    tpe_data['PTA_ever'] = 0
    tpe_data['PTA_year'] = 0
    tpe_data['PTA_id'] = 0
    tpe_data['PTA'] = 0
    tpe_data['PTA_lag'] = 0
    
    for index, row in tpe_data.iterrows():
        pair = (row['iso3_tp_o'], row['iso3_tp_d'])
        reverse_pair = (row['iso3_tp_d'], row['iso3_tp_o'])
        if pair in pta_pairs or reverse_pair in pta_pairs:
            matching_pta = pta_data[((pta_data['iso1_3letter'] == pair[0]) & (pta_data['iso2_3letter'] == pair[1])) |
                                    ((pta_data['iso1_3letter'] == reverse_pair[0]) & (pta_data['iso2_3letter'] == reverse_pair[1]))]
            if not matching_pta.empty:
                pta_year = matching_pta['year'].values[0]
                pta_id = matching_pta['base_treaty'].values[0]
                tpe_data.at[index, 'PTA_ever'] = 1
                tpe_data.at[index, 'PTA_year'] = pta_year
                tpe_data.at[index, 'PTA_id'] = pta_id
                if row['year'] > pta_year:
                    tpe_data.at[index, 'PTA'] = 1
                if row['year'] >= pta_year + 5:
                    tpe_data.at[index, 'PTA_lag'] = 1

    # Save the processed data to the output directory
    output_path = os.path.join(output_dir, f'{region_name}_stata.csv')
    tpe_data.to_csv(output_path, index=False)
    
    print(f"Processed data for region '{region_name}' has been saved to {output_path}")
