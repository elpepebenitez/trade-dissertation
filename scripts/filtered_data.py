import pandas as pd

# File paths
file_dahi = './data/processed_data/dahi_with_numeric_code.csv'
file_desta = './data/raw_data/pta/desta_list_of_treaties_02_02_dyads.csv'
# file_gravity = 'data/processed_data/Gravity_V202211_sample.csv'
file_gravity = 'data/raw_data/cepii/Gravity_csv_V202211/Gravity_V202211.csv'

# Reading the CSV files into dataframes
df_dahi = pd.read_csv(file_dahi)
df_desta = pd.read_csv(file_desta)
df_gravity = pd.read_csv(file_gravity, low_memory=False)

print(df_gravity.shape)

# Adding missing countries to the DAHI dataframe
missing_countries = {
    732: 'ESH',  # Western Sahara
    500: 'FLK',  # Falkland Islands
    900: 'XKX',  # Kosovo (or another unrecognized entity, XKX is often used)
    184: 'COK',  # Cook Islands
    570: 'NIU'   # Niue
}
missing_countries_df = pd.DataFrame({
    'numeric_code': list(missing_countries.keys()),
    'country_code': list(missing_countries.values()),
    'Cat': ['S'] * len(missing_countries)
})

df_dahi = pd.concat([df_dahi, missing_countries_df], ignore_index=True)

# Filtering DESTA dataframe for rows where the year is between 1995 and 2005
df_desta_filtered = df_desta[(df_desta['year'] >= 1995) & (df_desta['year'] <= 2005)]

# Merging DESTA with DAHI to get category for iso1
df_merged_iso1 = df_desta_filtered.merge(df_dahi[['numeric_code', 'Cat']], left_on='iso1', right_on='numeric_code', how='left')
df_merged_iso1.rename(columns={'Cat': 'Cat_iso1'}, inplace=True)

# Merging DESTA with DAHI to get category for iso2
df_merged_iso2 = df_merged_iso1.merge(df_dahi[['numeric_code', 'Cat']], left_on='iso2', right_on='numeric_code', how='left')
df_merged_iso2.rename(columns={'Cat': 'Cat_iso2'}, inplace=True)

# Function to classify the agreements
def classify_agreement(row):
    if row['Cat_iso1'] == 'N' and row['Cat_iso2'] == 'N':
        return 'North-North'
    elif (row['Cat_iso1'] in ['S', 'ES']) and (row['Cat_iso2'] in ['S', 'ES']):
        return 'South-South'
    elif (row['Cat_iso1'] == 'N' and row['Cat_iso2'] in ['S', 'ES']) or (row['Cat_iso1'] in ['S', 'ES'] and row['Cat_iso2'] == 'N'):
        return 'North-South'
    else:
        return 'Unknown'

# Applying the classification function to create the "Cat" column
df_merged_iso2['Cat'] = df_merged_iso2.apply(classify_agreement, axis=1)

# Dropping unnecessary columns
df_final = df_merged_iso2.drop(columns=['numeric_code_x', 'numeric_code_y', 'Cat_iso1', 'Cat_iso2'])

# Step 1: Filter out rows with North-North agreements
df_filtered = df_final[df_final['Cat'] != 'North-North']

# Step 2: Retain only rows of countries that have signed both North-South and South-South agreements
# Create a dataframe of countries with North-South agreements
north_south_countries = df_filtered[df_filtered['Cat'] == 'North-South'][['iso1', 'iso2']]

# Create a dataframe of countries with South-South agreements
south_south_countries = df_filtered[df_filtered['Cat'] == 'South-South'][['iso1', 'iso2']]

# Get the set of countries that appear in both North-South and South-South agreements
north_south_set = set(north_south_countries['iso1']).union(set(north_south_countries['iso2']))
south_south_set = set(south_south_countries['iso1']).union(set(south_south_countries['iso2']))
common_countries = north_south_set.intersection(south_south_set)

# Get the count of countries in common_countries
common_countries_count = len(common_countries)

# Filter the final dataframe to retain only rows with countries in the common set
df_final_filtered = df_filtered[(df_filtered['iso1'].isin(common_countries)) | (df_filtered['iso2'].isin(common_countries))]

# Calculate the min and max year in the final filtered dataframe
min_year = df_final_filtered['year'].min()
max_year = df_final_filtered['year'].max()

# Function to get counts of agreements
def get_agreement_counts(df, agreement_type):
    pair_counts = df[df['Cat'] == agreement_type].groupby(['iso1', 'iso2']).size().reset_index(name='count')
    one_agreement_count = (pair_counts['count'] == 1).sum()
    two_agreement_count = (pair_counts['count'] == 2).sum()
    three_or_more_agreements_count = (pair_counts['count'] >= 3).sum()
    return one_agreement_count, two_agreement_count, three_or_more_agreements_count

# Function to get pairs with exactly one agreement
def get_one_agreement_pairs(df, agreement_type):
    pair_counts = df[df['Cat'] == agreement_type].groupby(['iso1', 'iso2']).size().reset_index(name='count')
    one_agreement_pairs = pair_counts[pair_counts['count'] == 1][['iso1', 'iso2']]
    return one_agreement_pairs

# Get counts for North-South and South-South agreements
ns_one_agreement_count, ns_two_agreement_count, ns_three_or_more_agreements_count = get_agreement_counts(df_final_filtered, 'North-South')
ss_one_agreement_count, ss_two_agreement_count, ss_three_or_more_agreements_count = get_agreement_counts(df_final_filtered, 'South-South')

# Get one agreement pairs for North-South and South-South agreements
ns_one_agreement_pairs = get_one_agreement_pairs(df_final_filtered, 'North-South')
ss_one_agreement_pairs = get_one_agreement_pairs(df_final_filtered, 'South-South')

# Get counts of pairs with exactly one agreement
ns_one_agreement_pair_count = len(ns_one_agreement_pairs)
ss_one_agreement_pair_count = len(ss_one_agreement_pairs)

# Get the set of countries involved in both NS and SS one-agreement pairs
ns_one_agreement_countries = set(ns_one_agreement_pairs['iso1']).union(set(ns_one_agreement_pairs['iso2']))
ss_one_agreement_countries = set(ss_one_agreement_pairs['iso1']).union(set(ss_one_agreement_pairs['iso2']))

# Find common countries in NS and SS one-agreement pairs
common_ns_ss_countries = ns_one_agreement_countries.intersection(ss_one_agreement_countries)
common_ns_ss_countries_count = len(common_ns_ss_countries)

# Display the first few rows of the final filtered dataframe
print("Final Filtered Dataset:")
# print(df_final_filtered.head())

# Display the count of countries with both NS and SS agreements
print(f"\nNumber of countries with both North-South and South-South agreements: {common_countries_count}")

# Display the min and max year in the final filtered dataframe
print(f"\nMinimum year in the final filtered dataset: {min_year}")
print(f"Maximum year in the final filtered dataset: {max_year}")

# Display the disaggregated counts for North-South agreements
print(f"\nNumber of North-South pair countries with exactly 1 agreement: {ns_one_agreement_count}")
print(f"Number of North-South pair countries with exactly 2 agreements: {ns_two_agreement_count}")
print(f"Number of North-South pair countries with 3 or more agreements: {ns_three_or_more_agreements_count}")

# Display the disaggregated counts for South-South agreements
print(f"\nNumber of South-South pair countries with exactly 1 agreement: {ss_one_agreement_count}")
print(f"Number of South-South pair countries with exactly 2 agreements: {ss_two_agreement_count}")
print(f"Number of South-South pair countries with 3 or more agreements: {ss_three_or_more_agreements_count}")

# Display the counts of pairs with exactly one agreement
print(f"\nNumber of pairs with exactly 1 North-South agreement: {ns_one_agreement_pair_count}")
print(f"Number of pairs with exactly 1 South-South agreement: {ss_one_agreement_pair_count}")

# Display the count of common countries involved in both NS and SS one-agreement pairs
print(f"\nNumber of countries involved in both NS and SS one-agreement pairs: {common_ns_ss_countries_count}")

# Filtering the Gravity dataframe
# Step 1: Filter for years between 1990 and 2010
df_gravity_filtered = df_gravity[(df_gravity['year'] >= 1990) & (df_gravity['year'] <= 2010)]

# Step 2: Keep rows where the exporter is a South country
south_countries = df_dahi[df_dahi['Cat'].isin(['S', 'ES'])]['numeric_code'].tolist()
df_gravity_filtered = df_gravity_filtered[df_gravity_filtered['iso3num_o'].isin(south_countries)]

# Step 3: Keep rows where the exporter-destination pair appears in ns_one_agreement_pairs or ss_one_agreement_pairs
ns_pairs = set(zip(ns_one_agreement_pairs['iso1'], ns_one_agreement_pairs['iso2']))
ss_pairs = set(zip(ss_one_agreement_pairs['iso1'], ss_one_agreement_pairs['iso2']))

def is_in_pairs(row, pairs):
    return (row['iso3num_o'], row['iso3num_d']) in pairs

df_gravity_filtered = df_gravity_filtered[
    df_gravity_filtered.apply(lambda row: is_in_pairs(row, ns_pairs) or is_in_pairs(row, ss_pairs), axis=1)
]

# Display the first few rows of the filtered Gravity dataframe
print("Filtered Gravity Dataset:")
print(df_gravity_filtered.shape)

# Optionally, save the filtered Gravity dataframe to a new CSV file
df_gravity_filtered.to_csv('./data/processed_data/sample_filtered_gravity.csv', index=False)