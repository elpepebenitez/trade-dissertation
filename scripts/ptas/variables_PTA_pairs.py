import pandas as pd

# Define the list of ISO3 codes considered as "north"
north_iso3 = [
    'AUS', 'AUT', 'BEL', 'CAN', 'DNK', 'FIN', 'FRA', 'DEU', 'GRC', 'ISL', 'ISR', 'ITA', 'JPN',
    'LUX', 'NLD', 'NZL', 'NOR', 'PRT', 'ESP', 'SWE', 'CHE', 'GBR', 'USA'
]

# Read the CSV file
file_path = './data/processed_data/intermediate/TPe_filtered_PTA_pairs.csv'
df = pd.read_csv(file_path)

# Remove rows where 'year' has NaN or zero values
df = df.dropna(subset=['year'])
df = df[df['year'] != '0']

# Convert 'year' to string without '.0' and ensure 'PTA_year' is also string
df['year'] = df['year'].astype(int).astype(str)
df['PTA_year'] = df['PTA_year'].astype(int).astype(str)

# Create NS_o and NS_d based on the conditions
df['NS_o'] = df['iso3_tp_o'].apply(lambda x: 'N' if x in north_iso3 else 'S')
df['NS_d'] = df['iso3_tp_d'].apply(lambda x: 'N' if x in north_iso3 else 'S')

# Create the direction variable by combining NS_o and NS_d
df['direction'] = df['NS_o'] + df['NS_d']

# Create the international variable
df['international'] = df.apply(lambda row: 1 if row['iso3_tp_o'] != row['iso3_tp_d'] else 0, axis=1)

# Create PTA, PTA_lag, and NSPTA based on the specified conditions
def calculate_PTA(row):
    if row['international'] == 0:
        return 0
    return row['PTA_number'] if int(row['PTA_year']) < int(row['year']) else 0

def calculate_PTA_lag(row):
    if row['international'] == 0:
        return 0
    try:
        return 1 if int(row['year']) - int(row['PTA_year']) >= 5 else 0
    except ValueError:
        return 0

def calculate_NSPTA(row):
    if row['international'] == 0:
        return 0
    return 'NS' if row['NS_o'] == 'N' or row['NS_d'] == 'N' else 'SS'

df['PTA'] = df.apply(calculate_PTA, axis=1)
df['PTA_lag'] = df.apply(calculate_PTA_lag, axis=1)
df['NSPTA'] = df.apply(calculate_NSPTA, axis=1)

# Create a unique identifier for each country-pair based on the direction of trade
df['pair_direction'] = df['iso3_tp_o'] + '-' + df['iso3_tp_d']

# Save the updated DataFrame to a new CSV file
output_file_path = './data/processed_data/intermediate/TPe_filtered_PTA_pairs_updated.csv'
df.to_csv(output_file_path, index=False)

print(df.head)

# Save the updated DataFrame to a new CSV file
output_file_path = './data/processed_data/gravity_sample/gravity_PTA_pairs.csv'
df.to_csv(output_file_path, index=False)

print(f"Updated data has been saved to {output_file_path}")