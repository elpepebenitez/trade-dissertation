import pandas as pd
from data_cleaning import check_and_clean_data  # Import the data cleaning function
import pandas as pd

# Load datasets
dahi_path = './data/raw_data/dahi/Dahi.csv'
desta_path = './data/raw_data/pta/desta_list_of_treaties_02_02_dyads.csv'
country_map_path = './data/processed_data//country_agreements_classified_summary.csv'

dahi = pd.read_csv(dahi_path)
desta = pd.read_csv(desta_path)
country_map = pd.read_csv(country_map_path)

# Create a dictionary to map ISO3 letter codes to numeric codes
iso_map = dict(zip(country_map['Code'], country_map['numeric_code']))

# Add numeric codes to the Dahi dataset
dahi['numeric_code'] = dahi['Code'].map(iso_map)

# Merge Dahi and Desta datasets
dahi_renamed = dahi.rename(columns={'numeric_code': 'iso3num'})

# Merge to get country classifications
desta = desta.merge(dahi_renamed[['iso3num', 'Cat']], left_on='iso1', right_on='iso3num', how='left').rename(columns={'Cat': 'Cat_1'}).drop(columns=['iso3num'])
desta = desta.merge(dahi_renamed[['iso3num', 'Cat']], left_on='iso2', right_on='iso3num', how='left').rename(columns={'Cat': 'Cat_2'}).drop(columns=['iso3num'])

# Filter for North-South and South-South agreements
desta['agreement_type'] = desta.apply(
    lambda row: 'north-south' if (row['Cat_1'] == 'N' and row['Cat_2'] in ['S', 'ES']) or (row['Cat_2'] == 'N' and row['Cat_1'] in ['S', 'ES']) 
    else ('south-south' if row['Cat_1'] in ['S', 'ES'] and row['Cat_2'] in ['S', 'ES'] else None), axis=1)
desta_filtered = desta[desta['agreement_type'].notna()]

# Create a set of valid country pairs
valid_pairs = set(zip(desta_filtered['iso1'], desta_filtered['iso2']))

def filter_data(input_file_path, output_file_path, required_columns):
    """
    Filter the raw dataset and save the filtered data to a new CSV file.

    Parameters:
    input_file_path (str): Path to the input raw data file
    output_file_path (str): Path to the output filtered data file
    required_columns (list): List of required columns for the dataset
    """
    # Load data
    data = pd.read_csv(input_file_path, low_memory=False)

    # Filter for years 1990 to 2017
    data = data[(data['year'] >= 1990) & (data['year'] <= 2017)]

    # Map ISO3 letter codes to numeric codes
    data['iso3num_o'] = data['iso3_o'].map(iso_map)
    data['iso3num_d'] = data['iso3_d'].map(iso_map)

    # Filter for valid country pairs
    data['valid_agreement'] = data.apply(lambda row: (row['iso3num_o'], row['iso3num_d']) in valid_pairs or (row['iso3num_d'], row['iso3num_o']) in valid_pairs, axis=1)
    data = data[data['valid_agreement']]

    # Clean the data using the imported function
    # cleaned_data = check_and_clean_data(data, required_columns)

    # Save the filtered data to a new CSV file
    data.to_csv(output_file_path, index=False)
    print(f"Filtered data saved to {output_file_path}")

# Example usage
if __name__ == "__main__":
    input_file = './data/raw_data/cepii/Gravity_csv_V202211/Gravity_V202211.csv'
    output_file = './data/processed_data/filtered_gravity_data.csv'
    required_columns = ['year', 'iso3_o', 'iso3_d', 'iso3num_o', 'iso3num_d', 'gdp_o', 'gdp_d', 'dist', 'tradeflow_comtrade_o', 'comlang_off', 'contig', 'col_dep_ever', 'pop_o', 'pop_d']
    
    filter_data(input_file, output_file, required_columns)
