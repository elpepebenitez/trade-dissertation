# PSEUDO
# Static List of "North" and "South" countries
# 1. Get clean list of PTAs with membership
import pandas as pd

# Load the data
data = pd.read_csv('./input_data/pta/desta_list_of_treaties_02_02.csv')

# Select necessary columns and handle missing values for country columns
relevant_columns = ['base_treaty', 'name', 'year', 'entry_type', 'typememb'] + [f'c{i}' for i in range(1, 92)]
data = data[relevant_columns].fillna('')

# Drop entries where entry_type is 'negotiation'
data = data[data['entry_type'] != 'negotiation']

# Convert country code columns to lists of non-empty country codes, ensuring all are integers
def convert_to_integers(row):
    return [int(float(code)) for code in row if code != '']

data['countries'] = data.loc[:, 'c1':'c91'].apply(convert_to_integers, axis=1)

# Drop the individual country code columns as they are now aggregated
data.drop(columns=[f'c{i}' for i in range(1, 92)], inplace=True)

# Extract and save original names and original years for each base treaty
original_details = data[data['entry_type'] == 'base_treaty'][['base_treaty', 'name', 'year']].drop_duplicates('base_treaty')

# Convert 'year' to integer, handling non-numeric values
data['year'] = pd.to_numeric(data['year'], errors='coerce')

# Sort the data by 'year' to ensure chronological processing of updates
data.sort_values(by='year', inplace=True)

# Select the most recent entry for each base treaty
latest_entries = data.drop_duplicates(subset='base_treaty', keep='last')

# Merge with original details to replace modified names and years with the original ones
latest_entries = latest_entries.merge(original_details, on='base_treaty', how='left', suffixes=('', '_original'))
latest_entries['name'] = latest_entries['name_original'].fillna(latest_entries['name'])
latest_entries['year'] = latest_entries['year_original'].fillna(latest_entries['year']).astype(int)
latest_entries.drop(columns=['name_original', 'year_original', 'entry_type', 'typememb'], inplace=True)

# Save to CSV
latest_entries.to_csv('./output_data/pta_updated_membership.csv', index=False)